import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from app.api.v1.deps import get_chat_service, get_current_user, get_workflow_service
from app.schema.workflow_dto import PaginatedWorkflows, WorkflowRead, WorkflowRequest
from app.service.chat import ChatService
from app.service.workflow import WorkflowService

router = APIRouter()


@router.post("", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    body: WorkflowRequest,
    current_user: uuid.UUID = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service),
) -> WorkflowRead:
    """
    Create a new workflow and associate documents with it.

    This endpoint creates a workflow record and updates the specified documents to reference
    the newly created workflow.

    Args:
        document_ids (list[str]): List of document IDs to associate with the workflow
        title (Optional[str]): Optional title/name for the workflow
        description (Optional[str]): Optional description for the workflow
        current_user (uuid.UUID): ID of the authenticated user (from dependency)
        workflow_service (WorkflowService): Injected workflow service dependency

    Returns:
        WorkflowRead: The created workflow data

    Raises:
        HTTPException:
            - 400: If document_ids validation fails
            - 500: If workflow creation fails
    """
    try:
        workflow = await workflow_service.create_workflow(
            user_id=current_user, title=body.title, description=body.description
        )
        if workflow is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create workflow",
            )
        return workflow
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create workflow"
        )


@router.get("", response_model=PaginatedWorkflows)
async def get_workflows(
    page: int = Query(1, gt=0, description="Page number (must be greater than 0)"),
    limit: int = Query(20, gt=0, le=100, description="Number of records per page (1-100)"),
    current_user: uuid.UUID = Depends(get_current_user),
    workflow_service: WorkflowService = Depends(get_workflow_service),
) -> PaginatedWorkflows:
    """
    Retrieve paginated workflows for the authenticated user.

    Args:
        page (int): The page number for pagination (default: 1)
        limit (int): The number of records per page (default: 20)
        current_user (uuid.UUID): ID of the authenticated user (from dependency)
        workflow_service (WorkflowService): Injected workflow service dependency

    Returns:
        PaginatedWorkflows: Paginated response containing workflows and pagination metadata

    Raises:
        HTTPException:
            - 400: If pagination parameters are invalid
            - 500: If retrieval fails
    """
    try:
        workflows = await workflow_service.get_user_workflows(
            user_id=current_user, page=page, limit=limit
        )
        if workflows is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve workflows",
            )
        return workflows
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve workflows"
        )


@router.post("/{workflow_id}/chat")
async def chat_with_workflow(
    workflow_id: str,
    body: dict = Body(..., description="The user's query/question"),
    current_user: uuid.UUID = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
) -> str:
    """
    Chat endpoint for querying documents using semantic search and AI response generation.

    Args:
        workflow_id (str): The workflow ID to search within
        query (str): The user's query/question
        current_user (uuid.UUID): ID of the authenticated user (from dependency)
        chat_service (ChatService): Injected chat service dependency

    Returns:
        ChatResponse: AI-generated response based on document context

    Raises:
        HTTPException:
            - 400: If parameters are invalid
            - 500: If chat response generation fails
    """
    try:
        response = await chat_service.chat_with_workflow(body.get("query"), workflow_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate chat response",
            )
        return response

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat response: {str(e)}",
        )
