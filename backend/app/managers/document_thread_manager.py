import logging
from openai import AsyncOpenAI, AsyncAssistantEventHandler
from openai.types.beta.threads import Message
from openai.types.beta.threads.message import Attachment

class DocumentThreadManager:
    def __init__(self, client: AsyncOpenAI, assistant_id):
        self.client = client
        self.assistant_id = assistant_id
        self.thread = None
        self.run = None

    async def get_thread_async(self, thread_id=None):
        self.thread = await self.client.beta.threads.retrieve(thread_id) if thread_id else await self.client.beta.threads.create()
        return self.thread
    
    async def add_message_to_thread_async(self, role, content):
        message = await self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )
        return message.id
    
    async def get_thread_stream_async(self):
        try:
            async with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
            ) as stream:
                async for result in self.handle_stream_async(stream):
                    yield result
                await stream.until_done()
        except Exception as e:
            logging.error(f"An error occurred while waiting for param: {e}")
            raise e
        
    async def handle_stream_async(self, stream: AsyncAssistantEventHandler):
        try:
            async for event in stream:
                if event.event == 'thread.message.delta' and event.data.delta.content:
                    yield event
                elif event.event == "thread.message.completed":
                    has_annaotation = bool(event.data.content[0].text.annotations)
                    if has_annaotation:
                        event.data.content[0].text = await self.process_annotations_async(event.data)
                        yield event
                elif event.event == 'thread.run.completed':
                    break
                # Handle other events here
        except Exception as e:
            logging.error(f"An error occurred while handling stream: {e}")
            raise e
        
    async def process_annotations_async(self, message: Message):
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        
        # Iterate over the annotations and add footnotes
        for index, annotation in enumerate(annotations):
            # Replace the text with a footnote
            message_content.value = message_content.value.replace(annotation.text, f' [{index+1}]')
        
            # Gather citations based on annotation attributes
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = await self.client.files.retrieve(file_citation.file_id)
                citations.append(f'[{index+1}] {cited_file.filename}')
        
        # Add footnotes to the end of the message before displaying to user
        message_content.value += '\n\n' + '\n\n'.join(citations)
        return message_content.value
    
    async def messages_list_async(self):
        messages_list = []
        messages = await self.client.beta.threads.messages.list(thread_id=self.thread.id)
        for msg in messages.data:
            message = {}
            message["role"] = msg.role
            message["content"] = await self.process_annotations_async(msg)
            messages_list.append(message)  # Add each (role, message) pair to the list
        return messages_list