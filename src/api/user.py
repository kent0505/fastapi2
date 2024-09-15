from fastapi                   import APIRouter, HTTPException, Depends
from pydantic                  import BaseModel
from sqlalchemy.ext.asyncio    import AsyncSession
from typing                    import List
from sqlalchemy                import select
from src.core.models.base      import User
from src.core.models.db_helper import db_helper
from src.core.jwt.jwt_handler  import check_password, signJWT, hash_password, JwtAdmin


router = APIRouter()


class _LoginBody(BaseModel):
    username: str
    password: str
    role:     str
class _AddBody(BaseModel):
    username: str
    password: str
    role:     bool
class _UpdateBody(BaseModel):
    username:     str
    password:     str
    new_username: str
    new_password: str


@router.post("/login")
async def login(body: _LoginBody, db: AsyncSession = Depends(db_helper.get_db)):
    user = await db.scalar(select(User).filter(User.username == body.username))
    if user:
        hashed = check_password(body.password, user.password)
        if hashed and user.username == body.username:
            access_token = signJWT(user.id, body.role)
            print(access_token)
            return {"access_token": access_token}
    raise HTTPException(401, "username or password invalid")


@router.post("/register")
async def register(body: _AddBody, db: AsyncSession = Depends(db_helper.get_db)):
    users: List[User] = await db.scalars(select(User))
    for user in users:
        if user.role == "admin":
            raise HTTPException(409, "admin already exists")
        if body.username == user.username:
            raise HTTPException(409, "this username already exists")
    body.password = hash_password(body.password)
    db.add(User(
        username = body.username, 
        password = body.password, 
    ))
    await db.commit()
    return {"message": "new user added"}


@router.put("/", dependencies=[Depends(JwtAdmin())])
async def update_user(body: _UpdateBody, db: AsyncSession = Depends(db_helper.get_db)):
    user = await db.scalar(select(User).filter(User.username == body.username))
    if user == None:
        raise HTTPException(404, "user not found")
    if body.new_username != "" or body.new_password != "":
        hashed = check_password(body.password, user.password)
        if hashed:
            body.new_password = hash_password(body.new_password)
            user.username = body.new_username
            user.password = body.new_password
            await db.commit()
            return {"message": "user updated"}
        raise HTTPException(401, "username or password invalid")
    raise HTTPException(404, "user not found")


@router.delete("/{id}", dependencies=[Depends(JwtAdmin())])
async def delete_user(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    user = await db.scalar(select(User).filter_by(id=id))
    if user:
        await db.delete(user)
        await db.commit()
        return {"message": "user deleted"}
    raise HTTPException(404, "user not found")