import json
import logging
import os
from openai import AsyncOpenAI
from openai.types.beta import Assistant
from ..managers.document_upload_manager import DocumentUploadManager

class DocumentAssistantManager:
    def __init__(self, update_assistant_flag=False):
        self.update_assistant_flag = update_assistant_flag
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.config_path = os.environ.get("CONFIG_PATH")
        self.files_path = os.environ.get("DOCUMENTS_PATH")
        self.document_upload_manager: DocumentUploadManager = DocumentUploadManager(self.client)
        self.assistant: Assistant = None
        self.thread = None
        self.run = None
        self.vector_store = "Documents GPT VS"

        logging.info("Initializing Document Assistant")
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
            logging.info("Configuration loaded successfully")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")

    async def prepare_assistant_async(self):
        assistant_id = self.config.get('assistant_id')

        if assistant_id:
            logging.info(f"Assistant ID found in config: {assistant_id}")

            if self.update_assistant_flag:
                logging.info("Updating assistant as per flag")
                await self.update_async(on_assistant_updated=self.update_config)
            else:
                await self.retrieve_async(assistant_id=assistant_id)

            if not self.assistant:
                logging.warning("No assistant found with the provided ID, creating a new one...")
                await self.create_async(on_assistant_created=self.update_config)

        else:
            logging.info("No assistant ID found in config, creating a new assistant")
            await self.create_async(on_assistant_created=self.update_config)

    async def create_async(self, on_assistant_created=None):
        try:

            file_ids = await self.document_upload_manager.upload_files_from_dir_async(self.files_path)

            vector_store = await self.client.beta.vector_stores.create(name=self.vector_store, file_ids=file_ids)

            assistant_config = {
                "name": self.config.get('name', None),
                "instructions": self.config.get('instructions', None),
                "tools": self.config.get('tools', None),
                "model": self.config.get('model', None),
                "tool_resources": self.config.get('tool_resources', None),
            }
            assistant_config["tool_resources"]["file_search"]["vector_store_ids"] = [vector_store.id]


            # Filter out None values
            assistant_config = {k: v for k, v in assistant_config.items() if v is not None}
            self.assistant = await self.client.beta.assistants.create(**assistant_config)
            logging.info(f"Assistant created successfully: {self.assistant.id}")

            if callable(on_assistant_created):
                on_assistant_created()
        except Exception as e:
            logging.error(f"Error creating assistant: {e}")
            self.assistant = None

    async def update_async(self, on_assistant_updated=None):
        try:
            file_ids = await self.document_upload_manager.upload_files_from_dir_async(self.files_path)

            assistant_config = {
                "assistant_id": self.config.get('assistant_id', None),
                "name": self.config.get('name', None),
                "instructions": self.config.get('instructions', None),
                "tools": self.config.get('tools', None),
                "model": self.config.get('model', None),
                "tool_resources": self.config.get('tool_resources', None),
            }

            # delete existing vector stores
            if assistant_config["tool_resources"]["file_search"]["vector_store_ids"]:
                for vector_store_id in assistant_config["tool_resources"]["file_search"]["vector_store_ids"]:
                    await self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
            
            print(f'file_ids: {file_ids}')
            vector_store = await self.client.beta.vector_stores.create(name=self.vector_store, file_ids=file_ids)
            assistant_config["tool_resources"]["file_search"]["vector_store_ids"] = [vector_store.id]

            # Filter out None values
            assistant_config = {k: v for k, v in assistant_config.items() if v is not None}
            self.assistant = await self.client.beta.assistants.update(**assistant_config)

            logging.info(f"Assistant updated successfully: {self.assistant.id}")

            if callable(on_assistant_updated):
                on_assistant_updated()
        except Exception as e:
            logging.error(f"Error updating assistant: {e}")
            return None
        
    async def retrieve_async(self, assistant_id):
        try:
            self.assistant = await self.client.beta.assistants.retrieve(assistant_id)
            logging.info(f"Retrieved assistant: {self.assistant.id}")
        except Exception as e:
            logging.error(f"Error retrieving assistant: {e}")
            self.assistant = None

    def update_config(self):
        if self.assistant:
            try:
                self.config['assistant_id'] = self.assistant.id
                self.config['tool_resources']['file_search']['vector_store_ids'] = self.assistant.tool_resources.file_search.vector_store_ids

                with open(self.config_path, 'w') as file:
                    json.dump(self.config, file, indent=4)

                logging.info(f"Configuration updated successfully with assistant ID: {self.assistant.id}")
            except Exception as e:
                logging.error(f"Error updating configuration: {e}")