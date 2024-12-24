from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException, Body
# Создаем экземпляр приложения FastAPI

app = FastAPI(swagger_ui_parameters={"tryOutEnabled": True}, debug = True)

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users},)

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except:
        raise HTTPException(status_code=404, detail="Task not found")
@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                            description="Введите имя пользователя" )],
                       age: Annotated[int, Path(ge=18, le=76, description="Enter User age"
                                                      )]) -> str:
    if len(users) == 0:
        new_id = 1  # Если список пуст, назначаем ID 1
    else:
        new_id = max(user.id for user in users)+1
    users.append(User(id=new_id, username=username, age=age))
    return f"Пользователь{username}, возраст {age} лет(год) успешно добавлен"
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Введите ID пользователя")],
                      username: Annotated[str, Path(min_length=5, max_length=20,
                                            description="Введите имя пользователя")],
                      age: Annotated[int, Path(ge=18, le=76, description="Enter User age")]) -> str:
      for user in users:
            if user.id == user_id:
                user.age = age
                user.username = username
                return f"Пользователь id № {user_id} изменен на {username},возраст {age} лет(год)"

            raise HTTPException(status_code=404, detail="Пользователь не найден ")

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter User id",
                                                         example=24)] ) -> str:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return f"Пользователь с id {user_id} удален "
    raise HTTPException(status_code=404, detail=f"Пользователь отсутствуетт по id № {user_id} ")

