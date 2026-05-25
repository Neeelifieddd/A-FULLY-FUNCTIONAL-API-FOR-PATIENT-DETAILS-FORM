# A-FULLY-FUNCTIONAL-API-FOR-PATIENT-DETAILS-FORM
It's a fully functional API that can be used toTO CRUD operations on patient details 

Patient Management System API
A simple REST API built using FastAPI and Pydantic for managing patient records with automatic BMI calculation and health verdict generation.

Features
Create new patient records
View all patients
View a single patient by ID
Update patient details
Delete patient records
Sort patients by:
Height
Weight
BMI
Automatic BMI calculation
Automatic health verdict generation

TECH STACKS
Python
FastAPI
Pydantic
JSON File Storage
Uvicorn

Project Structure
FastAPI/│├── main.py├── patients.json└── README.md

Installation
1. Clone the repository
git clone <your-repository-link>cd FastAPI
2. Create virtual environment
python -m venv myenv
3. Activate virtual environment
Windows
myenv\Scripts\activate
Mac/Linux
source myenv/bin/activate

Install Dependencies
pip install fastapi uvicorn pydantic

Run the Server
uvicorn main:app --reload
Server will start at:
http://127.0.0.1:8000
Swagger Documentation:
http://127.0.0.1:8000/docs

API Endpoints

1. Home Route
GET /
Returns welcome message.
Response
{  "message": "PATIENT MANAGEMENT SYSTEM API"}

2. About Route
GET /about
Returns API information.

3. View All Patients
GET /VIEW
Returns all patient records.

4. View Patient By ID
GET /patient/{patient_id}
Example
GET /patient/P004

5. Create Patient
POST /create
Request Body
{  "id": "P011",  "name": "Rahul Gupta",  "city": "Hyderabad",  "age": 33,  "gender": "male",  "height": 1.89,  "weight": 55}
Response
{  "message": "Patient created successfully."}

6. Update Patient
PUT /edit/{patient_id}
Example Request
{  "city": "Kolkata",  "weight": 90}
Response
{  "message": "Patient updated successfully"}

7. Delete Patient
DELETE /delete/{patient_id}
Example
DELETE /delete/P004

8. Sort Patients
GET /sort
Query Parameters
ParameterDescriptionsort_byheight / weight / bmiorderasc / desc
Example
GET /sort?sort_by=bmi&order=desc

BMI Classification
BMI RangeVerdictBelow 18.5Underweight18.5 - 24.9Normal weight25 - 29.9Overweight30 and aboveObesity

Sample Patient JSON
{  "P001": {    "name": "Amit Mehta",    "city": "Mumbai",    "age": 35,    "gender": "male",    "height": 1.75,    "weight": 85,    "bmi": 27.76,    "verdict": "Overweight"  }}

Future Improvements
Database integration (MongoDB/MySQL/PostgreSQL)
Authentication & Authorization
Docker support
Frontend integration
Search functionality
Pagination
Deployment on Render/Railway/AWS

Author
ANKIT RAY
B.Tech CSE Student | FastAPI Beginner Project
