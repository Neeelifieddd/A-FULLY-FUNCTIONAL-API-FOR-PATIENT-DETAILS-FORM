from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json
app = FastAPI()

app=FastAPI()

class Patient(BaseModel):
    
    name:Annotated[Optional[str],Field(default=None)]
    city: Annotated[str, Field(min_length=1)]
    age:Annotated[int, Field(...,gt=0,lt=120,description="The age of the patient")]
    gender:Annotated[Literal['male','female','others'], Field(...,description="The gender of the patient")]
    height:Annotated[float, Field(...,gt=0,description="The height of the patient in metres")]
    weight:Annotated[float, Field(...,gt=0,description="The weight of the patient in kilograms")]
    id:Annotated[Optional[str],Field(default=None)]
    @computed_field
    @property
    def bmi(self) -> float:
        bmi= round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
        
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]

    city: Annotated[Optional[str], Field(default=None)]

    age: Annotated[Optional[int], Field(default=None, gt=0)]

    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]

    height: Annotated[Optional[float], Field(default=None, gt=0)]

    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json', 'r') as f:
        data= json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)
@app.get("/")
def hello():
    return {"message": "PATIENT MANAGEMENT SYSTEM API"}

@app.get('/about')
def about():
    return {"message": "API FOR MANAGING PATIENT RECORDS."}

@app.get('/VIEW')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str=Path(...,description="The ID of the patient to retrieve",example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found.")

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"),
    order: str = Query('asc', description="asc or desc")
):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}"
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort order. Valid orders are: asc, desc"
        )

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x[sort_by],
        reverse=sort_order
    )

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully."}, status_code=201)

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id

    # REMOVE computed fields
    existing_patient_info.pop('bmi', None)
    existing_patient_info.pop('verdict', None)

    patient_pydantic_object = Patient(**existing_patient_info)

    updated_patient_info_dict = patient_pydantic_object.model_dump(exclude=['id'])

    data[patient_id] = updated_patient_info_dict

    save_data(data)

    return JSONResponse(
        content={"message": "Patient updated successfully"},
        status_code=200
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(content={"message": "Patient deleted successfully."}, status_code=200)
    
  
