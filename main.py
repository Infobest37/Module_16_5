from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException, Body
# Создаем экземпляр приложения FastAPI
app = FastAPI(swagger_ui_parameters={"tryOutEnabled": True}, debug = True) # FastAPI(debug=True): Включает режим
            #swagger_ui_parameters={"tryItOutEnabled": True                # отладки, который выводит более подробные
            # позволяет в swagger не нажимать постоянно Try It Out         # сообщения об ошибках в консоль.

'''Проблемы и ошибки:
Если папка templates отсутствует, TemplateResponse вернет ошибку TemplateNotFound.
Если в указанной директории нет нужного шаблона (например, index.html), произойдет та же ошибка.'''
# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")



# 2. Модель данных Task и хранилище
class Task(BaseModel):
    id: int
    description: str
    is_completed: bool = False

tasks:List[Task] = [
    Task(id=1, description="Изучить FastAPI", is_completed=True),
    Task(id=2, description="Подготовить лекцию по Jinja", is_completed=False),

]
#Описание:
# BaseModel: Используется для проверки типов данных. Pydantic гарантирует, что каждый
# объект в tasks соответствует модели Task.
# is_completed: bool = False: Устанавливает значение по умолчанию, если поле не указ

# 3. Список задач (GET-запрос)
@app.get("/", response_class=HTMLResponse)
async def get_task(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/task/{task_id}", response_class=HTMLResponse)
async def get_task(request: Request, task_id: Annotated[int, Path(ge=1)]):
    for task in tasks:
        if task.id == task_id:
            return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})
    raise HTTPException(status_code=404, detail="Task not found")
@app.post("/task/{description}/{is_completed}", response_class=HTMLResponse)
async def create_task(request: Request, description: Annotated[str, Path(min_length=3, max_length=100)],
is_completed: Annotated[bool, Path()]):
    new_id = max(task.id for task in tasks) + 1 if tasks else 1
    new_task = Task(id=new_id, description=description, is_completed=is_completed)
    tasks.append(new_task)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})
@app.put("/task/{task_id}/{description}/{is_completed}", response_class=HTMLResponse)
async def update_task(request: Request,task_id: Annotated[int, Path(ge=1)],description: Annotated[str, Path(min_length=3, max_length=100)],
is_completed: Annotated[bool, Path()]):
    for task in tasks:
        if task.id == task_id:
            task.description = description
            task.is_completed = is_completed
            return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/task/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: Annotated[int, Path(ge=1)]):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})
    raise HTTPException(status_code=404, detail="Task not found")