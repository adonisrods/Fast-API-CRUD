from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Creating a sqlite engine instance
engine = create_engine("sqlite:///AddressBook.db")

# Creating a DeclarativeMeta instance
Base = declarative_base()