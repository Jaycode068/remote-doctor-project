import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="johnson",
    password="Ibelieve1!",
    database="remote_doctor"
)

# Check if the connection was successful
if connection.is_connected():
    print("Connected to the database")

    # Perform a test query or operation
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed")

else:
    print("Failed to connect to the database")

