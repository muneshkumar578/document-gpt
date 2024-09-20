# Technical Report: Document-Based GPT System

## 1. Introduction

This report provides an overview of the implemented document-based GPT system, which enables users to ask questions about internal documents and receive precise, well-sourced answers. The system leverages OpenAI's suite of tools to provide responses.

## 2. Approach Comparison

Two main approaches were considered for this project:

### 2.1 OpenAI Ecosystem Approach (Implemented)

- Utilizes OpenAI GPT API for natural language processing
- Employs OpenAI Vector stores for efficient document indexing and retrieval
- Integrates OpenAI Assistants for enhanced interaction capabilities

Pros:
- Rapid development and deployment

Cons:
- Reliance on external API
- Usage costs

### 2.2 Open-Source LLM with Ollama Approach

- Uses open-source language models deployed with Ollama
- Requires custom implementation of document indexing and retrieval

Pros:
- No usage costs

Cons:
- Longer development time
- Requires more resources for deployment and management

The OpenAI Ecosystem Approach was chosen due to time constraints and the desire for required results with minimal setup.

## 3. System Architecture

The system is built using Python FastAPI for the backend and a simple HTML/CSS/JavaScript frontend. It integrates with OpenAI's services for core functionality.

### 3.1 API Endpoints

1. `/query`: Enables users to ask questions about internal documents
2. `/conversation/{thread_id}`: Returns the message history for a specific conversation thread
3. `/upload`: Allows uploading of new internal documents to keep the knowledge base current

A Postman collection is included in the repository for detailed API documentation, as Swagger integration was not completed due to time constraints.

### 3.2 Document Management

The system supports two methods for updating the knowledge base:

1. Using the `/upload` endpoint to add new documents dynamically
2. Updating the document directory and rerunning the application to refresh the knowledge base

## 4. Testing

A test setup has been implemented to verify the system's behavior. Additional tests can be added to increase coverage and robustness.

To run the tests:

```
cd backend
pytest tests/
```

## 5. Future Improvements

Several areas have been identified for future enhancement:

1. Authentication: Implement user authentication to secure the API
2. Document Management: Add support for deleting existing internal documents
3. Conversation Management: Implement functionality to delete conversation threads
4. API Documentation: Complete Swagger integration for improved API discoverability
6. User Interface: Develop a more sophisticated frontend for improved user experience

## 6. Conclusion

The implemented document-based GPT system provides a solid foundation for querying internal documents using advanced AI technologies. While there are areas for improvement, the current implementation meets the core requirements and can be easily extended for future enhancements.
