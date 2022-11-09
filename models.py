from sqlalchemy import Column, Integer, String
from database import Base

# Define To Do class inheriting from Base
class Address(Base):
    #name f the table
    __tablename__ = 'Coordinates_of_the_Address'
    #fields in the table
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    latitude = Column(String(256))
    longitude = Column(String(256))
    country= Column(String(256))
    state= Column(String(256))
    ZipCode= Column(String(256))
