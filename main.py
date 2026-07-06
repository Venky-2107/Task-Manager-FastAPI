from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, users, tasks
import time

app = FastAPI()
Base.metadata.create_all(bind=engine)

# middleware for CORS -> Cross Origin Resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://task-manager-nnq7qf2fy-venky-2107s-projects.vercel.app", "https://task-manager-app-sable-psi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} - {request.url} -- took -- {process_time:.4f}s")
    return response

# include routers
app.include_router(auth.auth_router)
app.include_router(users.user_router)
app.include_router(tasks.task_router)
