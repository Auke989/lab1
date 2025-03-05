
from bson import ObjectId

import pymongo

myclient = pymongo.MongoClient("mongo", 27017)
mydb = myclient["students_db"]
mycol = mydb["students"]


def add(student=None):
    if not student:
        return "bad request", 400
    student_dict = {"first_name": student.first_name, "last_name": student.last_name}
    res = mycol.find_one(student_dict)
    if res:
        return 'already exists', 409

    # Generate a UUID if required by Swagger
    res = mycol.insert_one(student.to_dict())
    student.student_id = res.inserted_id
    print(student.student_id)
    return str(student.student_id)


def get_by_id(student_id=None):
    student = mycol.find_one({"_id": ObjectId(student_id)})

    if not student:
        return "not found", 404

    student["_id"] = str(student["_id"])

    return student


def delete(student_id=None):
    student = mycol.find_one({"_id": ObjectId(student_id)})

    if not student:
        return "not found", 404

    student["_id"] = str(student["_id"])

    mycol.delete_one({"_id": ObjectId(student_id)})
    return student