import logging
import os
from typing import Literal, Optional
from fastapi import File, UploadFile
from openai import AsyncOpenAI

PurposeType = Literal["assistants"]

class DocumentUploadManager:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def upload_files_from_dir_async(self, directory, purpose: PurposeType = "assistants"):
        # Check if the directory exists
        if not os.path.isdir(directory):
            logging.error(f"Directory not found: {directory}")
            return []

        logging.info(f"Uploading files from directory: {directory} with purpose: {purpose}")
        uploaded_file_ids = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                filename = os.path.basename(filepath)
                existing_file_id = await self.find_file_id_async(filename)
                if existing_file_id:
                    uploaded_file_ids.append(existing_file_id)
                    continue
                file = open(filepath, "rb")
                file_response = await self.client.files.create(file=(filename, bytes(file.read())), purpose=purpose)
                if file_response is not None:
                    uploaded_file_ids.append(file_response.id)

        logging.info(f"Uploaded {len(uploaded_file_ids)} files from {directory}")
        return uploaded_file_ids

    async def upload_files_async(self, files: Optional[list[UploadFile]] = File(...), purpose: PurposeType = "assistants"):
        uploaded_file_ids = []
        try:
            for file in files:
                existing_file_id = await self.find_file_id_async(file.filename)
                if existing_file_id:
                    logging.info(f"File {file.filename} already exists. Skipping upload.")
                    uploaded_file_ids.append(existing_file_id)
                    continue
                # read file in binary mode
                file_content = file.file.read()
                # convert file content to binary
                file_content = bytes(file_content)
                # upload file to openai
                file_id = await self.client.files.create(file=(file.filename, file_content), purpose=purpose)
                uploaded_file_ids.append(file_id.id)
            return uploaded_file_ids
        except Exception as e:
            logging.error(f"An error occurred while uploading files: {e}")
            raise e
        
    async def find_file_id_async(self, filename):
        response = await self.client.files.list()
        for file in response.data:
            if file.filename == filename:
                logging.info(f"Found file ID for {filename}: {file.id}")
                return file.id
        return None