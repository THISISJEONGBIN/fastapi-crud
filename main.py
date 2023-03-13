from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
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

# MySQL 환경변수 설정 후 연결
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password= password,
    database= db
)

# 사용자 모델
class User(BaseModel):
    name: str
    email: str
    age: int


@app.get("/", response_class=HTMLResponse) 
async def root(request: Request): 
	return templates.TemplateResponse("root.html", {"request": request})



# 사용자 생성

# @app.post("/create")
# async def create_item(request: Request, name: str = Form(...), email: str = Form(...), age: int = Form(...)):
#     mycursor = mydb.cursor()
#     sql = "INSERT INTO items (name, email, age) VALUES (%s, %s, %s)"
#     val = (name, email, age)
#     mycursor.execute(sql, val)
#     mydb.commit()
    # return templates.TemplateResponse("index.html", {"request": request})

@app.post("/InsertUser")
async def create_user(request: Request, name: str = Form(...),email: str = Form(...), age: int = Form(...)):
    cursor = mydb.cursor()
    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    values = (name, email, age)
    cursor.execute(query, values)
    mydb.commit()
    # return {"message": "User created successfully"}
    return templates.TemplateResponse("index.html", {"request": request})
    # return templates.TemplateResponse("User_Insert.html", {"request": request })

# 모든 사용자 가져오기
@app.get("/users")
async def get_users():
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()

# 특정 사용자 가져오기
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id=%s"
    value = (user_id,)
    cursor.execute(query, value)
    return cursor.fetchone()

# 사용자 수정
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    cursor = mydb.cursor()
    query = "UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s"
    values = (user.name, user.email, user.age, user_id)
    cursor.execute(query, values)
    mydb.commit()
    return {"message": "User updated successfully"}

# 사용자 삭제
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cursor = mydb.cursor()
    query = "DELETE FROM users WHERE id=%s"
    value = (user_id,)
    cursor.execute(query, value)
    mydb.commit()
    return {"message": "User deleted successfully"}
