from pydantic import BaseModel, Field

class Health_Check(BaseModel):
  version: str = Field(...)
  status: str = Field(...)