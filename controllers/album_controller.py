from database.models import Album, db
from typing import Dict, Any, Optional
from datetime import datetime
from flask import jsonify
import json

# 新增绘本
def add_album(user_id: int, protagonist_id: int, theme_id: Optional[int] = None,
              album_name: Optional[str] = None, content: Optional[str] = None) -> int:
    """
    添加新的画册。

    参数:
    - user_id: 用户ID
    - protagonist_id: 主角ID
    - theme_id: 画册主题ID（可选）
    - album_name: 画册名称（可选）
    - content: 画册内容（可选）

    返回:
    - 新画册的ID
    """

    # 创建新画册对象
    new_album = Album(
        user_id=user_id,
        protagonist_id=protagonist_id,
        theme_id=theme_id if theme_id else None,
        album_name=album_name if album_name else '默认画册名',
        content=json.dumps([content]) if content else json.dumps([]),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        valid=True
    )

    # 将新对象添加到数据库会话
    db.session.add(new_album)

    # 提交数据库会话
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return new_album.id


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
