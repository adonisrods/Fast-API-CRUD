from pydantic import BaseModel

# Creating Address Schema (Pydantic Model)
class Address(BaseModel):
    #fields
    name: str
    address: str