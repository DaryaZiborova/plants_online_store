import psycopg2
from psycopg2 import sql

host = "vectordb.c78quweqw7tg.us-east-1.rds.amazonaws.com"  
port = 5432                            
database = "vectorDB"         
username = "postgres"               
password = "001001p4ssw0rd"               

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=username,
        password=password
    )
    print("Connection to AWS RDS PostgreSQL database successful!")
    cursor = connection.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    connection.commit()
    print("pgvector extension installed successfully.")

    cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
    result = cursor.fetchone()
    if result:
        print(f"pgvector is enabled: {result}")
    else:
        print("Failed to enable pgvector.")

except Exception as error:
    print(f"Error connecting to the database: {error}")
