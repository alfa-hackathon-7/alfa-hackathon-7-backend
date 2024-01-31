from typing import Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.task import (
    Education,
    EducationTask,
    Task,
    TaskStatus,
    TaskFile
)


class EducationTaskCRUD(CRUDBase):

    async def remove_all_educations_from_task(self,
                                              task_id,
                                              session: AsyncSession):
        query = delete(EducationTask).where(EducationTask.task_id == task_id)
        await session.execute(query)
        await session.commit()
        return


class TaskCrud(CRUDBase):

    async def patch_task_awaiting_review(
            self,
            task_id: int,
            session: AsyncSession,
    ) -> Optional[Task]:
        task = await task_crud.get(task_id, session=session)
        task.task_status = "AWAITING_REVIEW"
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task

    async def check_task_in_ipr(self,
                                task_id: int,
                                ipr_id: int,
                                session: AsyncSession):
        query = (
            select(Task)
            .where(and_(Task.id == task_id, Task.ipr_id == ipr_id))
        )
        result = await session.execute(query)
        result = result.scalar()
        return result


task_crud = TaskCrud(Task)
file_crud = CRUDBase(TaskFile)
task_status_crud = CRUDBase(TaskStatus)
education_task_crud = EducationTaskCRUD(EducationTask)
education_crud = CRUDBase(Education)
