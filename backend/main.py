import csv
import sqlite3
from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from orm import models
from orm.db_setup import SessionLocal, engine
from orm.user_db_utils import create_user, get_all_entities, get_entities_by_mail, delete_entity_by_id
from orm.schemas import UserRegister, UserWholeInfo, EntityData
from orm.weather_db_utils import create_weather_by_loc, get_cities
from utils.cities_utils import cities
from utils.weather_retrieve import get_weather, get_month_data

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def create_connection():
    conn = sqlite3.connect('sql_app.db')
    return conn


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=UserWholeInfo)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    weather = get_weather(user.location, datetime.now())
    db_user = create_user(
        db_session=db,
        name=user.name,
        mail=user.email,
        loc=user.location,
        weather=weather,
    )
    return db_user


@app.get('/cities')
async def get_all_cities(db: Session = Depends(get_db)):
    return {"cities": get_cities(db)}


@app.get('/all-entities')
async def get_all_users_weather(db: Session = Depends(get_db)):
    entities = get_all_entities(db)
    users_weather = []

    for user_id, name, email, location, weather, max_month, min_month, avg_month in entities:
        user_weather = EntityData(
            id=user_id,
            name=name,
            email=email,
            location=location,
            weather=weather,
            max_month=max_month,
            min_month=min_month,
            avg_month=avg_month
        )
        users_weather.append(user_weather)
    return users_weather


@app.get('/entities-by-account/{user_mail}')
async def get_all_by_mail(user_mail: str, db: Session = Depends(get_db)):
    filtered_entities = get_entities_by_mail(db_session=db, mail=user_mail)
    return filtered_entities


@app.delete('/delete-entity/{entity_id:int}')
async def delete_row(entity_id, db: Session = Depends(get_db)):
    if successful_deletion := delete_entity_by_id(db, entity_id):
        print(successful_deletion)
        return {'status_code': 203}
    return {'status_code': 405}


@app.post('/new-weather')
def new_weather(db: Session = Depends(get_db)):
    for idx, city in enumerate(cities):
        try:
            location = f"{city['name']}, {city['country_code']}"
            weather = get_weather(location, datetime.now())
            min_month, max_month, avg_month = get_month_data(location, weather)
            db_weather = create_weather_by_loc(db_session=db,
                                               location=location,
                                               weather=weather,
                                               min_m=min_month,
                                               max_m=max_month,
                                               avg_m=avg_month)
        except Exception:
            print('Error')
    return {'message': 'Filled database'}


@app.on_event("startup")
async def startup():
    conn = create_connection()
    cursor = conn.cursor()

    with open('weather_data.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            try:
                cursor.execute(
                    "INSERT INTO weather (id, location, max_month, min_month, avg_month) VALUES (?, ?, ?, ?, ?)"
                    , row)
            except Exception as e:
                print('Failed to fill weather table', e)

    conn.commit()
    conn.close()
