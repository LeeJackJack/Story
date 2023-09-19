from database.models import AlbumTheme, db
from typing import List, Dict, Any
from sqlalchemy.sql.expression import func


def add_theme(theme, description, preset=None):
    new_theme = AlbumTheme(
        theme=theme,
        description=description,
        preset=preset,
    )
    db.session.add(new_theme)
    db.session.flush()  # 使得新的 Protagonist 对象的 ID 可用
    db.session.commit()

    return {
            'id': new_theme.id,
            'theme': new_theme.theme,
            'description': new_theme.description,
    }


def get_theme(theme_id) -> dict:
    theme = AlbumTheme.query.filter_by(id=theme_id).first()

    return {
        "id": theme.id,
        "description": theme.description,
        "theme": theme.theme,
        "preset": theme.preset,
    }


def get_theme_list() -> List[Dict[str, any]]:
    theme_query = AlbumTheme.query
    theme_query = theme_query.filter_by(valid='1', preset='1')
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
