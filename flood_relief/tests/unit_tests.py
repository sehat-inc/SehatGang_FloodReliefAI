import psycopg2

# Database connection details
db_config = {
    'host': '10.1.154.147',  # Replace with your friend's IP address
    'port': '5432',                     # Default PostgreSQL port
    'dbname': 'floodrelief',     # Replace with the database name
    'user': 'postgres',            # Replace with the PostgreSQL username
    'password': 'maaz'         # Replace with the PostgreSQL password
}

try:
    # Establish a connection to the database
    connection = psycopg2.connect(**db_config)
    print("Connected to the database!")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Example: Execute a query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Database version:", db_version)


except Exception as e:
    print("Error connecting to the database:", e)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Database connection closed.")