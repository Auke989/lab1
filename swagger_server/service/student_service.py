import uuid
from functools import reduce

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
    student_dict["student_id"] = str(uuid.uuid4())
    res = mycol.insert_one(student_dict)
    print("-============================================")
    print(student_dict["student_id"])
    print(res)
    print("-============================================")
    return student_dict["student_id"]


def get_by_id(student_id=None, subject=None):
    if not student_id:
        return "bad request", 400
    student = mycol.find_one({"_id": student_id})
    if not student:
        return "not found", 404
    student["student_id"] = str(student["_id"])
    print(student)
    return student


def delete(student_id=None):
    if not student_id:
        return "bad request", 400
    result = mycol.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        return "not found", 404

    return {"message": "Student deleted", "student_id": str(student_id)}