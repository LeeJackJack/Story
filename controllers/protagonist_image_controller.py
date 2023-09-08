from database.models import Protagonist,ProtagonistImage, db
from typing import Optional
from sqlalchemy.sql.expression import func
from logging import getLogger
from flask import jsonify

logger = getLogger(__name__)



def add_protagonist_image(image_url: str, image_description: str,
                          user_id: int,
                          protagonist_id: Optional[int] = None):

    # 参数验证
    if not image_url:
        raise ValueError("Image URL cannot be empty")

    if not image_description:
        raise ValueError("Image description cannot be empty")


    if user_id <= 0:
        raise ValueError("Invalid user ID")

    # 创建一个 Image 的实例
    new_image = ProtagonistImage(image_url=image_url,
                                 image_description=image_description,
                                 protagonist_id=protagonist_id,
                                 user_id=user_id)

    # 将实例添加到数据库会话
    db.session.add(new_image)

    # 提交会话以保存更改
    try:
        db.session.commit()
        return new_image.id  # 返回新创建的图片的 ID
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to add protagonist image: {e}")
        raise e


from flask import jsonify, request

# 查询并返回图片信息
def get_protagonist_image(protagonist_id: Optional[int] = None, image_id: Optional[int] = None):
    query = ProtagonistImage.query

    # 参数验证
    if protagonist_id:
        query = query.filter_by(protagonist_id=protagonist_id)
    if image_id:
        query = query.filter_by(id=image_id)

    # 分页
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_results = query.paginate(page, per_page, False)
    
    # 结果排序（此处按创建时间降序排序为例）
    query = query.order_by(ProtagonistImage.created_at.desc())

    images = paginated_results.items

    if not images:
        return jsonify({'status': 'error', 'message': 'No images found'}), 404

    # 格式化返回信息
    image_list = []
    for image in images:
        image_data = {
            'id': image.id,
            'image_url': image.image_url,
            'image_description': image.image_description,
            'protagonist_id': image.protagonist_id,
            'user_id': image.user_id,
            'created_at': image.created_at,
            'updated_at': image.updated_at,
            'valid': image.valid
        }
        image_list.append(image_data)

    return jsonify({
        'status': 'success', 
        'data': image_list,
        'total': paginated_results.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated_results.pages
    }), 200


#更新protagonist_image的
def edit_protagonist_image(image_id: int, new_protagonist_id: int):
    # 验证输入参数
    if image_id <= 0 or new_protagonist_id <= 0:
        return jsonify({'status': 'error', 'message': 'Invalid IDs'}), 400
    
    # 查找要编辑的 ProtagonistImage 对象
    image_to_edit = ProtagonistImage.query.get(image_id)
    if not image_to_edit:
        return jsonify({'status': 'error', 'message': 'Image not found'}), 404
    
    # 查找新的 Protagonist 对象
    new_protagonist = Protagonist.query.get(new_protagonist_id)
    if not new_protagonist:
        return jsonify({'status': 'error', 'message': 'Protagonist not found'}), 404
    
    # 更新 ProtagonistImage 的 protagonist_id 字段
    image_to_edit.protagonist_id = new_protagonist_id
    
    # 提交数据库会话
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to update: {e}'}), 500



def del_protagonist_image():
    return ''

