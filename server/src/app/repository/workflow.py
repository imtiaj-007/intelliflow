import uuid
from typing import Optional, Sequence, Tuple

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.workflow import Workflow
from app.schema.workflow_dto import WorkflowCreate
from app.utils.logger import log


class WorkflowRepository:
    """
    Repository class for handling database operations related to workflows.

    This class provides CRUD operations for the Workflow model using SQLAlchemy
    with async database sessions.

    Attributes:
        session (AsyncSession): The async database session used for all operations
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the WorkflowRepository with a database session.

        Args:
            db_session (AsyncSession): The async database session to use for operations
        """
        self.session = db_session

    async def create(self, workflow_data: WorkflowCreate) -> Optional[Workflow]:
        """
        Create a new workflow record in the database.

        Args:
            workflow_data (WorkflowCreate): The WorkflowCreate object to create

        Returns:
            Optional[Workflow]: The created Workflow object if successful, None if error occurs

        Raises:
            SQLAlchemyError: If there's a database error during the operation
            Exception: If any other unexpected error occurs during the operation
        """
        try:
            workflow = Workflow(**workflow_data.model_dump())
            self.session.add(workflow)
            await self.session.commit()
            await self.session.refresh(workflow)
            return workflow

        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error creating workflow: {e}")
            raise

        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error creating workflow: {e}")
            raise

    async def get_user_workflows(
        self, user_id: uuid.UUID, page: int = 1, limit: int = 20
    ) -> Tuple[Sequence[Workflow], int]:
        """
        Retrieve paginated workflows belonging to a specific user.

        Args:
            user_id (uuid.UUID): The UUID of the user whose workflows to retrieve
            page (int): The page number for pagination (default: 1)
            limit (int): The number of records per page (default: 20)

        Returns:
            Tuple[Sequence[Workflow], int]: A tuple containing:
                - Sequence of Workflow objects for the requested page
                - Total number of records across all pages

        Raises:
            SQLAlchemyError: If there's a database error during the operation
            Exception: If any other unexpected error occurs during the operation
        """
        try:
            q1 = select(func.count()).select_from(Workflow).where(Workflow.user_id == user_id)
            count_result = await self.session.execute(q1)
            total_records = count_result.scalar()

            if total_records is None or total_records == 0:
                return ([], 0)

            skip = (page - 1) * limit
            if skip >= total_records:
                return ([], total_records)

            q2 = (
                select(Workflow)
                .where(Workflow.user_id == user_id)
                .order_by(Workflow.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(q2)
            workflows = result.scalars().all()
            return workflows, total_records

        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error getting workflows: {e}")
            raise

        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error getting workflows: {e}")
            raise
