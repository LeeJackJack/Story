from database.models import StoryPlot, db
from typing import Optional
from sqlalchemy.sql.expression import func


def add_story_plot():

    return ""


def get_story_plot():
    return ''


def edit_story_plot():
    return ''


def del_story_plot():
    return ''


def get_random_story_plot(chapter, theme_id):
    story_plot = StoryPlot.query.filter_by(chapter=chapter, theme_id=theme_id).order_by(func.random()).first()
    if story_plot:
        return {
            "id": story_plot.id,
            "theme_id": story_plot.theme_id,
            "chapter": story_plot.chapter,
            "description": story_plot.description,
            "created_at": story_plot.created_at,
            "updated_at": story_plot.updated_at,
        }
    else:
        return None

