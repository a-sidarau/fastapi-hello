import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# стандартные респонсы  можно менять на кастомные
from fastapi.responses import HTMLResponse # для возврата прямого хтмл

from pydantic import BaseModel
from enum import Enum

from dotenv import load_dotenv

# создаём инстанс фастапи
app = FastAPI()

# загружаем переменные окружения из .env файла
load_dotenv()

# Монтируем папку статичных файлов и создаём сущность для шаблонов Jinja2
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ModelName(str, Enum):
    model_alexnet = "alexnet"
    model_resnet = "resnet"
    model_lenet = "lenet"


class Book(BaseModel):
    id: int
    title: str = "Untitled"
    autor: str = "Unknown"
    genre: str | None = None


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

books = [
    {
        "id": 1,
        "title": "Властелин колец",
        "autor": "Дж. Дж. Р. Толкин",
    },
    {
        "id": 2,
        "title": "Структура и интерпретация компьютерных программ",
        "autor": "Харольд Абельсон",
    },
]


@app.get("/")
async def root(request: Request):
    # словарь контекста, через который можно передать переменные в шаблон
    context = {
        "request": request,
        "title": "Index PAge",
        "cat_name": "Leopold"
    }
    # return templates.TemplateResponse("index.html", {"request": request})
    # в ответ на запрос возвращаем определённый шаблон с переданным контекстом
    return templates.TemplateResponse("index.html", context)

# eсли хотим возвращать хтмл напрямую, нужно подключить специальный класс
@app.get("/books", response_class=HTMLResponse)
def get_books():
    html_content = """
    <html>
        <head>
            <title>Books</title>
        </head>
        <body>
            <h1>Books</h1>
            <p>The list of all indexes from library</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

# >>>> File paths
# чтобы считывать пути из ссылок, нужно после переменной указать
# специальный параметр Starlette :path. ФастАПИ понимает, что значение
# нужно конвертировать в путь
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# >>>> Query параметры
# В ссылке после ? идут квери-параметры и они могут считываться питоном
# и преобразовываться в типы. Далее их можно использоваться в функциях
# http://127.0.0.1:8000/items/?skip=0&limit=10 - пример
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    q: str | None = None,
    short: bool = False
):  # q - пример опционального параметра
    item = {"item_id": item_id}  # short - bool квери-параметр
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Amazing item with very long description"})
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
