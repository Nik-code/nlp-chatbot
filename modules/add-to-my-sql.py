import numpy as np
import csv
import mysql.connector
from dotenv import load_dotenv
import os

# Lists to store questions, answers, and sentence embeddings
questions = []
answers = []
sentence_embeddings = []

# Read the sentence_embedding.csv file
with open('sentence_embedding.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    # Iterate over each row in the CSV file
    for row in reader:
        # Extract question, embedding, and answer from the row
        question = row[0]
        embedding = np.array(row[3].strip('[]').split(), dtype=np.float32)
        answer = row[1]

        # Append data to the respective lists
        questions.append(question)
        sentence_embeddings.append(embedding)
        answers.append(answer)


# Load the environment variables from .env file
load_dotenv('../values.env')

# Access the credentials using os.getenv()
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Connect to MySQL
cnx = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = cnx.cursor()

# Insert data into the MySQL table
for i in range(len(questions)):
    # SQL query to insert data into the table
    query = "INSERT INTO data (question, answer, embeddings) VALUES (%s, %s, %s)"
    values = (questions[i], answers[i], str(sentence_embeddings[i]))

    # Execute the query
    cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()

print("Data inserted successfully!")
