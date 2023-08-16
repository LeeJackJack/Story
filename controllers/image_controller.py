from database.models import Image, db
from typing import Optional


def add_image(image_url: str,
              album_id: Optional[int] = None,
              user_id: Optional[int] = None,
              description: Optional[str] = None,
              cost: Optional[float] = None,
              valid: Optional[bool] = True) -> None:

    # 创建一个 Image 的实例
    new_image = Image(image_url=image_url,
                      album_id=album_id,
                      user_id=user_id,
                      description=description,
                      cost=cost)

    # 将实例添加到数据库会话
    db.session.add(new_image)

    # 提交会话以保存更改
    try:
        db.session.commit()
    except Exception as e:
        # 如果出现错误，回滚会话
        db.session.rollback()
        raise e


def get_image():
    return ''


def edit_image():
    return ''


def del_image():
    return ''
