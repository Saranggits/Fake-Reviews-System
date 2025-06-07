import mysql.connector

def try_connection():
    try:
        # First try to connect as root to check if database exists
        root_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='5036'  # Try with no password first
        )
        
        if root_connection.is_connected():
            print("\n✅ Successfully connected as root!")
            cursor = root_connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            # Try to create database if it doesn't exist
            if 'fake_review_db' not in [db[0] for db in databases]:
                print("\nCreating database 'fake_review_db'...")
                cursor.execute("CREATE DATABASE fake_review_db")
                print("✅ Database created successfully!")
            
            cursor.close()
            root_connection.close()
            
            # Now try to connect to the specific database
            print("\nTrying to connect to fake_review_db...")
            connection = mysql.connector.connect(
                host='localhost',
                user='fake-review',
                password='5036',
                database='fake_review_db'
            )
            
            if connection.is_connected():
                print("✅ Successfully connected to fake_review_db!")
                db_info = connection.get_server_info()
                print(f"✅ Connected to MySQL Server version {db_info}")
                
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                print("\n✅ Available tables:")
                for table in tables:
                    print(f"   - {table[0]}")
                
                cursor.close()
                connection.close()
                print("\n✅ Database connection closed successfully")
                return True
                
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    try_connection() 