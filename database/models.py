from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    name = db.Column(db.String(80), nullable=False)
    # 电话
    phone = db.Column(db.String(20), unique=True, nullable=False)
    # 年龄
    age = db.Column(db.Integer, nullable=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # token
    token = db.Column(db.String(256), nullable=True)
    # 是否有效 (我假设valid是一个布尔字段，表示用户是否有效)
    valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Image(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 图片描述
    description = db.Column(db.String(255), nullable=True)
    # 图片地址
    image_url = db.Column(db.String(255), nullable=False)
    # 所属画册的外键
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', backref=db.backref('images', lazy=True))
    # 消费金额 (假设金额是小数形式)
    cost = db.Column(db.Float, nullable=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 是否有效
    valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Image {self.description}>"


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    album_name = db.Column(db.String(120), nullable=False)
    character_name = db.Column(db.String(120))
    character_race = db.Column(db.String(120))
    character_trait = db.Column(db.String(120))
    content = db.Column(db.Text)  # 使用文本字段来存储序列化后的整数数组
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    transaction_type = db.Column(db.String(50), nullable=False)  # 您可以使用'充值'或'消费'等值
    target_image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 外键指向图片表的id
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    content = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 外键指向图片表的id，可以为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)
