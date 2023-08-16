from database.models import Protagonist, db
from typing import Optional
from sqlalchemy.sql.expression import func


def add_protagonist():

    return ""


def get_protagonist():
    return ''


def edit_protagonist():
    return ''


def del_protagonist():
    return ''


def get_random_protagonist():
    protagonist = Protagonist.query.order_by(func.random()).first()
    if protagonist:
        return {
            "id": protagonist.id,
            "description": protagonist.description,
            "name": protagonist.name,
            "race": protagonist.race,
            "feature": protagonist.feature,
            "created_at": protagonist.created_at,
            "updated_at": protagonist.updated_at,
            "valid": protagonist.valid,
            "image_description": protagonist.image_description
        }
    else:
        return None
