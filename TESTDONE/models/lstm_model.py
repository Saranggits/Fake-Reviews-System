import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import os
import re
import mysql.connector
from mysql.connector import Error

class LSTMModel:
    def __init__(self, max_words=10000, max_len=200):
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = Tokenizer(num_words=max_words)
        self.model = None
        self.db_connection = None
        
    def connect_to_database(self, host, user, password, database):
        """
        Establish connection to MySQL database
        """
        try:
            self.db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.db_connection.is_connected():
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
            
    def close_database_connection(self):
        """
        Close the database connection
        """
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            print("Database connection closed")
            
    def save_prediction_to_db(self, text, predicted_class, confidence):
        """
        Save a prediction result to the database
        """
        if not self.db_connection or not self.db_connection.is_connected():
            print("No database connection available")
            return False
            
        try:
            cursor = self.db_connection.cursor()
            query = """
                INSERT INTO predictions (text, predicted_class, confidence)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (text, int(predicted_class), float(confidence)))
            self.db_connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error saving prediction to database: {e}")
            return False
        
    def build_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.max_words, 128),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(3, activation='softmax')  # 3 classes: negative, neutral, positive
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def preprocess_text(self, text):
        if isinstance(text, (np.ndarray, list)):
            return [self.preprocess_text(t) for t in text]
        
        # Convert to string if not already
        text = str(text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
        
    def prepare_text(self, texts):
        # Preprocess texts
        texts = self.preprocess_text(texts)
        
        if not isinstance(texts, list):
            texts = [texts]
            
        # Convert to sequences
        sequences = self.tokenizer.texts_to_sequences(texts)
        
        # Pad sequences
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len)
        
        return padded_sequences
        
    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
        # Preprocess all texts
        X_train = self.preprocess_text(X_train)
        X_val = self.preprocess_text(X_val)
        
        # Fit tokenizer on training data
        self.tokenizer.fit_on_texts(X_train)
        
        # Convert text to sequences
        X_train_seq = self.prepare_text(X_train)
        X_val_seq = self.prepare_text(X_val)
        
        # Build and train model
        if not self.model:
            self.build_model()
            
        history = self.model.fit(
            X_train_seq, y_train,
            validation_data=(X_val_seq, y_val),
            epochs=epochs,
            batch_size=batch_size
        )
        
        return history
        
    def predict(self, texts):
        if not self.model:
            raise ValueError("Model not trained yet!")
            
        # Prepare text
        X_seq = self.prepare_text(texts)
        
        # Get predictions with probabilities
        predictions = self.model.predict(X_seq)
        
        # Get class labels and confidence scores
        predicted_classes = np.argmax(predictions, axis=1)
        confidence_scores = np.max(predictions, axis=1)
        
        return predicted_classes, confidence_scores
        
    def save(self, model_path, tokenizer_path):
        if not self.model:
            raise ValueError("No model to save!")
            
        # Save model
        self.model.save(model_path)
        
        # Save tokenizer
        tokenizer_json = self.tokenizer.to_json()
        with open(tokenizer_path, 'w') as f:
            json.dump(tokenizer_json, f)
            
    @classmethod
    def load(cls, model_path, tokenizer_path):
        instance = cls()
        
        # Load model
        instance.model = tf.keras.models.load_model(model_path)
        
        # Load tokenizer
        with open(tokenizer_path, 'r') as f:
            tokenizer_json = json.load(f)
            instance.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)
            
        return instance 