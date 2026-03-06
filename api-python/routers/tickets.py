from fastapi import APIRouter, HTTPException, Path
from typing import List
from database import db
import schemas

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)

@router.post("/", response_model=schemas.Ticket, status_code=201)
async def create_ticket(ticket: schemas.TicketCreate):
    try:
        query = """
            INSERT INTO ticket (title, description, status, priority, assigned_to) 
            VALUES ($1, $2, COALESCE($3, 'open'), COALESCE($4, 'medium'), $5) 
            RETURNING *
        """
        row = await db.fetchrow(
            query, 
            ticket.title, 
            ticket.description, 
            ticket.status, 
            ticket.priority, 
            ticket.assigned_to
        )
        return dict(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.Ticket])
async def get_tickets():
    try:
        query = "SELECT * FROM ticket ORDER BY id ASC"
        rows = await db.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticket_id}", response_model=schemas.Ticket)
async def get_ticket(ticket_id: int = Path(...)):
    try:
        query = "SELECT * FROM ticket WHERE id = $1"
        row = await db.fetchrow(query, ticket_id)
        if not row:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(ticket: schemas.TicketUpdate, ticket_id: int = Path(...)):
    try:
        query_get = "SELECT * FROM ticket WHERE id = $1"
        existing = await db.fetchrow(query_get, ticket_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Ticket not found")

        title = ticket.title if ticket.title is not None else existing['title']
        description = ticket.description if ticket.description is not None else existing['description']
        status = ticket.status if ticket.status is not None else existing['status']
        priority = ticket.priority if ticket.priority is not None else existing['priority']
        assigned_to = ticket.assigned_to if ticket.assigned_to is not None else existing['assigned_to']

        query_update = """
            UPDATE ticket 
            SET title = $1, description = $2, status = $3, priority = $4, assigned_to = $5, updated_at = NOW()
            WHERE id = $6 RETURNING *
        """
        row = await db.fetchrow(query_update, title, description, status, priority, assigned_to, ticket_id)
        return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int = Path(...)):
    try:
        query = "DELETE FROM ticket WHERE id = $1 RETURNING *"
        row = await db.fetchrow(query, ticket_id)
        if not row:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return {"message": "Ticket deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
