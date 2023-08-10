from flask import Flask, render_template, request, stream_with_context, Response, jsonify
from dotenv import load_dotenv
from generate.text_to_image import generate_and_stream
from generate.completions import get_lan_response
from database.models import db, User
import os
from controllers.user_controller import add_new_user

load_dotenv()  # 加载 .env 文件中的变量
app = Flask(__name__, static_folder='out')

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


@app.route('/generateGpt', methods=['POST'])
def generate_gpt():
    prompt = ''
    response = get_lan_response(prompt)
    return jsonify({"response": response})


@app.route('/test', methods=['POST'])
def get_account():
    print('test')


# 测试数据连接
@app.route('/getUser')
def get_user():
    return add_new_user()


if __name__ == '__main__':
    app.run()