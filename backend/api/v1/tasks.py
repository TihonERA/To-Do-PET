from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from typing import Annotated
from backend.models.user import User
from backend.services.task_service import TaskService
from backend.schemas.task import TaskFilterParams, TaskResponse, TaskCreate, TaskUpdate
from backend.utils.validators import NotFound, AccessDeniedError, ValidationError
from backend.api.deps import get_current_user, get_task_service, get_task_filters
from datetime import datetime

router = APIRouter(tags=["Task"])

@router.get("/tasks", response_model=TaskResponse)
async def get_all_task(
        filters: Annotated[TaskFilterParams, Depends(get_task_filters)],
        current_user: Annotated[User, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ) -> TaskResponse:
    try:
        return await task_service.get_all_task(
                user_id=current_user.user_id,
                skip=filters.skip,
                limit=filters.limit,
                sort_by=filters.sort_by,
                sort_desc=filters.sort_desc,
                status=filters.status,
                priority=filters.priority
            )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
@router.get("/tasks/{tasks_id}", response_model=TaskResponse)
async def get_task(
    tasks_id: Annotated[int, Path()],
    current_user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ) -> TaskResponse:
    try:
        return await task_service.get_task(
            user_id=current_user.user_id,
            task_id=tasks_id
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AccessDeniedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/tasks/create_task", response_model=TaskResponse)
async def create_task(
    data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ) -> TaskResponse:
    try:
        task = await task_service.create_task(
            name=data.name,
            user_id=current_user.user_id,
            description=data.description,
            priority=data.priority,
            due_date=data.due_date
        )
        return task
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
        
@router.patch("/tasks/{task_id}/update_task", response_model=TaskResponse)
async def update_description(
            task_id: Annotated[int, Path(description="ID задачи")],
            task_data: TaskUpdate,
            current_user: Annotated[User, Depends(get_current_user)],
            task_service: Annotated[TaskService, Depends(get_task_service)]
        ) -> TaskResponse:
    try:   
        return await task_service.update_task(
            user_id=current_user.user_id,
            task_id=task_id,
            new_name=task_data.new_name,
            new_description=task_data.new_description,
            new_due_date=task_data.new_due_date,
            set_completed=task_data.set_completed,
            switch_status=task_data.switch_status
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AccessDeniedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
@router.delete("/tasks/{task_id}/delete")
async def delete_task(
    current_user: Annotated[User, Depends(get_current_user)],
    task_id: Annotated[int, Path()],
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ) -> dict:
    try:
        await task_service.delete_task(
            user_id=current_user.user_id,
            task_id=task_id
        )
        return {"detail": "Task deleted"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AccessDeniedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    