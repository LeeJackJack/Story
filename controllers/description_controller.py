from database.models import Description, db
from typing import Optional
from sqlalchemy.sql.expression import func


def add_description(
    user_id: int,
    content: str,
    cost: Optional[float] = None,
    image_id: Optional[int] = None,
    valid: Optional[bool] = True,
    chat_id: Optional[str] = None,
    chat_role: Optional[str] = None,
    prompt_tokens: Optional[str] = None,
    completion_tokens: Optional[str] = None,
    total_tokens: Optional[str] = None,
    chat_model: Optional[str] = None
) -> None:

    return ""


def get_description(image_id: Optional[int] = None,
                    plot_id: Optional[int] = None) -> dict:
    description_query = Description.query

    if image_id:
        description_query = description_query.filter_by(image_id=image_id, valid='1')

    if plot_id:
        description_query = description_query.filter_by(plot_id=plot_id,valid='1')

    description = description_query.first()

    # 根据查询结果返回相应的值
    if description:
        return {
            "id": description.id,
            "content": description.content,
            "image_id": description.image_id,
            "plot_id": description.plot_id,
            "created_at": description.created_at,
            "updated_at": description.updated_at,
            "valid": description.valid
        }
    else:
        return {}


def edit_description():
    return ''


def del_description():
    return ''

