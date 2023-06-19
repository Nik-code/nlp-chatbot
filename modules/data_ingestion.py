import csv
from sentence_transformers import SentenceTransformer
import time


def preprocess_sentence(sentence):
    # Convert the sentence to lowercase
    return sentence.lower()


# List to store the sentences read from the CSV file
sentences = []
t1 = time.time()

# Open the CSV file
with open('question-answer.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    # Read each row in the CSV file and append it to the sentences list
    sentences = list(reader)

# Separate the questions and answers from the sentences list
questions = [row[0] for row in sentences]
answers = [','.join(row[1:]) for row in sentences]

# Set to store unique questions
unique_questions = set(questions)

# Set to store duplicate questions
duplicates = set(q for q in questions if questions.count(q) > 1)

# Replace duplicate questions with an empty string
questions = ['' if q in duplicates else q for q in questions]

# Preprocess all sentences
preprocessed_sentences = [preprocess_sentence(sentence) for sentence in questions]

# Step 2: Sentence Embeddings
model = SentenceTransformer('paraphrase-mpnet-base-v2')
sentence_embeddings = model.encode(preprocessed_sentences)

# Create a new CSV file to store the preprocessed sentences and their vector representations
with open('sentence_embedding.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(['question', 'answer', 'preprocessed_sentence', 'vector'])  # Write the header row

    # Write the unique questions and their embeddings to the CSV file
    for i in range(len(questions)):
        if questions[i] != '':
            writer.writerow([questions[i], answers[i], preprocessed_sentences[i], sentence_embeddings[i]])

# Calculate and print the time taken for preprocessing and embedding
print(f"Preprocessing and embedding took {(time.time() - t1)} seconds")
