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


def edit_image(image_id: int,
               image_url: Optional[str] = None ,
               plot_description: Optional[str] = None,
               game_id: Optional[int] = None,
               user_id: Optional[int] = None,
               image_description: Optional[str] = None,
               chosen: Optional[str] = None,
               cost: Optional[float] = None,
               valid: Optional[bool] = True) -> Dict[str, Any]:

    image_query = Image.query
    image = image_query.filter_by(id=image_id, valid='1').first()
    image.chosen = '1'
    db.session.commit()  # 提交更改

    # 根据查询结果返回相应的值
    if image:
        return {
            "id": image.id,
            "image_url": image.image_url,
            "plot_description": image.plot_description,
            "game_id": image.game_id,
            "user_id": image.user_id,
            "image_description": image.image_description,
            "cost": image.cost,
            "valid": image.valid,
            "chosen": image.chosen,
        }
    else:
        return {}


def get_image(image_id: int,
              image_url: Optional[str] = None ,
              plot_description: Optional[str] = None,
              game_id: Optional[int] = None,
              user_id: Optional[int] = None,
              image_description: Optional[str] = None,
              chosen: Optional[str] = None,
              cost: Optional[float] = None,
              valid: Optional[bool] = True) -> Dict[str, Any]:
    image_query = Image.query

    image = image_query.filter_by(id=image_id, valid='1').first()

    # 根据查询结果返回相应的值
    if image:
        return {
            "id": image.id,
            "image_url": image.image_url,
            "plot_description": image.plot_description,
            "game_id": image.game_id,
            "user_id": image.user_id,
            "image_description": image.image_description,
            "cost": image.cost,
            "valid": image.valid,
            "chosen": image.chosen,
        }
    else:
        return {}


def del_image():
    return ''


def add_plot_image(image_url: str,
                   plot_description: Optional[str] = None,
                   game_id: Optional[int] = None,
                   user_id: Optional[int] = None,
                   image_description: Optional[str] = None,
                   chosen: Optional[str] = '0',
                   cost: Optional[float] = None,
                   valid: Optional[bool] = True) -> Dict[str, Any]:

    # 创建一个 Image 的实例
    new_image = Image(image_url=image_url,
                      game_id=game_id,
                      user_id=user_id,
                      plot_description=plot_description,
                      image_description=image_description,
                      cost=cost,
                      chosen='0')

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
            'chosen': '0',
            'valid': valid
        }
    except Exception as e:
        # 如果出现错误，回滚会话
        db.session.rollback()
        raise e


