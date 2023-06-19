import numpy as np
import time
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from spellchecker import SpellChecker
import os
from dotenv import load_dotenv

# Constants
MIN_MATCHING_SCORE = 0.6

# SpellChecker initialization
spell = SpellChecker()

# SentenceTransformer initialization
model = SentenceTransformer('paraphrase-mpnet-base-v2')

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


def preprocess_sentence(sentence):
    sentence = sentence.lower()
    return sentence


def fetch_data_from_db():
    cursor = cnx.cursor()
    # Fetch data from the database
    questions, answers, embeddings = [], [], []

    query = "SELECT question, answer, embeddings FROM data"
    cursor.execute(query)

    for row in cursor:
        question, embedding, answer = row[0], np.array(row[2].strip('[]').split(), dtype=np.float32), row[1]
        questions.append(question)
        embeddings.append(embedding)
        answers.append(answer)

    cursor.close()
    sentence_embeddings = np.array(embeddings)
    return questions, answers, sentence_embeddings


def get_response(query, mode):
    questions, answers, sentence_embeddings = fetch_data_from_db()
    t1 = time.time()
    preprocessed_query = preprocess_sentence(query)

    # Rest of your code to correct the query and calculate similarities
    corrected_query = ' '.join(spell.correction(word) for word in preprocessed_query.split())
    query_embedding = model.encode([corrected_query])
    similarities = cosine_similarity(query_embedding, sentence_embeddings)

    k = 5
    top_indices = np.argsort(similarities[0])[::-1][:k]
    matching_scores = similarities[0][top_indices]
    response = answers[top_indices[0]] if matching_scores[0] >= MIN_MATCHING_SCORE else "I'm sorry, I don't have an answer for that."
    t2 = time.time()

    top_sentences = [questions[i] for i in top_indices]  # Retrieve the top-k similar sentences
    matching_scores = similarities[0][top_indices]  # Retrieve the matching scores
    if mode == 'admin':
        # Print the top results
        if matching_scores[0] < MIN_MATCHING_SCORE:
            print("Time taken:", t2 - t1)
            return [["No match found", "I'm sorry, I don't have an answer for that.", 0]]
        else:
            output = []
            for i, (sentence, score) in enumerate(zip(top_sentences, matching_scores)):
                output.append([sentence, answers[top_indices[i]], float(score)])

            print("Time taken for Query Processing:", t2 - t1)
            return output
    else:
        return response
