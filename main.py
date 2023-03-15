from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from typing import Optional
import os
import mysql.connector

app = FastAPI()

load_dotenv()
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

templates = Jinja2Templates(directory="templates")

# CORS 설정
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL 환경변수 설정 
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password= password,
    database= db
)

# 사용자 모델
# class User(BaseModel):
#     name: str
#     email: str
#     age: int

# class UserUpdate(BaseModel):
#     name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     age: Optional[int] = None

class UserUpdate(BaseModel):
    name: str
    email: str
    age: int


@app.get("/", response_class=HTMLResponse) 
async def root(request: Request): 
    return RedirectResponse(url="/insertuser", status_code=302)



# 사용자 생성

@app.get("/insertuser",response_class=HTMLResponse)
async def create_user(request: Request):
    return templates.TemplateResponse("index.html", {"request": request })


@app.post("/insertuser", response_class=HTMLResponse)
async def create_user(request: Request, name: str = Form(...),email: str = Form(...), age: int = Form(...)):
    print(f'name: {name}')
    print(f'email: {email}')
    print(f'age: {age}')

    cursor = mydb.cursor()
    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    values = (name, email, age)
    cursor.execute(query, values)
    mydb.commit()
    return templates.TemplateResponse("index.html", {"request": request })

# 모든 사용자 가져오기
@app.get("/users")
async def get_users(request: Request):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()


@app.get("/users:{user_id}",response_class=HTMLResponse)
async def create_user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "user": user})


@app.get("/users/{user_id}")
async def get_user(request: Request, user_id: int):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id=%s"
    value = (user_id,)
    cursor.execute(query, value)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})



@app.get("/update/{id}")
async def update(request: Request, id: int):
    cursor = mydb.cursor()
    select_query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(select_query, (id,))
    result = cursor.fetchone()
    cursor.close()
    return templates.TemplateResponse("update.html", {"request": request, "id": result[0], "name": result[1], "email": result[2], "age": result[3], "user" : user})

@app.post("/update")
async def do_update(request: Request, id: int = Form(...), name: str = Form(...), email: str = Form(...), age: int = Form(...)):
    cursor = mydb.cursor()
    update_query = "UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s"
    cursor.execute(update_query, (name, email, age, id))
    mydb.commit()
    cursor.close()
    return {"message": "Data updated successfully."}


@app.get("/delete/{id}")
async def delete(request: Request, id: int):
    return templates.TemplateResponse("delete.html", {"request": request, "id": id})

@app.post("/delete")
async def do_delete(request: Request, id: int = Form(...)):
    cursor = mydb.cursor()
    delete_query = "DELETE FROM users WHERE id = %s"
    cursor.execute(delete_query, (id,))
    mydb.commit()
    cursor.close()
    return {"message": "Data deleted successfully."}
