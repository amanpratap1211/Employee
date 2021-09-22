from config import client
from app import app
from flask import request, jsonify, make_response

db = client.restfulapi
collection = db.users


@app.route("/api/get_all_users")
def get_all_user():
    all_document = collection.find()
    data = []
    for each_record in all_document:
        data.append(each_record)
    if len(data) < 1:
        return make_response("No Data Available", 204)
    return make_response(jsonify(data), 200)


@app.route("/api/get_single_user/<phone>")
def get_single_user(phone):
    all_document = collection.find({"_id": int(phone)})
    data = []
    for each_record in all_document:
        data.append(each_record)
    if len(data):
        return make_response(jsonify(data), 200)
    return make_response("Not Found", 404)


# this function can create single and multiple user
@app.route('/api/create_user', methods=["POST"])
def create():
    records = request.get_json()
    if type(records) is dict:
        records = [records]
    for record in records:
        if "phone" in record:
            record["_id"] = record["phone"]
        else:
            return make_response("phone is a compulsory", 400)
        flag = collection.find({"_id": record["_id"]}).count()
        if flag:
            return make_response("Phone Number already registered", 409)
    collection.insert_many(records)
    return make_response("USER created successfully", 201)


# this function can handle single and multiple updation
@app.route("/api/update_user", methods=["PUT"])
def update_user():
    records = request.get_json()
    if type(records) is dict:
        records = [records]
    for record in records:
        if "phone" in record:
            flag = collection.find({"_id": record["phone"]}).count()
            if flag:
                collection.update({"_id": record["phone"]}, {"$set": record})
            else:
                return make_response("Record Not Found", 404)
        else:
            return make_response("Phone is Compulsory", 404)
    return make_response("Updated Successfully", 200)


# this function can handle single and multiple deletion
@app.route("/api/delete_user", methods=["DELETE"])
def delete_collection():
    records = request.get_json()
    if type(records) is dict:
        records = [records]
    res = 0
    for record in records:
        flag = collection.find(record).count()
        if flag:
            res += flag
            collection.remove(record)
        else:
            return make_response({"error": str(res)+"collection found and Deleted..."}, 404)
    return make_response("Deleted Successfully", 204)
