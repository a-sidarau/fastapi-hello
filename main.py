import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


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
async def root():
    return {"message": "Hello, world!!!!!!"}


@app.get("/books")
def show_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # Можно создать класс enum и фастапи сможет подтягивать все значения
    # экземпляра данного класса. В доке можно будет увидеть все значения,
    # которые будет принимать функция
    if model_name is ModelName.model_alexnet:  # можно выбирать значения напрямую из класса
        return {"model_name": model_name, "message": "Deep Learning Model alnt"}

    if model_name.value == "lenet":  # можно указывать значение через атрибут value
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


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
    item_id: str, q: str | None = None, short: bool = False
):  # q - пример опционального параметра
    item = {"item_id": item_id}  # short - bool квери-параметр
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Amazing item with very long description"})
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
