from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    nick_name = db.Column(db.Text, default='微信用户')
    # 电话
    phone = db.Column(db.String(20), unique=True, nullable=True)
    # 微信id
    open_id = db.Column(db.Text, nullable=True)
    # 微信session
    session_key = db.Column(db.Text, nullable=True)
    # 微信code
    code = db.Column(db.Text, nullable=True)
    # 微信头像
    avatar_url = db.Column(db.Text, nullable=True, default='https://thirdwx.qlogo.cn/mmopen/vi_32/POgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg/132')
    # 用户城市
    city = db.Column(db.Text, nullable=True)
    # 用户国家
    country = db.Column(db.Text, nullable=True)
    # 用户省分
    province = db.Column(db.Text, nullable=True)
    # 用户性别
    gender = db.Column(db.String(64), nullable=True)
    # 用户语言
    language = db.Column(db.String(64), nullable=True)
    # 年龄
    age = db.Column(db.Integer, nullable=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 是否有效 (我假设valid是一个布尔字段，表示用户是否有效)
    valid = db.Column(db.Boolean, default=True)
    token = db.Column(db.Text, nullable=True)


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


# 主人翁（角色）表
class Protagonist(db.Model):
    __tablename__ = 'protagonist'  # 表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增
    description = db.Column(db.Text, nullable=False)  # 角色描述
    name = db.Column(db.String(80), nullable=False)  # 角色名称
    race = db.Column(db.String(80), nullable=True)  # 角色种族
    feature = db.Column(db.String(255), nullable=True)  # 角色特点
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    valid = db.Column(db.Boolean, default=True)  # 是否有效
    preset = db.Column(db.Boolean, default=False)  # 是否为预设角色
    protagonist_images = db.relationship('ProtagonistImage', backref='protagonist', lazy=True)  # 与 ProtagonistImage 的关联关系

# 角色图片表
class ProtagonistImage(db.Model):
    __tablename__ = 'protagonist_image'  # 表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增
    image_url = db.Column(db.String(255), nullable=False)  # 图片URL
    image_description = db.Column(db.Text, nullable=False)  # 用于生成图片的描述
    protagonist_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), nullable=True)  # 关联的主角ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 创建该图像的用户ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    valid = db.Column(db.Boolean, default=True)  # 是否有效


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
    # 是否被选中
    chosen = db.Column(db.String(255), default='0')


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

#用户角色关系
class UserRoleRelation(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True) # 用户ID（外键，指向用户表）
    role_id = db.Column(db.Integer, db.ForeignKey('protagonist.id'), primary_key=True) # 角色ID（外键，指向主人翁表）

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



