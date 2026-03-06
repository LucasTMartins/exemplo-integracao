from fastapi import APIRouter, HTTPException, Path
from typing import List
from database import db
import schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate):
    try:
        query = "INSERT INTO user_assign (name, email) VALUES ($1, $2) RETURNING *"
        row = await db.fetchrow(query, user.name, user.email)
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.User])
async def get_users():
    try:
        query = "SELECT * FROM user_assign ORDER BY id ASC"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int = Path(..., title="The ID of the user to get")):
    try:
        query = "SELECT * FROM user_assign WHERE id = $1"
        row = await db.fetchrow(query, user_id)
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user: schemas.UserUpdate, user_id: int = Path(...)):
    try:
        # Fetch existing user to handle partial updates
        query_get = "SELECT * FROM user_assign WHERE id = $1"
        existing = await db.fetchrow(query_get, user_id)
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")
        
        name = user.name if user.name is not None else existing['name']
        email = user.email if user.email is not None else existing['email']

        query_update = "UPDATE user_assign SET name = $1, email = $2 WHERE id = $3 RETURNING *"
        row = await db.fetchrow(query_update, name, email, user_id)
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: int = Path(...)):
    try:
        query = "DELETE FROM user_assign WHERE id = $1 RETURNING *"
        row = await db.fetchrow(query, user_id)
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
