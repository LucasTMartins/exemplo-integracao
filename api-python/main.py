from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import db
from routers import users, tickets

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database pool
    await db.connect()
    yield
    # Shutdown: Close the database pool
    await db.disconnect()

app = FastAPI(
    title="Ticket and User Assign API (Python/FastAPI)",
    description="Python API equivalent to the Node.js version to manage users and tickets.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include Routers
app.include_router(users.router)
app.include_router(tickets.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Python API. Visit /docs for documentation."}
