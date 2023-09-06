# game_controller.py
from database.models import Game, db
from typing import Optional, Dict, Any


def add_game():
    return "User added!"


def get_game(id: int) -> dict:
    game_query = Game.query
    if id:
        game_query = game_query.filter_by(id=id, valid='1')

    game = game_query.first()

    # 根据查询结果返回相应的值
    if game:
        return {
            "id": game.id,
            "user_id": game.user_id,
            "theme_id": game.theme_id,
            "protagonist_id": game.protagonist_id,
            "content": game.content,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
            "valid": game.valid,
            "if_finish": game.if_finish,
            "prompt_history": game.prompt_history,
        }
    else:
        return {}


def edit_game(id: int,
              user_id: Optional[int] = None,
              protagonist_id: Optional[int] = None,
              theme_id: Optional[int] = None,
              content: Optional[str] = None,
              if_finish: Optional[str] = None,
              prompt_history: Optional[str] = None) -> Dict[str, Any]:
    game_query = Game.query
    if id:
        game_query = game_query.filter_by(id=id, valid='1')

    game = game_query.first()

    # 根据查询结果返回相应的值
    if game:
        if user_id:
            game.user_id = user_id
        if protagonist_id:
            game.protagonist_id = protagonist_id
        if theme_id:
            game.theme_id = theme_id
        if if_finish:
            game.if_finish = if_finish
        if content:
            game.content = content
        if prompt_history:
            game.prompt_history = prompt_history

        db.session.commit()

        return {
            "id": game.id,
            "user_id": game.user_id,
            "theme_id": game.theme_id,
            "protagonist_id": game.protagonist_id,
            "content": game.content,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
            "valid": game.valid,
            "if_finish": game.if_finish,
            "prompt_history": game.prompt_history,
        }
    else:
        return {}


def del_game():
    return ''
