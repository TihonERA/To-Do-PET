from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class TaskFilterParams(BaseModel):
    skip: int = Field(0, ge=0, description="Пропустить N записей")
    limit: int = Field(100, ge=1, le=500, description="Количество записей на странице")
    
    sort_by: str = Field("created", description="Поле для сортировки")
    sort_desc: bool = Field(True, description="Сортировка по убыванию")
    
    status: Optional[bool] = Field(None, description="Фильтр по статусу (выполнено/нет)")
    priority: Optional[int] = Field(None, ge=0, le=2, description="Фильтр по приоритету (0-3)")

class TaskResponse(BaseModel):
    task_id: int = Field(description="Уникальный ID задачи")
    user_id: UUID = Field(description="ID пользователя, которому принадлежит задача")
    
    name: str = Field(max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    
    priority: int = Field(0, ge=0, le=2, description="Приоритет задачи (0-3)")
    status: bool = Field(False, description="Выполнена ли задача")
    
    created: datetime = Field(..., description="Дата создания задачи")
    completed: Optional[datetime] = Field(None, description="Дата завершения (если выполнена)")
    due_date: Optional[datetime] = Field(None, description="Крайний срок выполнения")

    model_config = {
        "from_attributes": True,  
        "json_schema_extra": {
            "example": {
                "task_id": 1,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Изучить FastAPI",
                "description": "Пройти туториал и написать API",
                "priority": 1,
                "status": False,
                "created": "2023-10-27T10:00:00Z",
                "completed": None,
                "due_date": "2023-11-01T00:00:00Z"
            }
        }
    }

class TaskCreate(BaseModel):
    name: str = Field(max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, max_length=500, description="Описание задачи")
    priority: int = Field(0, ge=0, le=3, description="Приоритет (0-3)")
    due_date: Optional[datetime] = Field(None, description="Крайний срок выполнения")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Купить продукты",
                "description": "Молоко, хлеб, яйца",
                "priority": 1,
                "due_date": "2023-12-31T23:59:59Z"
            }
        }
    }

class TaskUpdate(BaseModel):
    new_name: str | None = Field(
        default=None, 
        max_length=255, 
        description="Новое название задачи"
    )
    new_description: str | None = Field(
        default=None, 
        max_length=500, 
        description="Новое описание задачи"
    )
    new_due_date: datetime | None = Field(
        default=None, 
        description="Новый крайний срок"
    )
    set_completed: bool | None = Field(
        default=None, 
        description="Установить статус 'выполнено' (True) или 'не выполнено' (False)"
    )
    switch_status: bool | None = Field(
        default=None, 
        description="Инвертировать текущий статус (если True)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "new_name": "Обновленная задача",
                "new_description": "Описание изменено",
                "set_completed": True,
                "switch_status": False
            }
        }
    }