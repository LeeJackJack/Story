from database.models import Image, db
from typing import Optional, Dict, Any


def add_image(image_url: str,
              album_id: Optional[int] = None,
              user_id: Optional[int] = None,
              image_description: Optional[str] = None,
              cost: Optional[float] = None,
              valid: Optional[bool] = True) -> Dict[str, Any]:

    # 创建一个 Image 的实例
    new_image = Image(image_url=image_url,
                      album_id=album_id,
                      user_id=user_id,
                      image_description=image_description,
                      cost=cost)

    # 将实例添加到数据库会话
    db.session.add(new_image)

    # 提交会话以保存更改
    try:
        db.session.commit()

        # 构建并返回新图片的详细信息
        return {
            'id': new_image.id,
            'image_url': new_image.image_url,
            'album_id': new_image.album_id,
            'user_id': new_image.user_id,
            'image_description': new_image.image_description,
            'cost': new_image.cost,
            'valid': valid
        }
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


def add_plot_image(image_url: str,
                   plot_description: Optional[str] = None,
                   game_id: Optional[int] = None,
                   user_id: Optional[int] = None,
                   image_description: Optional[str] = None,
                   cost: Optional[float] = None,
                   valid: Optional[bool] = True) -> Dict[str, Any]:

    # 创建一个 Image 的实例
    new_image = Image(image_url=image_url,
                      game_id=game_id,
                      user_id=user_id,
                      plot_description=plot_description,
                      image_description=image_description,
                      cost=cost)

    # 将实例添加到数据库会话
    db.session.add(new_image)

    # 提交会话以保存更改
    try:
        db.session.commit()

        # 构建并返回新图片的详细信息
        return {
            'id': new_image.id,
            'image_url': new_image.image_url,
            'game_id': new_image.game_id,
            'plot_description': new_image.plot_description,
            'user_id': new_image.user_id,
            'image_description': new_image.image_description,
            'cost': new_image.cost,
            'valid': valid
        }
    except Exception as e:
        # 如果出现错误，回滚会话
        db.session.rollback()
        raise e


