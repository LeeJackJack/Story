# main.py
import json
from flask import Flask, render_template, request, stream_with_context, Response, jsonify
import requests
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream, generate_and_stream_plot_image, generate_and_save_plot_image, \
    test_generate_and_stream
from generate.completions import get_lan_response
from database.models import db
import os
from flask_cors import cross_origin, CORS
from controllers.user_controller import add_user, find_user_by_open_id, edit_user
from controllers.protagonist_controller import get_preset_role, generate_role_image, get_protagonist, get_protagonist_list, add_protagonist
from controllers.story_plot_controller import get_random_story_plot
from controllers.description_controller import get_description
from controllers.album_controller import get_album, edit_album
from controllers.game_controller import get_game, reset_game_plot, add_game, save_game_data
from controllers.image_controller import add_plot_image, get_image, edit_image
from controllers.theme_controller import get_theme_list, add_theme, get_theme
from controllers.pro_and_alb_controller import create_pro_and_alb
from generate.qinghua_completions import submit_plot_choice, get_random_plot, create_img_prompt, \
    create_plot, init_game_data, test_fake_init
from flask_jwt_extended import JWTManager, create_access_token
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

# JWT 配置
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_SECRET']  # JWT秘钥
jwt = JWTManager(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generateImg', methods=['GET'])
def generate_img():
    # prompt = request.json.get('prompt')
    return Response(stream_with_context(test_generate_and_stream()), content_type='text/plain')


@app.route('/generateGpt', methods=['GET'])
def generate_gpt():
    response = get_lan_response()
    return jsonify({"response": response})


@app.route('/getPlot', methods=['GET'])
def get_story_plot():
    chapter = int(request.args.get('chapter_next'))
    # print(chapter)
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
    user_id = request.args.get('user_id', type=int)  # 获取 user_id 参数
    return get_preset_role(user_id=user_id, preset=preset)


# 创建角色（Protagonist）和绘本（Album）并返回相关数据。
# 创建角色并将描述和图片保存到数据库
@app.route('/createProAndAlb', methods=['POST'])  # 使用 POST 方法，因为我们要创建新资源。
def create_pro_and_alb_route():
    data = request.json
    user_id = int(data.get('user_id'))
    description = data.get('description')
    protagonist_id = int(data.get('protagonist'))
    name = data.get('name')
    race = data.get('race')
    feature = data.get('feature')
    preset = data.get('preset', False)
    theme_id = int(data.get('theme_id'))  # 新添加的字段，用于绘本的主题ID
    album_name = data.get('album_name')  # 新添加的字段，用于绘本名称
    content = data.get('content')  # 新添加的字段，用于绘本内容
    image_id = data.get('image_id', None)  # 新添加的字段，用于角色图片ID

    result = create_pro_and_alb(user_id, description, name, race, feature, preset, theme_id, album_name, content, image_id)
    return jsonify(result)


# 根据编辑的描述生成图片
@app.route('/api/roles/generate-image', methods=['POST'])
def generate_role_image_route():
    description = request.json.get('description')
    return generate_role_image(description)


# 20230901 新版本新增接口 ----------------------------------------------------------------------------------------
@app.route('/getGameData', methods=['GET'])
def get_game_data():
    game_id = int(request.args.get('id'))
    result = get_game(game_id)
    return jsonify(result)


@app.route('/getRandomPlot', methods=['GET'])
def refresh_plot():
    game_id = int(request.args.get('id'))
    result = get_random_plot(game_id)
    return jsonify(result)


@app.route('/submitAnswer', methods=['GET'])
def submit_answer():
    choice = request.args.get('choice')
    game_id = int(request.args.get('id'))
    result = submit_plot_choice(game_id, choice)
    # print(result)
    return jsonify(result)


#用户输入转图片创造
@app.route('/createPlotImage', methods=['GET'])
def create_plot_image():
    content = request.args.get('content')
    game_id = int(request.args.get('game_id'))
    user_id = int(request.args.get('user_id'))
    prompt = create_img_prompt(content)

    if prompt:
        generator = generate_and_stream_plot_image(prompt)
        next(generator)
        generated_image_url = next(generator)

        # 保存图片数据
        result = add_plot_image(image_url=generated_image_url, plot_description=json.loads(content)['content'],
                                game_id=game_id, user_id=user_id, image_description=prompt)
        # print(result)
        return jsonify(result)


@app.route('/refreshPlotImage', methods=['GET'])
def refresh_plot_image():
    content = request.args.get('content')
    image_id = int(request.args.get('image_id'))
    prompt = create_img_prompt(content)

    # 获取图像内容
    image = get_image(image_id=image_id)

    if prompt:
        generator = generate_and_stream_plot_image(prompt)
        next(generator)
        generated_image_url = next(generator)

        # 保存图片数据
        result = add_plot_image(image_url=generated_image_url, plot_description=image['plot_description'],
                                game_id=image['game_id'], user_id=image['user_id'], image_description=prompt)
        # print(result)
        return jsonify(result)


@app.route('/confirmChosenImage', methods=['GET'])
def confirm_chosen_image():
    image_id = int(request.args.get('image_id'))
    # 修改图像为已选择
    image = edit_image(image_id=image_id)
    return jsonify(image)


@app.route('/createChoice', methods=['GET'])
def create_plot_content():
    choice = request.args.get('choice')
    game_id = int(request.args.get('game_id'))
    result = create_plot(choice, game_id)
    return jsonify(result)


@app.route('/resetStory', methods=['GET'])
def reset_game():
    game_id = int(request.args.get('game_id'))
    result = reset_game_plot(game_id)
    # print(result)
    return jsonify(result)


# 获取微信用户登录信息
@app.route('/wxLogin', methods=['GET'])
def wx_login():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Missing code"}), 400

    # 与微信服务器交互，获取 openId 和 sessionKey
    payload = {
        'appid': os.environ['MINI_PROGRAM_APP_ID'],
        'secret': os.environ['MINI_PROGRAM_APP_SECRET'],
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.get(os.environ['WX_LOGIN_URL'], params=payload)
    data = response.json()

    session_key = data['session_key']
    openid = data['openid']
    token = create_access_token(identity={'session_key': session_key, 'openid': openid})

    # 先查找用户是否已存在
    user = find_user_by_open_id(openid)
    # 不存在则存储新用户
    if not user:
        user = add_user(open_id=openid, session_key=session_key, token=token)

    return jsonify(user)


# 更新微信用户登录信息
@app.route('/wxLoginUpdate', methods=['GET'])
def wx_login_update():
    avatar_url = request.args.get('avatarUrl')
    city = request.args.get('city')
    country = request.args.get('country')
    gender = request.args.get('gender')
    language = request.args.get('language')
    nick_name = request.args.get('nickName')
    province = request.args.get('province')
    user_id = request.args.get('user_id')

    # 更新用户表信息
    user = edit_user(user_id=user_id, avatar_url=avatar_url, city=city, country=country, gender=gender,
                     language=language, nick_name=nick_name, province=province)

    return jsonify(user)


# 获取故事主题信息
@app.route('/getThemeData', methods=['GET'])
def get_theme_data_list():
    result = get_theme_list()
    print(result)
    return jsonify(result)


# 获取随机n个角色信息
@app.route('/getRoleData', methods=['GET'])
def get_random_protagonist_data():
    n = 7
    result = get_protagonist_list(n)
    # print(result)
    return jsonify(result)


# 用户自定义角色信息
@app.route('/createRoleData', methods=['GET'])
def create_protagonist_data():
    name = request.args.get('name')
    description = request.args.get('description')
    user_id = request.args.get('user_id')
    result = add_protagonist(user_id=user_id, description=description, name=name, preset=False)
    return jsonify(result)


# 用户自定义故事主题
@app.route('/createThemeData', methods=['GET'])
def create_theme_data():
    theme = request.args.get('theme')
    description = request.args.get('description')
    result = add_theme(theme=theme, description=description, preset=False)
    return jsonify(result)


# 用户根据主角，故事主题创建游戏
@app.route('/initGameData', methods=['GET'])
def init_game_start_data():
    theme_id = int(request.args.get('theme_id'))
    user_id = int(request.args.get('user_id'))
    protagonist_id = int(request.args.get('protagonist_id'))
    # 获取故事主角信息
    protagonist = get_protagonist(id=protagonist_id)
    # print(protagonist)
    # 获取故事主题信息
    theme = get_theme(theme_id=theme_id)
    # 调用大模型，初始化故事的内容
    init_story_result = init_game_data(theme=json.dumps(theme), protagonist=json.dumps(protagonist))
    print(init_story_result)
    # 保存数据内容到数据库
    result = save_game_data(user_id=user_id, theme=json.dumps(theme), protagonist=json.dumps(protagonist), game_data=json.dumps(init_story_result))
    return {'new_game_id': result, 'protagonist_id': protagonist_id}


# 获取特定故事主题内容
@app.route('/getTheme', methods=['GET'])
def get_theme_data():
    theme_id = request.args.get('theme_id')
    result = get_theme(theme_id=theme_id)
    return jsonify(result)


@app.route('/testFakeInit', methods=['GET'])
def test_invoke():
    result = test_fake_init()
    return jsonify(result)


if __name__ == '__main__':
    app.run()
    # socketio.run(app, debug=True)
