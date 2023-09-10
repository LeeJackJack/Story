from database.models import AlbumTheme, db
from typing import List, Dict, Any
from sqlalchemy.sql.expression import func


def add_theme():
    return {}


def get_theme() -> dict:
    return {}


def get_theme_list() -> List[Dict[str, any]]:
    theme_query = AlbumTheme.query
    theme_query = theme_query.filter_by(valid='1')
    themes = theme_query.all()
    theme_list = []
    for theme in themes:
        theme_dict = {
            'id': theme.id,
            'theme': theme.theme,
            'description': theme.description,
        }
        theme_list.append(theme_dict)
    return theme_list
