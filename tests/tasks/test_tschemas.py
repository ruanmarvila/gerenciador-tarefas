import pytest
from pydantic_core import ValidationError

from src.tasks.schemas import OrderFilter, Pagination, TaskCreate, TaskFilter, TaskUpdate


def test_create_task_schema():
    task = TaskCreate(
        title="Test",
        description="Test Description"
    )

    assert task.title == "Test"


def test_create_task_schema_with_default_values():
    task = TaskCreate()

    assert task.title == "Title"
    assert task.description == "Description"


def test_update_task_schema():
    updated_task = TaskUpdate(
        title="Update",
        description="Update title and description",
    )

    assert updated_task.title == "Update"


def test_update_task_schema_with_none_default_values():
    update_task = TaskUpdate()

    assert update_task.title is None
    assert update_task.description is None


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate, TaskFilter])
@pytest.mark.parametrize("title, description, status", [
    ("title", "", "todo"),
    ("", "description", "done"),
    ("", "", "")
    ],
)
def test_schemas_reject_empty_field(schema, title, description, status):
    data = {
        "title": title,
        "description": description,
    }

    if schema is TaskFilter:
        data["status"] = status

    with pytest.raises(ValidationError) as exc_info:
        schema(**data)
        
    assert title in str(exc_info.value) or description in str(exc_info.value) or status in str(exc_info.value)
    

def test_pagination_schema():
    pagination = Pagination(
        offset=5,
        limit=15,
    )

    assert pagination.limit == 15


def test_pagination_schema_reject_negative_values():
    with pytest.raises(ValidationError) as exc_info:
        Pagination(
            offset=-2,
            limit=-20,
        )
    
    assert "offset" in str(exc_info.value)
    assert "limit" in str(exc_info.value)


@pytest.mark.parametrize("title, description, status", [
    ("Test", "description test", "done"),
    (None, "test", "todo"),
    ("Title", None, "in_progress"),
    ("Title test", "description", None),
    (None, None, None),
    ]
)
def test_filter_task_schema_allows_none_values(title, description, status):
    task_filter = TaskFilter(
            title=title,
            description=description,
            status=status,
    )

    assert task_filter.title == title
    assert task_filter.description == description
    assert task_filter.status == status


def test_filter_task_schema_status_reject_invalid_values():
    with pytest.raises(ValidationError) as exc_info:
        TaskFilter(
            title="Title",
            description="Description",
            status="finished" # type: ignore
        )
    
    assert "status" in str(exc_info.value)


@pytest.mark.parametrize("column, order", [
    ("title", "asc"),
    ("created_at", "desc"),
    ("updated_at", None),
    (None, None)
    ],
)
def test_order_filter_schema_allows_none_values(column, order):
    order_filter = OrderFilter(
        column=column,
        order=order,
    )

    assert order_filter.column == column
    assert order_filter.order == order


@pytest.mark.parametrize("column, order", [
    ("description", "ascending"),
    ("id", "descending"),
    ]
)
def test_order_filter_schema_reject_invalid_values(column, order):
    with pytest.raises(ValidationError) as exc_info:
        OrderFilter(
            column=column,
            order=order,
        )

    assert column in str(exc_info.value)
    assert order in str(exc_info.value)