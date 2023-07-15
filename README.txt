Flask Project API

This project is a Flask API that provides functionality for managing user records in a MongoDB database. 
It allows users to perform CRUD operations (Create, Read, Update, Delete) on user data.

Installation
Clone the repository:
shell
Copy code
git clone <repository-url>
Navigate to the project directory:
shell
Copy code
cd flask-project-api
Install the required dependencies:
shell
Copy code
pip install -r requirements.txt
Set up a MongoDB database and provide the connection details in the Flask application code (app.py).
Usage
Start the Flask server:
shell
Copy code
python app.py
The API will be accessible at http://localhost:5000.
Endpoints
GET /users
Retrieves all user records from the MongoDB database.

Request:

Method: GET
Endpoint: /users
Response:

Status Code: 200 (OK)
Body:
json
Copy code
[
  {
    "_id": "609e45cc335c9a2d1cde32a1",
    "firstname": "Manish",
    "lastname": "Kumar",
    "email": "manishkumar@gmail.com",
    "phone": "1234567890",
    "dob": "1990-01-01"
  },
  {
    "_id": "609e45cc335c9a2d1cde32a2",
    "firstname": "Piyush",
    "lastname": "Kumar",
    "email": "piyushkumar@gmail.com",
    "phone": "9876543210",
    "dob": "1995-05-10"
  }
]
POST /users
Creates a new user record in the MongoDB database.

Request:

Method: POST
Endpoint: /users
Body:
json
Copy code
{
  "firstname": "Rajat",
  "lastname": "Tyagi",
  "email": "rajatyagi1996@gmail.com",
  "phone": "4567891230",
  "dob": "1988-08-20"
}
Response:

Status Code: 200 (OK)
Body:
json
Copy code
{
  "message": "User created successfully"
}
GET /users/{id}
Retrieves a specific user record from the MongoDB database by ID.

Request:

Method: GET
Endpoint: /users/{id} (replace {id} with the user's ID)
Response:

Status Code: 200 (OK)
Body:
json
Copy code
{
  "_id": "609e45cc335c9a2d1cde32a1",
  "firstname": "Amit",
  "lastname": "Goswami",
  "email": "amitgoswami089@gmail.com",
  "phone": "1234567890",
  "dob": "1990-01-01"
}
PUT /users/{id}
Updates a specific user record in the MongoDB database by ID.

Request:

Method: PUT
Endpoint: /users/{id} (replace {id} with the user's ID)
Body:
json
Copy code
{
  "phone": "5555555555"
}
Response:

Status Code: 200 (OK)
Body:
json
Copy code
{
  "message": "User updated successfully"
}
DELETE /users/{id}
Deletes a specific user record from the MongoDB database by ID.

Request:

Method: DELETE
Endpoint: /users/{id} (replace {id} with the user's ID)
Response:

Status Code: 200 (OK)
Body:
json
Copy code
{
  "message": "User deleted successfully"
}
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, 
please open an issue or submit a pull request.

To setup db run command docker-compose up -d