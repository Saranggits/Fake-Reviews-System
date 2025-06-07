import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # MySQL root username
                password='5036',  # Your MySQL root password
                database='fake_review_db'
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None

    def close(self):
        if hasattr(self, 'connection') and self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def save_analysis(self, review_text, url, svm_pred, lr_pred, final_pred, accuracy):
        if not self.connection or not self.connection.is_connected():
            print("Database connection not available")
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Insert into analysis_history
            query = """
            INSERT INTO analysis_history 
            (url_analyzed, review_text, prediction_result, confidence_score) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (url, review_text, final_pred, accuracy))
            
            # If there's a review text, also save it to reviews table
            if review_text:
                # First check if product exists
                product_query = "SELECT product_id FROM products WHERE url = %s"
                cursor.execute(product_query, (url,))
                product = cursor.fetchone()
                
                if not product:
                    # Insert new product
                    product_query = """
                    INSERT INTO products (name, url, platform) 
                    VALUES (%s, %s, %s)
                    """
                    platform = self._get_platform_from_url(url)
                    cursor.execute(product_query, ("Unknown Product", url, platform))
                    product_id = cursor.lastrowid
                else:
                    product_id = product[0]
                
                # Insert review
                review_query = """
                INSERT INTO reviews 
                (product_id, review_text, is_fake, confidence_score) 
                VALUES (%s, %s, %s, %s)
                """
                is_fake = final_pred.lower() == 'fake'
                cursor.execute(review_query, (product_id, review_text, is_fake, accuracy))
                
                # Get the review_id
                review_id = cursor.lastrowid
                
                # Insert analysis results
                analysis_query = """
                INSERT INTO analysis_results 
                (review_id, svm_prediction, lr_prediction, final_prediction, accuracy) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(analysis_query, (review_id, svm_pred, lr_pred, final_pred, accuracy))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error saving analysis: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_analysis_history(self, limit=10):
        if not self.connection or not self.connection.is_connected():
            print("Database connection not available")
            return []
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT * FROM analysis_history 
            ORDER BY analyzed_at DESC 
            LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching analysis history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def _get_platform_from_url(self, url):
        if not url:
            return "Unknown"
        url = url.lower()
        if "amazon" in url:
            return "Amazon"
        elif "flipkart" in url:
            return "Flipkart"
        elif "meesho" in url:
            return "Meesho"
        else:
            return "Other"

# Example usage:
if __name__ == "__main__":
    db = Database()
    try:
        # Test saving an analysis
        db.save_analysis(
            review_text="This product is amazing!",
            url="https://amazon.com/product123",
            svm_pred="positive",
            lr_pred="positive",
            final_pred="Real",
            accuracy=95.5
        )
        
        # Test getting history
        history = db.get_analysis_history()
        print("Analysis History:", history)
        
    finally:
        db.close() 