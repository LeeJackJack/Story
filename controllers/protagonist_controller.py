from database.models import Protagonist, db
from typing import Optional
from sqlalchemy.sql.expression import func
from flask import request
from generate.text_to_image import generate_and_stream



def add_protagonist():

    return ""


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
    if not preset:
        image_data_generator = generate_and_stream(protagonist.image_description)
        next(image_data_generator) # 跳过第一个yield，例如"Image generation started..."
        next(image_data_generator) # 跳过第二个yield，例如"Image generated successfully! URL: ..."
        next(image_data_generator) # 跳过第三个yield，例如"Upscale Image generated successfully! ..."

        # 获取第四个yield的值，即图像的URL列表
        image_data_line = next(image_data_generator) 
        image_data = image_data_line.split("FI-URL: ")[1].strip() if "FI-URL:" in image_data_line else None

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
        "image": image_data
    }

# 根据编辑的描述生成图片
def generate_role_image(description):
    # 在此处实现您的逻辑
    return ...

# 创建角色
def create_role(description, image_data):
    # 在此处实现您的逻辑
    return ...