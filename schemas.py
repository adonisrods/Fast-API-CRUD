from pydantic import BaseModel

# Creating Address Schema (Pydantic Model)
class Address(BaseModel):
    #fields
    latitude : str
    longitude : str
   
    distance_upto : str
    Nearbycities: str
