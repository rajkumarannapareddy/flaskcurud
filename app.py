from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://rajkumarannapareddy786:Raj630370%40@cluster0.l3xaorl.mongodb.net/")
db = client["college_details"]
students_col = db["Student_details"]
marks_col = db["student_marks"]


if students_col.count_documents({}) == 0:
    student_data = [
        {"Id": 101, "Name": "Ram", "Age": 21, "Branch": "Mech"},
        {"Id": 102, "Name": "Mani", "Age": 23, "Branch": "Cse"},
        {"Id": 103, "Name": "Raj", "Age": 24, "Branch": "Ece"},
        {"Id": 104, "Name": "Kishore", "Age": 25, "Branch": "EEE"},
        {"Id": 105, "Name": "Ravi", "Age": 26, "Branch": "Aeronautical"},
        {"Id": 106, "Name": "shesu", "Age": 21, "Branch": "Civil"},
        {"Id": 107, "Name": "Chaitanya", "Age": 21, "Branch": "ML"},
        {"Id": 108, "Name": "Phani", "Age": 23, "Branch": "Cse"},
        {"Id": 109, "Name": "satish", "Age": 21, "Branch": "Ece"},
    ]
    students_col.insert_many(student_data)

if marks_col.count_documents({}) == 0: 
    marks_data = [
        {"Id": 101, "Marks": 587}, {"Id": 102, "Marks": 487}, {"Id": 103, "Marks": 550},
        {"Id": 104, "Marks": 450}, {"Id": 105, "Marks": 590}, {"Id": 106, "Marks": 501},
        {"Id": 107, "Marks": 560}, {"Id": 108, "Marks": 425}, {"Id": 109, "Marks": 480},
    ]
    marks_col.insert_many(marks_data)

# ------------------- STUDENT API -----------------------

@app.route('/student_details', methods=['GET'])
def get_all_students():
    students = list(students_col.find())
    return dumps(students), 200

@app.route('/student_details/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = students_col.find_one({"Id": student_id})
    return (dumps(student), 200) if student else (jsonify({"error": "Student not found"}), 404)

@app.route('/student_details', methods=['POST'])
def create_student():
    new_data = request.get_json()
    students_col.insert_one(new_data)
    return jsonify({"message": "Student added successfully"}), 201

@app.route('/student_details/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    updated_data = request.get_json()
    result = students_col.update_one({"Id": student_id}, {"$set": updated_data})
    return (jsonify({"message": "Student updated"}), 200) if result.modified_count > 0 else (jsonify({"error": "Not found"}), 404)

@app.route('/student_details/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    result = students_col.delete_one({"Id": student_id})
    return (jsonify({"message": "Deleted"}), 200) if result.deleted_count > 0 else (jsonify({"error": "Not found"}), 404)

# ------------------- MARKS API -----------------------

@app.route('/student_marks', methods=['GET'])
def get_all_marks():
    marks = list(marks_col.find())
    return dumps(marks), 200

@app.route('/student_marks/<int:student_id>', methods=['GET'])
def get_marks_by_id(student_id):
    mark = marks_col.find_one({"Id": student_id})
    return (dumps(mark), 200) if mark else (jsonify({"error": "Mark not found"}), 404)

@app.route('/student_marks', methods=['POST'])
def add_marks():
    new_data = request.get_json()
    marks_col.insert_one(new_data)
    return jsonify({"message": "Marks added"}), 201

@app.route('/student_marks/<int:student_id>', methods=['PUT'])
def update_marks(student_id):
    updated_data = request.get_json()
    result = marks_col.update_one({"Id": student_id}, {"$set": updated_data})
    return (jsonify({"message": "Marks updated"}), 200) if result.modified_count > 0 else (jsonify({"error": "Not found"}), 404)

@app.route('/student_marks/<int:student_id>', methods=['DELETE'])
def delete_marks(student_id):
    result = marks_col.delete_one({"Id": student_id})
    return (jsonify({"message": "Marks deleted"}), 200) if result.deleted_count > 0 else (jsonify({"error": "Not found"}), 404)

# ------------------- JOINED API -----------------------

@app.route('/student_details/full/<int:student_id>', methods=['GET'])
def get_full_student_info(student_id):
    student = students_col.find_one({"Id": student_id})
    marks = marks_col.find_one({"Id": student_id})
    if student:
        full_info = student.copy()
        if marks:
            full_info["Marks"] = marks["Marks"]
        return dumps(full_info), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# Run Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
