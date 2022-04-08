import random

from typing import Optional
from fastapi import FastAPI
import uvicorn
import names
import requests


ANIMALS = []

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Python Developer"}

@app.get("/random/number")
def random_number():

    value = random.randint(0, 10)

    return {"value": value}


@app.get("/random/animal")
def random_animal():
    global ANIMALS
    if not ANIMALS:
        url = "https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt"
        resp = requests.get(url)
        ANIMALS = resp.text.splitlines()

    value = random.choice(ANIMALS)

    return {"value": value}


@app.get("/random/name")
def random_name():
    return {"value": names.get_full_name()}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
