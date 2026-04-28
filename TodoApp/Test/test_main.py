from fastapi.testclient import TestClient
from TodoApp.main import app
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}

def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
