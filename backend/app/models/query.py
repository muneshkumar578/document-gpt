from pydantic import BaseModel

class Query(BaseModel):
    query: str
    thread_id: str