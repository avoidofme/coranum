from random import randint

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel

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


@app.get("/ops")
async def get_ops():
    return "add, sub, mult, div, mod"


class Ops(SQLModel):
    fnum: int
    snum: int


@app.post("/ops/{op}")
async def get_op(op: str, data: Ops):
    if op in ["div", "mod"] and data.snum == 0:
        raise HTTPException(400, "can't do")
    res = f"Hellow {op}"
    match op:
        case "add":
            res = data.fnum + data.snum
        case "sub":
            res = data.fnum - data.snum
        case "mult":
            res = data.fnum * data.snum
        case "div":
            res = data.fnum // data.snum
        case "mod":
            res = data.fnum % data.snum
        case _:
            raise HTTPException(400, "check /ops")
    return res


@app.get("/trade")
async def get_trade():
    return "Hellow trade"


@app.get("/up")
async def get_up():
    return "HEllow up"
