from flask import Flask,jsonify,request
from bson import ObjectId
from pymongo import MongoClient
import re, datetime

app = Flask(__name__)

ALLOWED_KEYS = ['firstname','lastname','email','phone','dob']

def get_phone(phone_number):
    pattern = r'^\d{10}$'  # Assuming 10-digit phone number format
    if re.match(pattern, phone_number):
        return True
    else:
        return False
    
def get_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def get_dob(dob):
    try:
        datetime.datetime.strptime(dob, '%d %B %Y')  # Assuming YYYY-MM-DD format
        return True
    except ValueError:
        return False
        

@app.route('/users', methods = ['GET','POST'])
def index():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"] 
    collections = db["user"]
    data = []
    if request.method == "GET":
        for i in collections.find():
            i['_id'] = str(i['_id']) 
            data.append(i)
    elif request.method == "POST":
        new_record = request.get_json()
        firstname = new_record['firstname']
        lastname = new_record['lastname']
        email = new_record['email']
        phone = new_record['phone']
        dob = new_record['dob']
        if 'firstname' in new_record and 'lastname' in new_record and 'email' in new_record and 'phone' in new_record and 'dob' in new_record:
            if firstname and lastname and get_email(email) and get_phone(phone) and get_dob(dob):
                collections.insert_one(new_record)
                return jsonify({"message":"successful"})
            else:
                return jsonify({"message":"invalid fields values"})
        else:
            return jsonify({"message":"invalid fields"})
    return jsonify(data)

@app.route('/users/<id>', methods = ['GET','PUT','DELETE'])
def get_put_delete(id):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    collections = db["user"]
    data = []
    if request.method == "GET":
        for i in collections.find({"_id":ObjectId(id)}):
            i['_id'] = str(i['_id'])
            data.append(i)
        return jsonify(data)
    
    elif request.method == "PUT":
        new = request.get_json()
        for key in new:
            if not key in ALLOWED_KEYS:
                return jsonify({"message":"Invalid fields found"})
            if key == "email":
                if not get_email(new[key]):
                    return jsonify({"message":"Invalid email id"})
            elif key == "phone":
                if not get_phone(new[key]):
                    return jsonify({"message":"Invalid phone number"})
            elif key == "dob":
                if not get_dob(new[key]):
                    return jsonify({"message":"Invalid dob"})
            elif key == "firstname":
                if not new[key]:
                    return jsonify({"message":"Invalid firstname"})
            else:
                if not new[key]:
                    return jsonify({"message":"Invalid lastname"})

        query = {"_id":ObjectId(id)} 
        update_query = {"$set":new}
        collections.update_many(query,update_query)
        return jsonify({"message":"successful update"})

            
    elif request.method == "DELETE":
        query = {"_id":ObjectId(id)}
        collections.delete_many(query)
        return jsonify({"message":"record deleted"})
    
app.run(debug=True)