from database.models import Album, db
from typing import Dict, Any, Optional
from datetime import datetime
from flask import jsonify
import json


def add_album():
    return ""


def get_album(album_id: int) -> dict:
    album_query = Album.query

    if album_id:
        album_query = album_query.filter_by(id=album_id, valid='1')

    album = album_query.first()

    # 根据查询结果返回相应的值
    if album:
        return {
            "album_id": album.id,
            "user_id": album.user_id,
            "theme_id": album.theme_id,
            "album_name": album.album_name,
            "protagonist_id": album.protagonist_id,
            "content": album.content,
            "created_at": album.created_at,
            "updated_at": album.updated_at,
            "valid": album.valid
        }
    else:
        return {}


def edit_album(album_id: int, user_id: Optional[int] = None, theme_id: Optional[int] = None,
               album_name: Optional[str] = None,
               protagonist_id: Optional[int] = None,
               content: Optional[str] = None,
               valid: Optional[bool] = None) -> Dict[str, Any]:

    album = Album.query.get(album_id)
    ex_content = json.loads(album.content)
    new_content = []
    new_content.append(json.loads(content))
    combined_list = ex_content + new_content
    combined_string = json.dumps(combined_list, ensure_ascii=False)
    # print(combined_string)

    if album is None:
        raise ValueError(f"No album found with ID {album_id}")

    if user_id is not None:
        album.user_id = user_id
    if theme_id is not None:
        album.theme_id = theme_id
    if album_name is not None:
        album.album_name = album_name
    if protagonist_id is not None:
        album.protagonist_id = protagonist_id
    if content is not None:
        album.content = combined_string
    if valid is not None:
        album.valid = valid

    album.updated_at = datetime.utcnow()  # update the updated_at timestamp

    try:
        db.session.commit()

        # Return the updated album details
        return {
            'id': album.id,
            'user_id': album.user_id,
            'theme_id': album.theme_id,
            'album_name': album.album_name,
            'protagonist_id': album.protagonist_id,
            'content': album.content,
            'created_at': album.created_at,
            'updated_at': album.updated_at,
            'valid': album.valid
        }
    except Exception as e:
        db.session.rollback()
        raise e


def del_album():
    return ''
