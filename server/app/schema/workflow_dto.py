import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schema.app_dto import PaginatedResponse


class WorkflowRequest(BaseModel):
    title: str | None
    description: str | None


class WorkflowBase(BaseModel):
    id: uuid.UUID = Field(..., description="Unique identifier for the workflow.")
    user_id: uuid.UUID = Field(..., description="ID of the user who owns this workflow.")
    name: str = Field(..., description="Name of the workflow.")
    description: Optional[str] = Field(None, description="Description of the workflow.")
    is_active: bool = Field(..., description="Whether the workflow is active or not.")
    created_at: datetime = Field(..., description="Timestamp when the workflow was created.")
    updated_at: datetime = Field(..., description="Timestamp when the workflow was last updated.")


class WorkflowCreate(BaseModel):
    user_id: uuid.UUID = Field(..., description="ID of the user who owns this workflow.")
    name: str = Field(..., description="Name of the workflow.")
    description: Optional[str] = Field(None, description="Description of the workflow.")
    is_active: bool = Field(True, description="Whether the workflow is active or not.")


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the workflow.")
    description: Optional[str] = Field(None, description="Description of the workflow.")
    is_active: Optional[bool] = Field(None, description="Whether the workflow is active or not.")


class WorkflowRead(WorkflowBase):
    pass


PaginatedWorkflows = PaginatedResponse[WorkflowRead]


class WorkflowNodeBase(BaseModel):
    id: uuid.UUID = Field(..., description="Unique identifier for the workflow node.")
    workflow_id: uuid.UUID = Field(..., description="Workflow this node belongs to.")
    type: str = Field(
        ...,
        description="Type of the node, e.g. 'UserQuery', 'KnowledgeBase', 'LLMEngine', 'Output'.",
    )
    name: Optional[str] = Field(None, description="Optional name/label for the node.")
    position: Optional[Dict[str, Any]] = Field(
        None, description="Canvas position of the node in the frontend workspace."
    )
    config: Optional[Dict[str, Any]] = Field(
        None, description="Configuration settings for the node."
    )
    connections: Optional[List[Dict[str, Any]]] = Field(
        None, description="Connection data for the node."
    )
    created_at: datetime = Field(..., description="Timestamp when the node was created.")
    updated_at: datetime = Field(..., description="Timestamp when the node was last updated.")


class WorkflowNodeCreate(BaseModel):
    workflow_id: uuid.UUID = Field(..., description="Workflow this node belongs to.")
    type: str = Field(
        ...,
        description="Type of the node, e.g. 'UserQuery', 'KnowledgeBase', 'LLMEngine', 'Output'.",
    )
    name: Optional[str] = Field(None, description="Optional name/label for the node.")
    position: Optional[Dict[str, Any]] = Field(
        None, description="Canvas position of the node in the frontend workspace."
    )
    config: Optional[Dict[str, Any]] = Field(
        None, description="Configuration settings for the node."
    )
    connections: Optional[List[Dict[str, Any]]] = Field(
        None, description="Connection data for the node."
    )


class WorkflowNodeUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Optional name/label for the node.")
    position: Optional[Dict[str, Any]] = Field(
        None, description="Canvas position of the node in the frontend workspace."
    )
    config: Optional[Dict[str, Any]] = Field(
        None, description="Configuration settings for the node."
    )
    connections: Optional[List[Dict[str, Any]]] = Field(
        None, description="Connection data for the node."
    )


class WorkflowNodeRead(WorkflowNodeBase):
    pass


class WorkflowWithNodes(WorkflowRead):
    nodes: List[WorkflowNodeRead] = Field(
        ..., description="List of nodes belonging to this workflow."
    )
