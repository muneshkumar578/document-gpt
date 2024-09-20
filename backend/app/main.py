import logging
from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from .managers.document_assistant_manager import DocumentAssistantManager
from .services.document_gpt_service import DocumentGPTService
from .models.query import Query

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


#region - Lifespan Events

@asynccontextmanager
async def lifespan(api: FastAPI):
    # The first part of the function, before the yield, will be executed before the application starts.

    document_assistant = DocumentAssistantManager(update_assistant_flag=True)
    await document_assistant.prepare_assistant_async()
    api.state.document_assistant = document_assistant

    document_gpt_service: DocumentGPTService = DocumentGPTService(client=document_assistant.client,
        assistant_id=document_assistant.assistant.id)
    api.state.document_gpt_service = document_gpt_service



    yield
    # the part after the yield will be executed after the application has finished.

#endregion


api = FastAPI(lifespan=lifespan)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
async def test():
    return {"message": "Document GPT API is running!"}


@api.post("/query")
async def query(query: Query):
    document_gpt_service: DocumentGPTService = api.state.document_gpt_service

    async def get_streamed_response():
        async for event in document_gpt_service.process_query_async(query.query, query.thread_id):
            yield event

    return StreamingResponse(get_streamed_response(), media_type="text/event-stream")


@api.get("/conversation/{thread_id}")
async def get_conversation_messages_by_thread_id(thread_id: str):
    document_gpt_service: DocumentGPTService = api.state.document_gpt_service
    return await document_gpt_service.messages_list_async(thread_id)

@api.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document_gpt_service: DocumentGPTService = api.state.document_gpt_service
    await document_gpt_service.upload_new_document_async(file)

    document_assistant: DocumentAssistantManager = api.state.document_assistant
    await document_assistant.prepare_assistant_async()

    return {"message": "Document uploaded successfully!"}