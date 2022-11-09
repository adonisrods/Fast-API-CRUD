from sqlalchemy import Column, Integer, String
from database import Base

# Define To Do class inheriting from Base
class Address(Base):
    #name f the table
    __tablename__ = 'Coordinates_of_the_Address'
    #fields in the table
    id = Column(Integer, primary_key=True)
    latitude = Column(String(256))
    longitude = Column(String(256))

    distance_upto = Column(String(256))
    Nearbycities= Column(String(256))
