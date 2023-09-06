# NLP Chatbot

An advanced NLP-based chatbot developed using Flask, integrated with a MySQL database, and enhanced with encryption for data security.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contribution](#contribution)
- [License](#license)

## Features

### Flask Application

- The main server is set up using Flask.
- Configuration is managed through environment variables from `values.env`.

### User Management

- User details are stored securely in a MySQL database.
- Passwords are hashed using `bcrypt` before storage, ensuring data security.
- Functions to insert users and retrieve users by username are encapsulated in `controllers.py`.

### Database Operations

- Utilizes SQLAlchemy for Object-Relational Mapping (ORM).
- The `User` model is defined with attributes such as `username`, `name`, `email`, `card_number`, and `password`.
- Database connection and CRUD operations are managed in `database.py`.

### Encryption

- Employs the `cryptography` library for robust encryption and decryption mechanisms.
- Public and private keys (`public_key.pem` and `private_key.pem`) are utilized for these operations.
- Functions for encryption and decryption are housed in `security.py`.

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/Nik-code/nlp-chatbot.git
   cd nlp-chatbot
2. **Dependencies**: Install the required Python packages:
   ```
   pip install -r requirements.txt 
3. **Environment Variables**: Ensure your values.env file is set up with the necessary configurations:
  - **SECRET_KEY**: Secret key for Flask.
  - **DB_HOST**: Database host.
  - **DB_USER**: Database user.
  - **DB_PASSWORD**: Database password.
  - **DB_NAME**: Database name.

## Usage

Start the Flask server using the following command:
  ```
python main.py
```
By default, the server will run on port 6000. Navigate to http://localhost:6000 in your browser to access the chatbot.

## Dependencies 

The project relies on several Python packages for its functionality. Some of the primary dependencies include:

- Flask
- bcrypt
- cryptography
- SQLAlchemy
... and many more. Refer to `requirements.txt` for the complete list.

## Contribution

Contributions are always welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is open-source and available under the MIT License.
