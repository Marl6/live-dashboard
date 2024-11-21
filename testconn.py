import pyodbc

# Define the connection string (same as in your script)
DB_CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;DATABASE=consumptiondb;'
    'UID=DESKTOP-AUBLB3S\\Admin;PWD=Yukithedog'
)

# Try connecting to the database
try:
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    print("Connected to the database successfully.")
    
    # Optionally, test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM powerconsumption")
    row = cursor.fetchone()
    
    if row:
        print("Data found in powerconsumption table.")
    else:
        print("No data found in powerconsumption table.")
    
    # Close the connection
    conn.close()
except Exception as e:
    print("Error:", e)
