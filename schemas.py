from pydantic import BaseModel

# Creating Address Schema (Pydantic Model)
class Address(BaseModel):
    #fields
    name: str
    latitude: str
    longitude:str
