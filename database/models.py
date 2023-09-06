from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# 用户表
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


# 画册表
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    theme_id = db.Column(db.Integer, db.ForeignKey('album_theme.id'), nullable=False)  # 外键指向主题表的id
    album_name = db.Column(db.String(120), nullable=False)
    protagonist_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), nullable=False)  # 外键指向主人翁表的id
    content = db.Column(db.Text)  # 使用文本字段来存储序列化后的整数数组
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


# 画册主题表
class AlbumTheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


# 主题剧情表
class StoryPlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('album_theme.id'), nullable=False)  # 外键指向画册主题表的id
    chapter = db.Column(db.Integer, nullable=False)  # 章节编号
    description = db.Column(db.String(100), nullable=False)  # 章节描述
    gpt_description = db.relationship('Description', backref='story_plot', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)
    default_image = db.Column(db.Text, nullable=False)


# 主人翁（主角）表
class Protagonist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(80), nullable=False)
    feature = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)
    image_description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)  # 图片的URL
    preset = db.Column(db.Boolean, default=False)  # 字段用于区分是否为预设角色
    protagonist_image = db.relationship('ProtagonistImage', backref='protagonist_image', lazy=True)


# 用户角色关系表：记录哪些用户使用了哪些角色
class UserRoleRelation(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True) # 用户ID（外键，指向用户表）
    role_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), primary_key=True) # 角色ID（外键，指向主人翁表）


# 图片表
class ProtagonistImage(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 图片地址
    image_url = db.Column(db.String(255), nullable=False)
    # 所属画册的外键
    protagonist_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), nullable=False)
    # 所属用户的外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 是否有效
    valid = db.Column(db.Boolean, default=True)


class Image(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 剧情描述
    plot_description = db.Column(db.Text, nullable=True)
    # 图片描述
    image_description = db.Column(db.Text, nullable=True)
    # 图片地址
    image_url = db.Column(db.Text, nullable=False)
    # 所属画册的外键
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    # 所属用户的外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 消费金额 (假设金额是小数形式)
    cost = db.Column(db.Float, nullable=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 是否有效
    valid = db.Column(db.Boolean, default=True)


# 剧情图片描述表
class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 外键指向图片表的id，可以为空
    image = db.relationship('Image', backref='descriptions', lazy=True)  # 注意这里使用了复数形式
    plot_id = db.Column(db.Integer, db.ForeignKey('story_plot.id'))  # 外键指向主题剧情表的id，可以为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


# 消费表
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    transaction_type = db.Column(db.String(50), nullable=False)  # 0 代表生文 1 代表生图
    target_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 外键指向图片表的id
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)


# 游戏表
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键指向用户表的id
    protagonist_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), nullable=False)  # 外键指向主角表的id
    theme_id = db.Column(db.Integer, db.ForeignKey('album_theme.id'), nullable=False)  # 外键指向主题表的id
    content = db.Column(db.Text)  # 使用文本字段来存储序列化后的整数数组
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    valid = db.Column(db.Boolean, default=True)
    if_finish = db.Column(db.Boolean, default=False)
    prompt_history = db.Column(db.Text)



