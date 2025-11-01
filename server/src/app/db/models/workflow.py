import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import ConfigDict
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.file import File
    from app.db.models.user import User


class Workflow(Base):
    """
    Represents a workflow built by the user in the IntelliFlow system.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ddee5c11-1122-3344-5566-778899aabbcc",
                "user_id": "f1234e56-789a-4bcd-8123-d45e67890fab",
                "name": "PDF QA Bot",
                "description": "Workflow that uses document embeddings and GPT for QA.",
                "is_active": True,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T09:30:00Z",
            }
        }
    )

    __tablename__ = "workflows"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the workflow.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.users.id"),
        index=True,
        nullable=False,
        comment="ID of the user who owns this workflow.",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Name of the workflow.")
    description: Mapped[Optional[str]] = mapped_column(
        Text, default=None, nullable=True, comment="Description of the workflow."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="Whether the workflow is active or not."
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the workflow was created.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the workflow was last updated.",
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="workflows")
    nodes: Mapped[List["WorkflowNode"]] = relationship(
        back_populates="workflow", cascade="all, delete-orphan", passive_deletes=True
    )
    files: Mapped[List["File"]] = relationship(
        back_populates="workflow", cascade="all, delete-orphan", passive_deletes=True
    )


class WorkflowNode(Base):
    """
    Represents an individual component/node in a workflow graph.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "7f6d2a44-3b1c-4569-a9b3-9a1b7de7f61d",
                "workflow_id": "ddee5c11-1122-3344-5566-778899aabbcc",
                "type": "LLMEngine",
                "name": "Answer Generator",
                "position": {"x": 350, "y": 200},
                "config": {"model": "gpt-4-turbo", "temperature": 0.7, "use_web_search": False},
                "connections": [{"inputs": ["UserQueryNode"], "outputs": ["OutputNode"]}],
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-02T09:30:00Z",
            }
        }
    )

    __tablename__ = "workflow_nodes"
    __table_args__ = {"schema": "public", "keep_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the workflow node.",
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("public.workflows.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
        comment="Workflow this node belongs to.",
    )
    type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Type of the node, e.g. 'UserQuery', 'KnowledgeBase', 'LLMEngine', 'Output'.",
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255), default=None, nullable=True, comment="Optional name/label for the node."
    )
    position: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        default=None,
        nullable=True,
        comment="Canvas position of the node in the frontend workspace.",
    )
    config: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        default=None,
        nullable=True,
        comment="Configuration options for this node (model, API keys, parameters).",
    )
    connections: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSON,
        default=None,
        nullable=True,
        comment="List of connections between nodes: [{'source': 'node1', 'target': 'node2', 'sourceHandle': 'output', 'targetHandle': 'input'}]",
    )
    execution_order: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Execution sequence order within the workflow.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the node was created.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the node was last updated.",
    )

    # Relationships
    workflow: Mapped["Workflow"] = relationship(back_populates="nodes")
