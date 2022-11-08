from sqlalchemy import Column, Integer, String
from database import Base

# Define To Do class inheriting from Base
class Address(Base):
    #name f the table
    __tablename__ = 'Coordinates_of_the_Address'
    #fields in the table
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    address = Column(String(256))