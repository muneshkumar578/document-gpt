import json
import logging
import os
from fastapi import File, UploadFile
from openai import AsyncOpenAI
from ..managers.document_thread_manager import DocumentThreadManager

class DocumentGPTService:
    def __init__(self, client: AsyncOpenAI, assistant_id: str):
        self.client = client
        self.assistant_id = assistant_id
        self.document_thread_manager = None

    async def prepare_thread_async(self, thread_id=None, initialize_thread=True):
        self.document_thread_manager = DocumentThreadManager(client=self.client, assistant_id=self.assistant_id)
        if initialize_thread:
            await self.document_thread_manager.get_thread_async(thread_id)

    async def process_query_async(self, message, thread_id=None):
        try:
            await self.prepare_thread_async(thread_id)
            thread = self.document_thread_manager.thread
            
            thread_id = thread.id

            _ = await self.document_thread_manager.add_message_to_thread_async(role="user", content=message)

            async for event in self.document_thread_manager.get_thread_stream_async():
                if event.event == "thread.message.completed":
                    yield f'data: {json.dumps({"content": event.data.content[0].text, "thread_id": thread.id, "last_message": True })}\n\n'
                elif event.event == "thread.message.delta":
                    yield f'data: {json.dumps({"content": event.data.delta.content[0].text.value, "thread_id": thread.id, "last_message": False })}\n\n'
            
        except Exception as e:
            logging.error(f"An error occurred while processing query: {e}")
            raise e
        
    async def messages_list_async(self, thread_id):
        try:
            await self.prepare_thread_async(thread_id)
            return await self.document_thread_manager.messages_list_async()
        except Exception as e:
            logging.error(f"An error occurred while listing messages: {e}")
            return []
        
    async def upload_new_document_async(self, file: UploadFile = File(...)):
        try:
            documents_path = os.environ.get("DOCUMENTS_PATH")

            # Save the file in the documents directory
            file_path = os.path.join(documents_path, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            logging.error(f"An error occurred while uploading document: {e}")