from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from typing import Annotated
from backend.models.user import User
from backend.models.task import Tasks
from backend.services.task_service import TaskService
from backend.utils.validators import NotFound, AccessDeniedError, ValidationError
from backend.api.deps import get_current_user, get_task_service
from datetime import datetime

router = APIRouter(tags=["Task"])

@router.get("/tasks")
async def get_all_task(
        current_user: Annotated[User, Depends(get_current_user)],
        task_service: Annotated[TaskService, Depends(get_task_service)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=500)] = 100,
        sort_by: Annotated[str, Query()] = "created",
        sort_desc: Annotated[bool, Query()] = True,
        status: Annotated[bool | None, Query()] = None,
        priority: Annotated[int | None, Query(ge=0, le=3)] = None
    ):
    try:
        return await task_service.get_all_task(
                user_id=current_user.user_id,
                skip=skip,
                limit=limit,
                sort_by=sort_by,
                sort_desc=sort_desc,
                status=status,
                priority=priority
            )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
@router.get("/tasks/{tasks_id}")
async def get_task(
    tasks_id: Annotated[int, Path()],
    current_user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    try:
        return await task_service.get_task(
            user_id=current_user.user_id,
            task_id=tasks_id
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AccessDeniedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/tasks/create_task")
async def create_task(
    name: Annotated[str, Body(embed=True)],
    current_user: Annotated[User, Depends(get_current_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    description: Annotated[str | None, Body()] = None,
    priority: Annotated[int | None, Body()] = None,
    due_date: Annotated[datetime | None, Body()] = None
    ):
    try:
        task = await task_service.create_task(
            name=name,
            user_id=current_user.user_id,
            description=description,
            priority=priority,
            due_date=due_date
        )
        return task
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
        
@router.patch("/tasks/{task_id}/update_task")
async def update_description(
            current_user: Annotated[User, Depends(get_current_user)],
            task_service: Annotated[TaskService, Depends(get_task_service)],
            task_id: Annotated[int, Path()],
            new_name: Annotated[str | None, Body()] = None,
            new_description: Annotated[str | None, Body()] = None,
            new_due_date: Annotated[datetime | None, Body()] = None,
            set_completed: Annotated[bool | None, Body()] = None,
            switch_status: Annotated[bool | None, Body()] = None,
        ):
    try:   
        return await task_service.update_task(
            user_id=current_user.user_id,
            task_id=task_id,
            new_name=new_name,
            new_description=new_description,
            new_due_date=new_due_date,
            set_completed=set_completed,
            switch_status=switch_status
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
    task_id: int,
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
    