import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    connection = None
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password="5036"  # Your MySQL root password
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL server")
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS fake_review_db")
            print("✅ Database created or already exists")
            
            # Use the database
            cursor.execute("USE fake_review_db")
            
            # Create products table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) UNIQUE,
                platform VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("✅ Products table created")
            
            # Create reviews table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                review_text TEXT,
                is_fake BOOLEAN,
                confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
            """)
            print("✅ Reviews table created")
            
            # Create analysis_results table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                analysis_id INT AUTO_INCREMENT PRIMARY KEY,
                review_id INT,
                svm_prediction VARCHAR(50),
                lr_prediction VARCHAR(50),
                final_prediction VARCHAR(50),
                accuracy FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (review_id) REFERENCES reviews(review_id)
            )
            """)
            print("✅ Analysis results table created")
            
            # Create analysis_history table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                url_analyzed VARCHAR(255),
                review_text TEXT,
                prediction_result VARCHAR(50),
                confidence_score FLOAT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("✅ Analysis history table created")
            
            connection.commit()
            print("✅ All tables created successfully")
            
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ MySQL connection closed")

if __name__ == "__main__":
    print("Setting up database and tables...")
    create_database_and_tables() 