import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    # Создание задачи
    response = client.post("/task", json={"duration": 1})
    assert response.status_code == 200
    task_id = response.json()["task_id"]

    # Ожидание завершения задачи
    asyncio.run(wait_for_task_completion(task_id))

    # Проверка статуса задачи
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "done"}


async def wait_for_task_completion(task_id):
    while True:
        response = client.get(f"/task/{task_id}")
        status = response.json()["status"]
        if status == "done":
            break
        await asyncio.sleep(0.1)
