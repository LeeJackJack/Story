from database.models import ProtagonistImage, db
from typing import Optional
from sqlalchemy.sql.expression import func


def add_protagonist_image(image_url: str,
              protagonist_id: Optional[int] = None,
              user_id: Optional[int] = None):

    # 创建一个 Image 的实例
    new_image = ProtagonistImage(image_url=image_url,
                      protagonist_id=protagonist_id,
                      user_id=user_id)

    # 将实例添加到数据库会话
    db.session.add(new_image)

    # 提交会话以保存更改
    try:
        db.session.commit()
    except Exception as e:
        # 如果出现错误，回滚会话
        db.session.rollback()
        raise e


def get_protagonist_image():
    return ''


def edit_protagonist_image():
    return ''


def del_protagonist_image():
    return ''

