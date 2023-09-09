# user_controller.py
from database.models import User, db


def add_user(nick_name=None, phone=None, age=None, open_id=None, session_key=None, token=None, code=None, avatar_url=None
             , city=None, country=None, province=None, gender=None, language=None):
    # 添加一个新用户
    new_user = User(
        nick_name=nick_name,
        phone=phone,
        age=age,
        open_id=open_id,
        session_key=session_key,
        code=code,
        avatar_url=avatar_url,
        city=city,
        country=country,
        province=province,
        gender=gender,
        language=language,
        token=token,
    )
    db.session.add(new_user)
    db.session.commit()

    return {
            'id': new_user.id,
            'nick_name': new_user.nick_name,
            'phone': new_user.phone,
            'age': new_user.age,
            'open_id': new_user.open_id,
            'code': new_user.code,
            'avatar_url': new_user.avatar_url,
            'city': new_user.city,
            'country': new_user.country,
            'province': new_user.province,
            'gender': new_user.gender,
            'language': new_user.language,
            'token': new_user.token,
    }


def get_user(open_id):
    return ''


def edit_user(user_id, nick_name=None, phone=None, age=None, avatar_url=None, city=None, country=None,
              province=None, gender=None, language=None):
    user_query = User.query
    if user_id:
        user_query = user_query.filter_by(id=user_id, valid='1')
    user = user_query.first()

    user.nick_name = nick_name
    user.phone = phone
    user.age = age
    user.avatar_url = avatar_url
    user.city = city
    user.country = country
    user.province = province
    user.gender = gender
    user.language = language
    db.session.commit()

    return {
        "id": user.id,
        "nick_name": user.nick_name,
        "phone": user.phone,
        "age": user.age,
        "open_id": user.open_id,
        "avatar_url": user.avatar_url,
        "city": user.city,
        "country": user.country,
        "province": user.province,
        "gender": user.gender,
        "language": user.language,
        "token": user.token,
    }


def del_user():
    return ''


def find_user_by_open_id(open_id):
    user_query = User.query
    if open_id:
        user_query = user_query.filter_by(open_id=open_id, valid='1')
    user = user_query.first()

    if user:
        return {
            "id": user.id,
            "nick_name": user.nick_name,
            "phone": user.phone,
            "age": user.age,
            "open_id": user.open_id,
            "avatar_url": user.avatar_url,
            "city": user.city,
            "country": user.country,
            "province": user.province,
            "gender": user.gender,
            "language": user.language,
            "token": user.token,
        }
    else:
        return {}

