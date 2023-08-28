from flask import Flask, render_template, request, stream_with_context, Response, jsonify
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream, generate_and_stream_plot_image, generate_and_save_plot_image
from generate.completions import get_lan_response
from database.models import db
import os
from flask_cors import cross_origin, CORS
from controllers.protagonist_controller import get_preset_role, generate_role_image, create_role, get_protagonist
from controllers.story_plot_controller import get_random_story_plot
from controllers.description_controller import get_description
from controllers.album_controller import get_album, edit_album
from app_instance import app


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


@app.route('/getProtagonist', methods=['GET'])
def get_protagonist_data():
    # 获取请求中的 'id' 参数
    protagonist_id = request.args.get('protagonist_id', type=int)
    result = get_protagonist(id=protagonist_id)
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
    preset = preset_str.lower() != "false"  # 如果 preset_str 不是 "false"，则 preset 为 True
    return get_preset_role(preset)


# 根据编辑的描述生成图片
@app.route('/api/roles/generate-image', methods=['POST'])
def generate_role_image_route():
    description = request.json.get('description')
    return generate_role_image(description)


# 创建角色并将描述和图片保存到数据库
@app.route('/api/roles/create', methods=['POST'])
def create_role_route():
    description = request.json.get('description')
    image_data = request.json.get('image_data')
    return create_role(description, image_data)


if __name__ == '__main__':
    app.run()
