from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
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

# MySQL 환경변수 설정 
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
	# return templates.TemplateResponse("root.html", {"request": request})
    return RedirectResponse(url="/insertuser", status_code=302)



# 사용자 생성

# @app.post("/create")
# async def create_item(request: Request, name: str = Form(...), email: str = Form(...), age: int = Form(...)):
#     mycursor = mydb.cursor()
#     sql = "INSERT INTO items (name, email, age) VALUES (%s, %s, %s)"
#     val = (name, email, age)
#     mycursor.execute(sql, val)
#     mydb.commit()
    # return templates.TemplateResponse("index.html", {"request": request})

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
    # return {"message": "User created successfully"}
    # return templates.TemplateResponse("index.html", {"request": request, "name":name, "email":email, "age":age})
    return templates.TemplateResponse("index.html", {"request": request })

# 모든 사용자 가져오기
@app.get("/users")
async def get_users(request: Request):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()


# 특정 사용자 가져오기
# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     cursor = mydb.cursor(buffered=True)
#     query = "SELECT * FROM users WHERE id=%s"
#     value = (user_id,)
#     cursor.execute(query, value)
#     return cursor.fetchone()

# @app.get("/users/{user_id}",response_class=HTMLResponse)
# async def create_user1(request: Request):
#     return templates.TemplateResponse("user.html", {"request": request })

# @app.get("/users/{user_id}",response_class=HTMLResponse)
# async def get_user(request : Request, user_id: int):
#     cursor = mydb.cursor(buffered=True)
#     query = "SELECT * FROM users WHERE id=%s"
#     value = (user_id,)
#     cursor.execute(query, value)
#     # return cursor.fetchone()
#     return templates.TemplateResponse("user.html", {"request": request ,"id" : id})

@app.get("/users:{user_id}",response_class=HTMLResponse)
async def create_user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

# @app.get("/users:{user_id}", response_class=HTMLResponse)
# async def get_user(request: Request, user_id: int):
#     cursor = mydb.cursor(buffered=True)
#     query = "SELECT * FROM users WHERE id=%s"
#     value = (user_id,)
#     cursor.execute(query, value)
#     user = cursor.fetchone()
#     return templates.TemplateResponse("user.html", {"request": request, "user": user})

# @app.get("/users/{user_id}",response_class=HTMLResponse)
# async def get_user(request: Request, user_id: int):
#     cursor = mydb.cursor(buffered=True)
#     query = "SELECT * FROM users WHERE id=%s"
#     value = (user_id,)
#     cursor.execute(query, value)
#     # return cursor.fetchone()
#     return templates.TemplateResponse("user.html", {"request": request, "user": user})

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



# 사용자 수정




# @app.get("/edituser/{user_id}",response_class=HTMLResponse)
# async def create_user(request: Request):
#     return templates.TemplateResponse("edit.html", {"request": request })

# @app.put("/edituser/{user_id}")
# async def update_user(request : Request, user_id: int,name: str = Form(...),email: str = Form(...), age: int = Form(...)):
#     cursor = mydb.cursor(buffered=True)
#     query = "UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s"
#     values = (name, email, age, user_id)
#     cursor.execute(query, values)
#     mydb.commit()
#     return {"message": "User updated successfully"}
    # return templates.TemplateResponse("edit.html", {"request": request ,"name" : name,"email" : email, "age" : age})
    # return RedirectResponse(url="/users", status_code=302)

# @app.put("/edituser/{user_id}")
# async def update_user(request : Request, user_id: int,name: str = Form(...),email: str = Form(...), age: int = Form(...)):
#     cursor = mydb.cursor(buffered=True)
#     query = "UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s"
#     values = (name, email, age, user_id)
#     cursor.execute(query, values)
#     mydb.commit()
#     return templates.TemplateResponse("edit.html", {"request": request })

    # return {"message": "User updated successfully"}

# 사용자 삭제
@app.delete("/delusers/{user_id}")
async def delete_user(user_id: int):
    cursor = mydb.cursor()
    query = "DELETE FROM users WHERE id=%s"
    value = (user_id,)
    cursor.execute(query, value)
    mydb.commit()
    return {"message": "User deleted successfully"}


# @app.get("/update/{id}")
# async def read_item(request: Request, user_id: int):
#     cursor = mydb.cursor(dictionary=True)
#     query = "SELECT * FROM users WHERE id=%s"
#     value = (user_id,)
#     cursor.execute(query, value)
#     user = cursor.fetchone()
#     return templates.TemplateResponse("update.html", {"request": request, "user": user})

# @app.get("/update")
# async def update_item(request: Request, user_id: int = Form(...), name: str = Form(...),email: str = Form(...), age: int = Form(...)):
#     cursor = mydb.cursor(dictionary=True)
#     query = ("UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s")
#     values = (user_id,name, email, age)
#     cursor.execute(query, values)
#     mydb.commit()
#     # return {"message": "Data updated successfully."}
#     return templates.TemplateResponse("update.html", {"request": request})

@app.get("/update/{user_id}")
async def read_item(request: Request, user_id: int, response_class=HTMLResponse):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return templates.TemplateResponse("update.html", {"request": request, "user": user})

# 밑 코드 실행시 localhost/docs 에서 Object of type 'type' is not JSON serializable 오류 뜸 
@app.post("/update")
async def update_item(request: Request, user_id: int = Form(...), name: str = Form(...), email: str = Form(...), age: int = Form(...)):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("UPDATE users SET name = %s, email = %s ,age = %s WHERE id = %s", (name,email ,age, user_id))
    db.commit()
    return {"message": "Data updated successfully."}



