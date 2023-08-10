# user_controller.py
from database.models import User, db


def add_new_user():
    # 示例：添加一个新用户
    new_user = User(name='john', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()

    return "User added!"
