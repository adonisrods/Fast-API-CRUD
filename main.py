from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas
from geopy.geocoders import Nominatim
from math import cos, asin, sqrt
values=" "
def distance(lat1, lon1, lat2, lon2,d):
    global values
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2  
    actual_distance= 12742 * asin(sqrt(hav))
    if actual_distance < d:
        temp={"latitude":lat2, "longitude": lon2}
        location= geolocator.reverse(str(temp['latitude'])+","+str(temp['longitude']))
        address = location.raw['address']
        city = address.get('city', '')
        values= str(values) + ", "+ str(city)
        print(values)
    print(12742 * asin(sqrt(hav)))  
    return 12742 * asin(sqrt(hav))


def closest(data, v,d):
    check=min(data, key=lambda p: distance(float(v['lat']), float(v['lon']) , float(p['lat']) , float(p['lon']),float(d)))
    return check

tempDataList = [{'lat': 28.6139, 'lon': 77.2090},  #delhi
                {'lat': 18.5204,  'lon': 73.8567 }, #pune
                {'lat': 12.9716, 'lon': 77.5946}, #bangalore
                {'lat': 15.4909, 'lon': 73.8278}, # panjim goa
                {'lat': 19.0760, 'lon': 72.8777}, #mumbai
                {'lat': 28.4595, 'lon': 77.0266}, #gurugao
                {'lat': 15.2832, 'lon': 73.9862},#margao goa
                {'lat': 28.474388, 'lon': 77.50399}# noida
                ]
# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiProject")

# Create the database
Base.metadata.create_all(engine)
# Initialize app and disabled access information
app = FastAPI()

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
    #locationname = geolocator.geocode(addressbook.CityorState)
    
    d=addressbook.distance_upto
    v = {'lat': addressbook.latitude, 'lon': addressbook.longitude}
    close= closest(tempDataList, v,d)
    addressbookdb = models.Address( latitude= addressbook.latitude, longitude= addressbook.longitude,distance_upto= addressbook.distance_upto , Nearbycities=values)
    
    
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
    location = geolocator.reverse(addressbook.latitude+","+addressbook.longitude)

    address = location.raw['address']
    return address

@app.put("/addressbook/{id}")
def update_addressbook(id: int, latitude:str, longitude:str,distance_upto):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # get the addressbook item with the given id
   
    addressbook = session.query(models.Address).get(id)
    d=addressbook.distance_upto
    v = {'lat':latitude, 'lon': longitude}
    close= closest(tempDataList, v,d)
    # update addressbook item with the given address (if an item with the given id was found)
    if addressbook:
        addressbook.latitude= latitude
        addressbook.longitude= longitude
        addressbook.distance_upto=distance_upto
        addressbook.Nearbycities=values
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

        
        
    return  addressbook_list
