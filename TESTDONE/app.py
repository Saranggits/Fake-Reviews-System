from flask import Flask, request, jsonify, render_template
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import string
import numpy as np
from database import Database
from models.lstm_model import LSTMModel

app = Flask(__name__)
db = Database()

# --- Load TF-IDF Vectorizer and Models ---
vectorizer = None
svm_model = None
lr_model = None
lstm_model = None

try:
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    print("TF-IDF Vectorizer lo-aded successfully.")
except FileNotFoundError:
    print("Warning: 'models/tfidf_vectorizer.pkl' not found. TF-IDF will be non-functional or mock.")
except Exception as e:
    print(f"Error loading TF-IDF vectorizer: {e}")

try:
    svm_model = joblib.load('models/svm_model.pkl')
    print("SVM model loaded successfully.")
except FileNotFoundError:
    print("Warning: 'models/svm_model.pkl' not found. SVM predictions will be unavailable.")
except Exception as e:
    print(f"Error loading SVM model: {e}")

try:
    lr_model = joblib.load('models/logistic_regression_model.pkl')
    print("Logistic Regression model loaded successfully.")
except FileNotFoundError:
    print("Warning: 'models/logistic_regression_model.pkl' not found. Logistic Regression predictions will be unavailable.")
except Exception as e:
    print(f"Error loading Logistic Regression model: {e}")

try:
    lstm_model = LSTMModel.load('models/lstm_model', 'models/lstm_tokenizer.json')
    print("LSTM model loaded successfully.")
except FileNotFoundError:
    print("Warning: LSTM model files not found. LSTM predictions will be unavailable.")
except Exception as e:
    print(f"Error loading LSTM model: {e}")

lemmatizer = WordNetLemmatizer()
stop_words_english = set(stopwords.words('english'))

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return nltk.corpus.wordnet.NOUN

def preprocess_text(text):
    if not isinstance(text, str):
        print(f"Warning: preprocess_text received non-string input: {type(text)}. Returning empty string.")
        return ""
        
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    
    lemmatized_tokens = []
    for word, tag in pos_tags:
        if word.isalpha() and word not in stop_words_english:
            wordnet_tag = get_wordnet_pos(tag)
            lemma = lemmatizer.lemmatize(word, pos=wordnet_tag)
            lemmatized_tokens.append(lemma)
            
    processed_text = " ".join(lemmatized_tokens)
    print(f"Original: {text[:100]}... | Processed: {processed_text[:100]}...")
    return processed_text

def apply_tf_idf(texts):
    if vectorizer:
        print("Applying loaded TF-IDF vectorizer...")
        if isinstance(texts, str):
            texts = [texts]
        return vectorizer.transform(texts)
    else:
        print("TF-IDF vectorizer not loaded. Using mock TF-IDF.")
        return [[0.1, 0.5, 0.3] for _ in texts]

def predict_svm(features):
    print("Attempting SVM prediction...")
    if svm_model and features is not None:
        try:
            pred = svm_model.predict(features)
            proba = svm_model.predict_proba(features)
            confidence = np.max(proba, axis=1)
            return pred, confidence
        except Exception as e:
            print(f"Error during SVM prediction: {e}")
            return ["SVM_ERROR" for _ in range(len(features))], [0.0 for _ in range(len(features))]
    print("SVM model not loaded or no features. Returning unavailable.")
    return ["SVM_UNAVAILABLE" for _ in range(len(features))], [0.0 for _ in range(len(features))]

def predict_logistic_regression(features):
    print("Attempting Logistic Regression prediction...")
    if lr_model and features is not None:
        try:
            pred = lr_model.predict(features)
            proba = lr_model.predict_proba(features)
            confidence = np.max(proba, axis=1)
            return pred, confidence
        except Exception as e:
            print(f"Error during LR prediction: {e}")
            return ["LR_ERROR" for _ in range(len(features))], [0.0 for _ in range(len(features))]
    print("LR model not loaded or no features. Returning unavailable.")
    return ["LR_UNAVAILABLE" for _ in range(len(features))], [0.0 for _ in range(len(features))]

def predict_lstm(text):
    print("Attempting LSTM prediction...")
    if lstm_model:
        try:
            classes, confidence = lstm_model.predict([text])
            # Convert numeric predictions back to labels
            label_mapping = {0: 'negative', 1: 'neutral', 2: 'positive'}
            predictions = [label_mapping[cls] for cls in classes]
            return predictions, confidence
        except Exception as e:
            print(f"Error during LSTM prediction: {e}")
            return ["LSTM_ERROR"], [0.0]
    print("LSTM model not loaded. Returning unavailable.")
    return ["LSTM_UNAVAILABLE"], [0.0]

@app.route('/')
def home():
    return render_template('wlc.html', title='Welcome')

@app.route('/detect')
def detect():
    return render_template('detect.html', title='Detect Fake Reviews')

@app.route('/result')
def result():
    return render_template('result.html', title='Analysis Results')

@app.route('/analyze', methods=['POST'])
def analyze_reviews():
    try:
        data = request.get_json()
        url = data.get('url', '')
        review_text = data.get('review_text', '')
        
        # Use either URL or review text
        text_to_analyze = review_text if review_text else url
        
        if not text_to_analyze:
            return jsonify({'error': 'No text to analyze'}), 400
            
        # Vectorize the text
        text_vector = vectorizer.transform([text_to_analyze])
        
        # Get predictions
        svm_pred = 'Real' if svm_model.predict(text_vector)[0] == 1 else 'Fake'
        lr_pred = 'Real' if lr_model.predict(text_vector)[0] == 1 else 'Fake'
        
        # Calculate final prediction
        predictions = [svm_pred, lr_pred]
        final_pred = 'Real' if predictions.count('Real') >= len(predictions)/2 else 'Fake'
        
        # Calculate confidence
        svm_prob = svm_model.predict_proba(text_vector)[0]
        lr_prob = lr_model.predict_proba(text_vector)[0]
        
        confidence = np.mean([
            svm_prob.max() * 100,
            lr_prob.max() * 100
        ])
        
        # Save to database
        db.save_analysis(
            review_text=text_to_analyze,
            url=url,
            svm_pred=svm_pred,
            lr_pred=lr_pred,
            final_pred=final_pred,
            accuracy=confidence
        )

        return jsonify({
            'prediction': final_pred,
            'accuracy': confidence,
            'svm_prediction': svm_pred,
            'lr_prediction': lr_pred
        })
        
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    history = db.get_analysis_history()
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 