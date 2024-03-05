from orm.models import User, Weather


def create_user(db_session, name, mail, loc, weather):
    db_user = User(name=name, email=mail, location=loc, weather=weather)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def get_all_entities(db_session):
    query_result = db_session.query(User.id, User.name, User.email, User.location,
                                    User.weather, Weather.max_month, Weather.min_month,
                                    Weather.avg_month).join(Weather, User.location == Weather.location).all()

    return query_result


def get_entities_by_mail(db_session, mail):
    filtered_users = db_session.query(User).filter(User.email == mail).all()
    query_results = []

    for user in filtered_users:
        user_weather = db_session.query(Weather).filter(Weather.location == user.location).first()

        if user_weather:
            combined_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "location": user.location,
                "weather": user.weather,
                "max_month": user_weather.max_month,
                "min_month": user_weather.min_month,
                "avg_month": user_weather.avg_month
            }
            query_results.append(combined_data)

    return query_results


def delete_entity_by_id(db_session, id):
    user_to_delete = db_session.query(User).filter(User.id == id).first()

    if user_to_delete:
        db_session.delete(user_to_delete)
        db_session.commit()
        return True
    else:
        return False
