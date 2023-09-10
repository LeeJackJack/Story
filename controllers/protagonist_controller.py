from database.models import Protagonist, UserRoleRelation,ProtagonistImage, db
from typing import Optional
from sqlalchemy.sql.expression import func
from flask import request
from generate.text_to_image import generate_and_stream,generate_and_save_plot_image
from datetime import datetime
from controllers.protagonist_image_controller import edit_protagonist_image


# 创建角色
def add_protagonist(user_id, description, name, race, feature, preset,image_id=None):
    # print(image_id)
    new_protagonist = Protagonist(
        description=description,
        name=name,
        race=race,
        feature=feature,
        preset=preset,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        valid=True
    )
    db.session.add(new_protagonist)
    db.session.flush()  # 使得新的 Protagonist 对象的 ID 可用

    # 如果 image_id 存在，则更新 ProtagonistImage 的 protagonist_id 字段
    if image_id:
        edit_protagonist_image(image_id, new_protagonist.id)  # 角色表关联 Protagonist
    
    # 创建用户和角色之间的关联
    new_relation = UserRoleRelation(
        user_id=user_id,
        role_id=new_protagonist.id
    )
    db.session.add(new_relation)
    
    db.session.commit()
    
    return new_protagonist.id




def get_protagonist(id: int) -> dict:

    protagonist_query = Protagonist.query

    protagonist = protagonist_query.filter_by(id=id, valid='1')

    image = protagonist.protagonist_image

    protagonist = protagonist_query.first()

    # 根据查询结果返回相应的值
    if protagonist:
        return {
            "id": protagonist_query.id,
            "description": protagonist_query.description,
            "name": protagonist_query.name,
            "race": protagonist_query.race,
            "feature": protagonist_query.feature,
            "user_edit":protagonist_query.user_edit,
            "created_at": protagonist_query.created_at,
            "updated_at": protagonist_query.updated_at,
            "valid": protagonist_query.valid,
            "image": image
        }
    else:
        return {}


def edit_protagonist():
    return ''


def del_protagonist():
    return ''


# 获取预设角色描述及图片
def get_preset_role(user_id,preset=False):
    # 从数据库中获取一个随机的预设角色
    protagonist = Protagonist.query.filter_by(preset=True).order_by(func.random()).first()
    # 如果没有找到预设角色，则返回错误信息
    if not protagonist:
        return {"error": "No preset role found"}, 400
        # 从数据库中获取与该角色相关联的最新 image_id 和 image_description

    related_image = ProtagonistImage.query.filter_by(protagonist_id=protagonist.id)\
        .order_by(ProtagonistImage.created_at.desc()).first()
    if related_image:
        image_id = related_image.id
        image_description = related_image.image_description  

    # 如果需要生成新的图像，则调用图像生成函数
    # print("准备运行获取图片")
    # if not preset:
    #     print("运行获取图片")
    #     # image_data_generator = generate_and_save_plot_image(image_description, user_id, None) # 假设 album_id 和 user_id 为空
    #     #
    #     # next(image_data_generator) # 跳过第一个yield，例如"Image generation started..."
    #     #
    #     # # 获取第二个yield的值，即包含图像URL和图像详细信息的字典
    #     # image_data_result = next(image_data_generator)
    #     # image_data = image_data_result.get("generated_image_url", None)  # 提取图像URL
    #     # image_id = image_data_result.get("image_id", None)  # 提取图像ID
    #     #
    #     # if not image_data:
    #     #     return {"error": "Image generation failed"}, 500
    # else:
    #     # 如果 preset 为 True, 直接使用之前获取到的 image_id 来获取 image_url
    #     # image_data = related_image.image_url
    #     # 测试时先固定一个id
    #     image_data = "https://gpt-story.oss-cn-guangzhou.aliyuncs.com/out/20230908101731/image.png"
    #     image_id = 217

    return {
        "id": protagonist.id,
        "description": protagonist.description,
        "name": protagonist.name,
        "race": protagonist.race,
        "feature": protagonist.feature,
        "created_at": protagonist.created_at,
        "updated_at": protagonist.updated_at,
        "valid": protagonist.valid,
        "image_description": image_description,
        "image": "https://gpt-story.oss-cn-guangzhou.aliyuncs.com/out/20230908101731/image.png", # 提取角色图像URL
        "image_id": 217  # 提取角色图像ID
    }

# 根据编辑的描述生成图片
def generate_role_image(description):
    # 在此处实现您的逻辑
    return ...

