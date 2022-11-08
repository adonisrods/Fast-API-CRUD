from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas
# Create the database
Base.metadata.create_all(engine)
# Initialize app and disabled access information
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian","syntaxHighlight": False})

#the initial landing page for http://127.0.0.1:8000/
@app.get("/")
def root():
    #asking to redirect
    return " go to http://127.0.0.1:8000/docs"

@app.post("/addressbook", status_code=status.HTTP_201_CREATED)
def create_addressbook(addressbook: schemas.Address):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # create an instance of  database model
    addressbookdb = models.Address(address = addressbook.address, name= addressbook.name)
    # add it to the session and commit it
    session.add(addressbookdb)
    session.commit()
    # grab the id given to the object from the database
    id = addressbookdb.id
    # close the session
    session.close()
    # return the id
    return f"created addressbook item with id {id}"

@app.get("/addressbook/{id}")
def read_addressbook(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get the addressbook item with the given id
    addressbook = session.query(models.Address).get(id)
    # close the session
    session.close()
    # check if addressbook item with given id exists. If not, raise exception and return 404 not found response
    if not addressbook:
        raise HTTPException(status_code=404, detail=f"addressbook item with id {id} not found")

    return addressbook

@app.put("/addressbook/{id}")
def update_addressbook(id: int, address: str, name:str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get the addressbook item with the given id
    addressbook = session.query(models.Address).get(id)
    # update addressbook item with the given address (if an item with the given id was found)
    if addressbook:
        addressbook.addesss = address
        addressbook.name= name
        session.commit()
    # close the session
    session.close()
    # check if addressbook item with given id exists. If not, raise exception and return 404 not found response
    if not addressbook:
        raise HTTPException(status_code=404, detail=f"addressbook item with id {id} not found")
    return addressbook

@app.delete("/addressbook/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_addressbook(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get the addressbook item with the given id
    addressbook = session.query(models.Address).get(id)
    # if addressbook item with given id exists, delete it from the database. Otherwise raise 404 error
    if addressbook:
        session.delete(addressbook)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"addressbook item with id {id} not found")
    return None

# reads entire list 
@app.get("/addressbook")
def read_addressbook_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get all addressbook items
    addressbook_list = session.query(models.Address).all()
    # close the session
    session.close()
    return addressbook_list