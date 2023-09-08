from database.models import db, Protagonist, Album, UserRoleRelation
from datetime import datetime
from controllers.protagonist_controller import add_protagonist
from controllers.album_controller import add_album
from controllers.game_controller import add_game


from controllers.album_controller import add_album

def create_pro_and_alb(user_id, description, name, race, feature, preset, theme_id, album_name, content, image_id=None):
    # 创建新角色并获取其ID
    # 参数 image_id 是新添加的，用于关联角色图片
    new_protagonist_id = add_protagonist(user_id, description, name, race, feature, preset, image_id)
    
    # 创建新绘本并获取其ID
    # 新添加的参数 theme_id, album_name, content 用于创建绘本
    # new_album_id = add_album(user_id, new_protagonist_id, theme_id, album_name, content)

    # 新建游戏
    new_game_id=add_game(user_id, new_protagonist_id, theme_id=1, 
             content=None, prompt_history=None)
    
    # 返回新创建的角色和绘本的ID
    return {'new_game_id': new_game_id, 'protagonist_id': new_protagonist_id}
