# models here
from pydantic import BaseModel

class request_in(BaseModel):
    args: dict