from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import asyncio

app = FastAPI()


class Task(BaseModel):
    duration: int


tasks = {}


@app.post("/task", response_model=dict)
async def create_task(task: Task):
    task_id = str(uuid.uuid4())
    tasks[task_id] = "running"
    await asyncio.sleep(task.duration)
    tasks[task_id] = "done"
    return {"task_id": task_id}


@app.get("/task/{task_id}", response_model=dict)
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    status = tasks[task_id]
    return {"status": status}
