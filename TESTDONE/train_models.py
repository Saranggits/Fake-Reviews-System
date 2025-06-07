import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from models.lstm_model import LSTMModel
from sklearn.metrics import classification_report
import joblib
import os


# Create models directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('large_dataset.csv')

# Using the correct column names from the dataset
X = df['review_text'].values
y = df['sentiment'].values

# Convert sentiment labels to numeric
label_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
y_numeric = np.array([label_mapping[label] for label in y])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_numeric, test_size=0.2, random_state=42)
X_train_text, X_val, y_train_text, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Convert numpy arrays to lists for LSTM
print("\nPreparing data for LSTM...")
X_train_text = X_train_text.tolist()
X_val = X_val.tolist()
X_test = X_test.tolist()

# 1. Train TF-IDF Vectorizer
print("\nTraining TF-IDF Vectorizer...")
tfidf = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Save the vectorizer
joblib.dump(tfidf, 'models/tfidf_vectorizer.pkl')
print("TF-IDF Vectorizer saved.")

# 2. Train SVM with probability estimates
print("\nTraining SVM model...")
svm = SVC(kernel='linear', probability=True)
svm.fit(X_train_tfidf, y_train)
svm_pred = svm.predict(X_test_tfidf)
svm_proba = svm.predict_proba(X_test_tfidf)
print("\nSVM Classification Report:")
print(classification_report(y_test, svm_pred))
joblib.dump(svm, 'models/svm_model.pkl')
print("SVM model saved.")

# 3. Train Logistic Regression
print("\nTraining Logistic Regression model...")
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_tfidf, y_train)
lr_pred = lr.predict(X_test_tfidf)
lr_proba = lr.predict_proba(X_test_tfidf)
print("\nLogistic Regression Classification Report:")
print(classification_report(y_test, lr_pred))
joblib.dump(lr, 'models/logistic_regression_model.pkl')
print("Logistic Regression model saved.")

# 4. Train LSTM Model
print("\nTraining LSTM model...")
lstm_model = LSTMModel()
history = lstm_model.train(
    X_train_text, 
    y_train_text,
    X_val,
    y_val,
    epochs=5,
    batch_size=32
)

# Evaluate LSTM
lstm_classes, lstm_confidence = lstm_model.predict(X_test)
print("\nLSTM Classification Report:")
print(classification_report(y_test, lstm_classes))

# Save LSTM model
lstm_model.save('models/lstm_model', 'models/lstm_tokenizer.json')
print("LSTM model saved.")

print("\nAll models have been trained and saved successfully!") 