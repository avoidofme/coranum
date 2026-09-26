from random import randint

from fastapi import FastAPI

app = FastAPI()


limit = 8

col = {}
for i in range(1 << limit):
    col.update({i: 0})


@app.get("/")
async def get_root():
    return "Hellow orld"


@app.get("/api")
async def get_api():
    return "HEllow api"


@app.get("/api/v1")
async def get_v1():
    return "Hellow v1"


@app.get("/roll")
async def get_roll():
    n = randint(1, 1 << limit) - 1
    e = col.get(n)
    if e:
        col.update({n: e + 1})
    else:
        col.update({n: 1})
    return {
        "rolled": bin(n)[2:].ljust(limit, "0"),
        "number": n,
        "limit": (1 << limit) - 1,
        "col": col,
    }
