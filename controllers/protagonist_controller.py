from database.models import Protagonist, UserRoleRelation, db
from typing import Optional
from sqlalchemy.sql.expression import func
from flask import request
from generate.text_to_image import generate_and_stream,generate_and_save_plot_image
from datetime import datetime



# 创建角色
def add_protagonist(user_id, description, name, race, feature, image, preset, image_description=None):
    new_protagonist = Protagonist(
        description=description,
        name=name,
        race=race,
        feature=feature,
        image=image,
        preset=preset,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        valid=True,
        image_description=image_description 
    )
    db.session.add(new_protagonist)
    db.session.flush()  # 使得新的 Protagonist 对象的 ID 可用
    
    # 创建用户和角色之间的关联
    new_relation = UserRoleRelation(
        user_id=user_id,
        role_id=new_protagonist.id
    )
    db.session.add(new_relation)
    
    db.session.commit()
    
    return new_protagonist.id



def get_protagonist():
    return ''


def edit_protagonist():
    return ''


def del_protagonist():
    return ''


def get_random_protagonist():
    protagonist = Protagonist.query.order_by(func.random()).first()
    if protagonist:
        return {
            "id": protagonist.id,
            "description": protagonist.description,
            "name": protagonist.name,
            "race": protagonist.race,
            "feature": protagonist.feature,
            "created_at": protagonist.created_at,
            "updated_at": protagonist.updated_at,
            "valid": protagonist.valid,
            "image_description": protagonist.image_description,
            "image": protagonist.image
        }
    else:
        return None
    
# 获取预设角色描述及图片
def get_preset_role(preset=False):
    # 从数据库中获取一个随机的预设角色
    protagonist = Protagonist.query.filter_by(preset=True).order_by(func.random()).first()
    # 如果没有找到预设角色，则返回错误信息
    if not protagonist:
        return {"error": "No preset role found"}, 404

    # 如果需要生成新的图像，则调用图像生成函数
    print("准备运行获取图片")
    if not preset:
        print("运行获取图片")
        image_data_generator = generate_and_save_plot_image(protagonist.image_description, None, None) # 假设 album_id 和 user_id 为空

        next(image_data_generator) # 跳过第一个yield，例如"Image generation started..."

        # 获取第二个yield的值，即包含图像URL和图像详细信息的字典
        image_data_result = next(image_data_generator)
        image_data = image_data_result.get("generated_image_url", None) # 提取图像URL

        if not image_data:
            return {"error": "Image generation failed"}, 500


    else:
        image_data = protagonist.image

    return {
        "id": protagonist.id,
        "description": protagonist.description,
        "name": protagonist.name,
        "race": protagonist.race,
        "feature": protagonist.feature,
        "created_at": protagonist.created_at,
        "updated_at": protagonist.updated_at,
        "valid": protagonist.valid,
        "image_description": protagonist.image_description,
        "image": image_data # 提取图像URL
    }

# 根据编辑的描述生成图片
def generate_role_image(description):
    # 在此处实现您的逻辑
    return ...

