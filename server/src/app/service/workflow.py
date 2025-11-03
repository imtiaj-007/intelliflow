import math
from typing import Optional
from uuid import UUID

from app.repository.file import FileRepository
from app.repository.workflow import WorkflowRepository
from app.schema.workflow_dto import PaginatedWorkflows, WorkflowCreate, WorkflowRead
from app.utils.logger import log


class WorkflowService:
    """Service class for handling workflow operations.

    This class provides a high-level interface for workflow-related operations, coordinating between
    the workflow repository for data persistence and file repository for document management.

    Attributes:
        workflow_repo (WorkflowRepository): Repository instance for workflow-related database operations
        file_repo (FileRepository): Repository instance for file-related database operations
    """

    def __init__(self, workflow_repository: WorkflowRepository, file_repository: FileRepository):
        """Initialize the WorkflowService with required dependencies.

        Args:
            workflow_repository (WorkflowRepository): Repository instance for workflow database operations
            file_repository (FileRepository): Repository instance for file database operations
        """
        self.workflow_repo = workflow_repository
        self.file_repo = file_repository

    async def create_workflow(
        self,
        user_id: str | UUID,
        title: Optional[str],
        description: Optional[str],
    ) -> Optional[WorkflowRead]:
        """Create a new workflow and associate documents with it.

        This method creates a workflow record and updates the specified documents to reference
        the newly created workflow.

        Args:
            user_id (str | UUID): The user ID creating the workflow (can be string or UUID)
            title (Optional[str]): Optional title/name for the workflow
            description (Optional[str]): Optional description for the workflow

        Returns:
            Optional[WorkflowRead]: The created workflow data if successful, None if creation failed

        Raises:
            Exception: If workflow creation fails in the repository
        """
        try:
            user_id = UUID(user_id) if isinstance(user_id, str) else user_id
            workflow_data = WorkflowCreate(
                user_id=user_id,
                name=title,
                description=description,
            )
            workflow = await self.workflow_repo.create(workflow_data)
            if workflow is None:
                raise Exception("Failed to create workflow")

            return WorkflowRead(
                id=workflow.id,
                user_id=workflow.user_id,
                name=workflow.name,
                description=workflow.description,
                is_active=workflow.is_active,
                created_at=workflow.created_at,
                updated_at=workflow.updated_at,
            )
        except Exception as e:
            log.error(f"Failed to create workflow: {e}")
            raise

    async def get_user_workflows(
        self, user_id: UUID, page: int = 1, limit: int = 20
    ) -> Optional[PaginatedWorkflows]:
        """Retrieve paginated workflows for a specific user.

        Args:
            user_id (UUID): The UUID of the user whose workflows to retrieve
            page (int): The page number for pagination (default: 1)
            limit (int): The number of records per page (default: 20)

        Returns:
            Optional[PaginatedWorkflows]: Paginated response containing workflows and pagination metadata,
                or None if an error occurs

        Note:
            Returns empty paginated response with zero records if no workflows are found
        """
        try:
            workflow_result = await self.workflow_repo.get_user_workflows(
                user_id=user_id, page=page, limit=limit
            )
            workflows, total_records = [], 0

            if workflow_result:
                user_workflows, total_records = workflow_result
                workflows = [
                    WorkflowRead(
                        id=workflow.id,
                        user_id=workflow.user_id,
                        name=workflow.name,
                        description=workflow.description,
                        is_active=workflow.is_active,
                        created_at=workflow.created_at,
                        updated_at=workflow.updated_at,
                    )
                    for workflow in user_workflows
                ]

            return PaginatedWorkflows(
                data=workflows,
                current_page=page,
                total_pages=math.ceil(total_records / limit) if total_records > 0 else 0,
                total_records=total_records,
            )

        except Exception as e:
            log.error(f"Failed to get workflows for user [{user_id}]: {e}")
            raise
