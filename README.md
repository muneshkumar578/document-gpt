# Document-Based GPT System

## Overview

This project implements a document-based GPT system that answers questions based on a collection of internal documents. The system leverages OpenAI's powerful tools, including the GPT model, Vector stores for efficient document indexing and retrieval, and OpenAI Assistants for enhanced interaction capabilities.

### Approach

I chose to use the OpenAI for this implementation due to ease of integration, allowing for rapid development within the given time constraints (i.e. 2 days). This approach prioritizes quick deployment and high-performance results over the alternative of using open-source models, which would require more setup time and infrastructure management.

## Features

- Question answering based on internal document content using OpenAI's GPT model
- Efficient document indexing and retrieval using OpenAI Vector stores
- Interactive and context-aware responses powered by OpenAI Assistants
- Precise answers with links to source documents and specific paragraphs
- REST API for easy integration
- Simple frontend interface for interaction
- Document relevance checking
- Easy updates for new documents
- Implemented guardrails to prevent inappropriate or irrelevant answers

## Project Structure

The project is organized into two main folders:

- `backend/`: Contains the Python FastAPI code for the backend service
- `frontend/`: Contains the frontend application built with HTML/CSS/JavaScript

## Setup

### Prerequisites

- Docker
- Python 3.11

### Docker Setup

1. Clone the repository:
   ```
   git clone https://github.com/muneshkumar578/document-gpt.git
   cd backend
   ```

2. Create a `.env` file in the `backend` folder with the following content:
   ```
   OPENAI_API_KEY={Add your API_Key}
   CONFIG_PATH=data/config.json
   DOCUMENTS_PATH=data/documents
   ```
   Replace `{Add your API_Key}` with your actual OpenAI API key.

3. Build the Docker image:
   ```  
   docker build -t document-gpt:latest .
   ```

4. Run the Docker container:
   ```
   docker run -p 8000:8000 document-gpt:latest
   ```

### Local Setup

If you prefer to run the application locally:

1. Clone the repository (if not done already):
   ```
   git clone https://github.com/muneshkumar578/document-gpt.git
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv env
   env\Scripts\activate     # On Windows 
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend` folder with the following content:
   ```
   OPENAI_API_KEY={Add your API_Key}
   CONFIG_PATH=data/config.json
   DOCUMENTS_PATH=data/documents
   ```
   Replace `{Add your API_Key}` with your actual OpenAI API key.

4. Run the backend:
   ```
   uvicorn app.main:api --host 127.0.0.1 --port 8000
   ```

## Usage

There are two ways to interact with the application:

1. API: The backend API will be available at `http://localhost:8000`

2. Frontend Application: 
   - Run the frontend/document-gpt-frontend.html file in browser