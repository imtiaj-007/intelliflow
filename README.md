# IntelliFlow - No-Code AI Workflow Builder

## 🚀 Introduction

IntelliFlow is a powerful no-code/low-code platform that enables users to visually create and interact with intelligent AI workflows. Build custom AI pipelines by dragging and dropping components, upload documents for contextual knowledge, and chat with your AI assistant through beautifully designed interfaces.

## 🛠️ Tech Stack

### Frontend
- **React.js** with TypeScript
- **React Flow** for visual workflow builder
- **ShadCN/UI** for beautiful components
- **Tailwind CSS** for styling
- **React Hook Form** with Zod validation

### Backend
- **FastAPI** with Python 3.11
- **PostgreSQL** for data persistence
- **SQLAlchemy 2.0** with async support
- **LangChain** for AI orchestration

### AI & Storage
- **Google Gemini** & **OpenAI GPT** for LLMs
- **ChromaDB** for vector embeddings
- **AWS S3** for file storage
- **SerpAPI/Brave** for web search

### Deployment
- **Docker** with Docker Compose
- **Nginx** for production serving
- **Multi-stage builds** for optimization

## ✨ Features

### 🎯 Visual Workflow Builder
- Drag-and-drop interface with React Flow
- Four core components: User Query, KnowledgeBase, LLM Engine, Output
- Real-time workflow validation
- Canvas with zoom, pan, and connection management

### 📚 Knowledge Base
- PDF document upload and processing
- Automatic text extraction and chunking
- Vector embeddings with semantic search
- Context-aware AI responses

### 💬 Intelligent Chat
- Beautiful markdown chat interface
- Streaming responses for real-time experience
- Follow-up questions with workflow context
- Session management and history

### 🔧 Production Ready
- Comprehensive error handling
- Authentication & authorization
- Containerized deployment
- Health checks and monitoring

## 🏗️ Architecture

### 1. Embedding Process

- **Document Pipeline**: S3 upload → PyMuPDF text extraction → LangChain text splitting → Gemini embeddings → ChromaDB vector storage
- **Metadata Tracking**: PostgreSQL stores file metadata, chunk information, and ChromaDB references for efficient retrieval
- **Async Processing**: Non-blocking file processing with status tracking and error handling

![Document Processing Pipeline](/web/public/doc-processing.png)

### 2. Chat Orchestration  
- **Workflow Execution**: User query → KnowledgeBase semantic search → LLM Engine with context → Streaming response output
- **Context Management**: Dynamic prompt building with document context, web search results, and conversation history
- **Multi-Provider Support**: Configurable AI providers (Gemini, OpenAI) with fallback strategies

![Chat Orchestration Pipeline](/web/public/query-processing.png)

### 3. Database Design
- **Relational Core**: PostgreSQL with UUID primary keys, proper indexing, and cascade relationships
- **JSON Flexibility**: Workflow configurations, node positions, and metadata stored as JSON for schema evolution
- **Separation of Concerns**: Vector data in ChromaDB, relational data in PostgreSQL, file storage in S3

![Database Design](/web/public/db-architecture.png)

### Core Components
1. **User Management** - Authentication and session handling
2. **Workflow Engine** - Visual builder and execution orchestration
3. **Knowledge Base** - Document processing and vector search
4. **Chat Service** - AI response generation with context
5. **File Service** - Cloud storage and processing pipeline

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- AWS account (for S3 storage)
- Google AI API key (for Gemini)
- OpenAI API key (optional)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/imtiaj-007/intelliflow.git
   cd intelliflow
   ```

2. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**

   Frontend: http://localhost:3000
   Backend API: http://localhost:8000
   API Docs: http://localhost:8000/docs

## 📚 Usage Guide

1. Create a Workflow

  - Drag components from sidebar to canvas
  - Connect User Query → KnowledgeBase → LLM Engine → Output
  - Configure each node with models and settings

2. Upload Documents

  - Click KnowledgeBase node to upload PDFs
  - Documents are automatically processed and embedded

3. Chat with Your AI

  - Click "Chat with Stack" to open chat interface
  - Ask questions that use your workflow logic
  - Get contextual responses from your documents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<p align='center'>Built with ❤️ for the AI/ML community</p>