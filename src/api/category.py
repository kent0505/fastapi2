from fastapi                   import APIRouter, HTTPException, Depends
from pydantic                  import BaseModel
from sqlalchemy.ext.asyncio    import AsyncSession
from typing                    import List
from sqlalchemy                import select
from src.core.models.base      import Category
from src.core.models.db_helper import db_helper


router = APIRouter()


class _AddBody(BaseModel):
    title: str
class _UpdateBody(BaseModel):
    id:    int
    title: str


@router.get("/")
async def get_categories(db: AsyncSession = Depends(db_helper.get_db)):
    data = []
    categories: List[Category] = await db.scalars(select(Category))
    for category in categories:
        data.append({
            "id":    category.id,
            "title": category.title,
        })
    return {"category": data}


@router.post("/")
async def add_category(body: _AddBody, db: AsyncSession = Depends(db_helper.get_db)):
    db.add(Category(
        title = body.title,
    ))
    await db.commit()
    return {"message": "category added"}


@router.put("/")
async def update_category(body: _UpdateBody, db: AsyncSession = Depends(db_helper.get_db)):
    category: Category | None = await db.scalar(select(Category).filter(Category.id == body.id))
    if category:
        category.title = body.title
        await db.commit()
        return {"message": "category updated"}
    raise HTTPException(404, "id not found")


@router.delete("/{id}")
async def delete_category(id: int, db: AsyncSession = Depends(db_helper.get_db)):
    category: Category | None = await db.scalar(select(Category).filter(Category.id == id))
    if category:
        await db.delete(category)
        await db.commit()
        return {"message": "category deleted"}
    raise HTTPException(404, "id not found")