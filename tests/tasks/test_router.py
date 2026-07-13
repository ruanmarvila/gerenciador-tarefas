import pytest
from fastapi import status

from tests.tasks.factories import TaskFactory


@pytest.mark.asyncio
async def test_create_task(client, token):
    response = await client.post(
        "/api/v1/tasks/create",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "title": "Test title",
            "description": "Test description"
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "title": "Test title",
        "description": "Test description",
        "status": "todo",
    }

@pytest.mark.asyncio
async def test_list_tasks_should_return_all_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 5
    assert response.json()[0]["status"] == "todo"

@pytest.mark.asyncio
async def test_list_tasks_with_pagination_should_return_paginated_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?offset=1&limit=2",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_list_tasks_filter_title_should_return_filted_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id, title="Task 1"))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?title=Task 1",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_list_tasks_filter_description_should_return_filted_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id, description="description"))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?description=description",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_list_tasks_filter_status_should_return_filted_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?status=todo",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_list_tasks_filter_combined_should_return_filted_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(5, user_id=user.id, title="Test combined", 
                                                description="combined description"))
    await db_session.commit()

    db_session.add_all(TaskFactory.create_batch(2, user_id=user.id, title="other title", 
                                                description="other description"))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?title=Test combined&description=combined description&status=todo",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 5

@pytest.mark.asyncio
async def test_list_task_order_filter_should_return_ordered_tasks(db_session, client, user, token):
    db_session.add_all(TaskFactory.create_batch(3, user_id=user.id))
    await db_session.commit()

    response = await client.get(
        "/api/v1/tasks/list?column=title&order=desc",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 3

    response = await client.get(
        "/api/v1/tasks/list?column=title",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()) == 3

@pytest.mark.asyncio
async def test_list_tasks_when_no_tasks_match_filters_should_return_not_found(client, token):
    response = await client.get(
        "/api/v1/tasks/list?title=Brasil perdeu :(",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_update_task(db_session, client, user, token):
    task = TaskFactory(user_id=user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.patch(
        f"/api/v1/tasks/update/{task.id}",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "title": "Test!"
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Test!"

@pytest.mark.asyncio
async def test_update_task_when_task_not_found(client, token):
    response = await client.patch(
        "/api/v1/tasks/update/200",
        headers = {"Authorization": f"Bearer {token}"},
        json = {},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_update_other_user_task_returns_forbidden(db_session, client, other_user, token):
    task = TaskFactory(user_id=other_user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.patch(
        f"/api/v1/tasks/update/{task.id}",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "title": "Error"
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You don't have authorization for this operation"

@pytest.mark.asyncio
async def test_update_task_status(db_session, client, user, token):
    task = TaskFactory(user_id=user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.patch(
        f"/api/v1/tasks/update/status/{task.id}?status=in_progress",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_update_task_with_invalid_status(db_session, client, user, token):
    task = TaskFactory(user_id=user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.patch(
        f"/api/v1/tasks/update/status/{task.id}?status=unknown",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.asyncio
async def test_update_other_user_status_task(db_session, client, other_user, token):
    task = TaskFactory(user_id=other_user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.patch(
        f"/api/v1/tasks/update/status/{task.id}?status=done",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You don't have authorization for this operation"

@pytest.mark.asyncio
async def test_soft_delete_task(db_session, client, user, token):
    task = TaskFactory(user_id=user.id, title="Test delete", description="Test delete description")

    db_session.add(task)
    await db_session.commit()

    response = await client.delete(
        f"/api/v1/tasks/delete/{task.id}",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": task.id,
        "title": "Test delete",
        "description": "Test delete description",
        "status": "todo",
    }

@pytest.mark.asyncio
async def test_list_deleted_tasks(db_session, client, user, token):
    for _ in range(3):
        task = TaskFactory(user_id=user.id)

        db_session.add(task)
        await db_session.commit()

        response = await client.delete(
            f"/api/v1/tasks/delete/{task.id}",
            headers = {"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK

    response = await client.get(
        "/api/v1/tasks/bin",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3

@pytest.mark.asyncio
async def test_restore_deleted_task(db_session, client, user, token):
    task = TaskFactory(user_id=user.id)

    db_session.add(task)
    await db_session.commit()

    response = await client.delete(
        f"/api/v1/tasks/delete/{task.id}",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    response = await client.patch(
        f"/api/v1/tasks/restore/{task.id}",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_delete_all_deleted_tasks(db_session, client, user, token):
    for _ in range(2):
        task = TaskFactory(user_id=user.id)

        db_session.add(task)
        await db_session.commit()

        response = await client.delete(
            f"/api/v1/tasks/delete/{task.id}",
            headers = {"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_200_OK
    
    response = await client.delete(
        "/api/v1/tasks/delete/bin",
        headers = {"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT