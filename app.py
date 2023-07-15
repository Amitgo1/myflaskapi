from flask import Flask, Blueprint, jsonify, request
from bson import ObjectId
from pymongo import MongoClient
from flask_restful import Resource, Api
import re
import datetime

app = Flask(__name__)
users_bp = Blueprint('api', __name__)
api = Api(users_bp)

class UsersView(Resource):
    ALLOWED_KEYS = ['firstname','lastname','email','phone','dob']
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]
        self.collection = self.db["user"]

    def get_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def get_phone(self, phone):
        pattern = r'^\d{10}$'  # Assuming 10-digit phone number format
        return re.match(pattern, phone) is not None

    def get_dob(self, dob):
        try:
            datetime.datetime.strptime(dob, '%d %B %Y')  # Assuming DD Month YYYY format
            return True
        except ValueError:
            return False

    def get(self, id = None):
        if id:
            data = []
            for i in self.collection.find({"_id":ObjectId(id)}):
                i['_id'] = str(i['_id'])
                data.append(i)
            return jsonify(data)
                
        else:
            data = list(self.collection.find())
            for document in data:
                document['_id'] = str(document['_id'])
            return jsonify(data)

    def post(self):
        new_record = request.get_json()
        required_fields = ['firstname', 'lastname', 'email', 'phone', 'dob']

        if all(field in new_record for field in required_fields):
            firstname = new_record['firstname']
            lastname = new_record['lastname']
            email = new_record['email']
            phone = new_record['phone']
            dob = new_record['dob']

            if firstname and lastname and self.get_email(email) and self.get_phone(phone) and self.get_dob(dob):
                self.collection.insert_one(new_record)
                return jsonify({"message": "success"})
            else:
                return jsonify({"message": "Invalid field values"})
        else:
            return jsonify({"message": "Missing required fields"})
    def put(self, id):
        new = request.get_json()
        for key in new:
            if not key in self.ALLOWED_KEYS:
                return jsonify({"message":"Invalid fields found"})
            if key == "email":
                if not self.get_email(new[key]):
                    return jsonify({"message":"Invalid email id"})
            elif key == "phone":
                if not self.get_phone(new[key]):
                    return jsonify({"message":"Invalid phone number"})
            elif key == "dob":
                if not self.get_dob(new[key]):
                    return jsonify({"message":"Invalid dob"})
            elif key == "firstname":
                if not new[key]:
                    return jsonify({"message":"Invalid firstname"})
            else:
                if not new[key]:
                    return jsonify({"message":"Invalid lastname"})

        query = {"_id":ObjectId(id)} 
        update_query = {"$set":new}
        self.collection.update_many(query,update_query)
        return jsonify({"message":"successful update"})

    def delete(self, id):
        query = {"_id":ObjectId(id)}
        self.collection.delete_many(query)
        return jsonify({"message":"record deleted"})

# Add the view to the users blueprint
api.add_resource(UsersView, '/users', '/users/<id>')
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)