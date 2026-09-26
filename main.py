import os
import sys
from collections.abc import Generator
from random import randint

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()

app = FastAPI()

db_path = os.getenv("DATABASE_URL")
if not db_path:
    print("define DATABASE_URL on environment.")
    sys.exit(1)
engine = create_engine(db_path)


class UserBase(SQLModel):
    username: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


limit = 8

col = {}
for i in range(1 << limit):
    col.update({i: 0})

mock_users = [
    {
        "id": 1,
        "username": "nobody",
        "hashed_password": "s0m3c00lpw",
        "collection": col,
    }
]


@app.get("/")
async def get_root():
    return "Hellow orld"


# ======================================
# NOTE: Hellow note, decoration of our code.
# ======================================


@app.get("/api")
async def get_api():
    return "HEllow api"


@app.get("/api/v1")
async def get_v1():
    return "Hellow v1"


# ======================================


@app.get("/users")
async def get_users(session: Session = Depends(get_session)):
    # statement = select(User)
    # users = [x for x in session.exec(statement).all()]
    users = mock_users
    return users


@app.post("/users")
async def post_users():
    pass


@app.get("/user/{id}")
async def get_user(id: int):
    pass


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
async def post_op(op: str, data: Ops):
    if op in ["div", "mod"] and data.snum == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "can't do")
    res = f"Hellow {op}: "
    match op:
        case "add":
            res += str(data.fnum + data.snum)
        case "sub":
            res += str(data.fnum - data.snum)
        case "mult":
            res += str(data.fnum * data.snum)
        case "div":
            res += str(data.fnum // data.snum)
        case "mod":
            res += str(data.fnum % data.snum)
        case _:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "check /ops")
    return res


@app.get("/trade")
async def get_trade():
    return "Hellow trade"


@app.get("/up")
async def get_up():
    return "HEllow up"
