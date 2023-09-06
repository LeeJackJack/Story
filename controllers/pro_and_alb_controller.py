from database.models import db, Protagonist, Album, UserRoleRelation
from datetime import datetime
from controllers.protagonist_controller import add_protagonist
from controllers.album_controller import add_album


from controllers.album_controller import add_album

def create_pro_and_alb(user_id, description, name, race, feature, image, preset, image_description, theme_id, album_name, content):
    # 创建新角色并获取其ID
    new_protagonist_id = add_protagonist(user_id, description, name, race, feature, image, preset, image_description)
    
    # 创建新绘本并获取其ID
    new_album_id = add_album(user_id, new_protagonist_id, theme_id, album_name, content)
    
    # 返回新创建的角色和绘本的ID
    return {'album_id': new_album_id, 'protagonist_id': new_protagonist_id}



