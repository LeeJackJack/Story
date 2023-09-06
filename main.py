from flask import Flask, render_template, request, stream_with_context, Response, jsonify
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream, generate_and_stream_protagonist, generate_and_stream_plot_image, generate_and_save_plot_image
from generate.completions import get_lan_response
from database.models import db, User
import os
from flask_cors import cross_origin, CORS
from controllers.user_controller import add_user
from tools.ali_oss import upload_pic
from controllers.protagonist_controller import get_random_protagonist,get_preset_role, generate_role_image
from controllers.story_plot_controller import get_random_story_plot
from controllers.description_controller import get_description
from controllers.album_controller import get_album, edit_album
from app_instance import app
from controllers.pro_and_alb_controller import create_pro_and_alb


load_dotenv()  # 加载 .env 文件中的变量
CORS(app)

# 使用 os.environ 从 .env 文件中获取配置
DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
DATABASE_HOST = os.environ['DATABASE_HOST']
DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generateImg', methods=['POST'])
def generate_img():
    prompt = request.json.get('prompt')
    return Response(stream_with_context(generate_and_stream(prompt)), content_type='text/plain')


@app.route('/generateGpt', methods=['GET'])
def generate_gpt():
    response = get_lan_response()
    return jsonify({"response": response})


@app.route('/test', methods=['POST'])
def get_account():
    print('test')


@app.route('/uploadImg', methods=['GET'])
def upload_img():
    return upload_pic('1', '2')


# 测试数据连接
@app.route('/getUser')
def get_user():
    return add_user()


@app.route('/getProtagonist')
def get_protagonist():
    protagonist = get_random_protagonist()
    if protagonist:
        return jsonify(protagonist)
    else:
        return jsonify({"error": "No protagonist found"}), 404


@app.route('/createProtagonistImage', methods=['POST'])
def create_protagonist_image():
    prompt = request.json.get('prompt')
    protagonist_id = request.json.get('protagonist_id')
    return Response(stream_with_context(generate_and_stream_protagonist(prompt, protagonist_id)), content_type='text/plain')


@app.route('/createProtagonist')
def create_protagonist():
    protagonist = get_random_protagonist()
    if protagonist:
        return jsonify(protagonist)
    else:
        return jsonify({"error": "No protagonist found"}), 404


@app.route('/getPlot', methods=['GET'])
def get_story_plot():
    chapter = int(request.args.get('chapter_next'))
    print(chapter)
    theme_id = int(request.args.get('theme_id'))
    plot = get_random_story_plot(chapter, theme_id)
    return jsonify(plot)


@app.route('/getPlotImage', methods=['POST'])
def get_story_plot_image():
    # plot_id = request.json.get('plot_id')
    plot_id = 23
    description = get_description(plot_id=plot_id)

    return Response(stream_with_context(generate_and_stream_plot_image(description['content'])), content_type='text/plain')


@app.route('/getAlbum', methods=['GET'])
def get_album_route():
    # 获取请求中的 'id' 参数
    album_id = request.args.get('album_id', type=int)
    result = get_album(album_id=album_id)
    return jsonify(result)


@app.route('/changeImage', methods=['GET'])
def change_plot_image():
    description = request.args.get('description')
    album_id = request.args.get('album_id', type=int)
    user_id = request.args.get('user_id', type=int)
    result = generate_and_save_plot_image(description, album_id, user_id)
    next(result)
    image_url = next(result)
    return jsonify(image_url)


@app.route('/saveAlbum', methods=['GET'])
def save_album():
    album_id = request.args.get('album_id', type=int)
    data = request.args.get('formData')
    # print(data)
    result = edit_album(album_id=album_id, content=data)
    return jsonify(result)

# 获取预设角色描述及图片
@app.route('/api/roles/preset/random', methods=['GET'])
def get_preset_role_route():
    preset_str = request.args.get('preset', default="false")
    preset = preset_str.lower() != "false" # 如果 preset_str 不是 "false"，则 preset 为 True
    return get_preset_role(preset)

# 创建角色（Protagonist）和绘本（Album）并返回相关数据。
# 创建角色并将描述和图片保存到数据库
@app.route('/createProAndAlb', methods=['POST'])  # 使用 POST 方法，因为我们要创建新资源。
def create_pro_and_alb_route():
    data = request.json
    user_id = int(data.get('user_id'))
    description = data.get('description')
    name = data.get('name')
    race = data.get('race')
    feature = data.get('feature')
    image = data.get('image')
    preset = data.get('preset', False)
    image_description = data.get('image_description')  # 新添加的字段
    theme_id = int(data.get('theme_id'))  # 新添加的字段
    album_name = data.get('album_name')  # 新添加的字段
    content = data.get('content')  # 新添加的字段

    result = create_pro_and_alb(user_id, description, name, race, feature, image, preset, image_description, theme_id, album_name, content)
    return jsonify(result)


# 根据编辑的描述生成图片
@app.route('/api/roles/generate-image', methods=['POST'])
def generate_role_image_route():
    description = request.json.get('description')
    return generate_role_image(description)



if __name__ == '__main__':
    app.run()

