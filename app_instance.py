# app_instance.py

from flask import Flask
from flask_socketio import SocketIO, emit,send
from flask_sockets import Sockets
import zhipuai
import eventlet
import logging


# eventlet.monkey_patch()
app = Flask(__name__, static_folder='out')
app.debug = True
# socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# logging.basicConfig(filename='socketio_errors.log', level=logging.DEBUG)

#
# @socketio.on_error_default  # 默认的错误处理器
# def default_error_handler(e):
#     app.logger.error('An error has occurred: ' + str(e))
#
#
# @socketio.on('connect')
# def handle_connect():
#     print('im connected')
#
#
# @socketio.on('disconnect')
# def handle_disconnect():
#     print('im disconnect')
#
#
# @app.route('/ping')
# def ping():
#     socketio.emit('ping event', {'data': 42})
#
#
# @socketio.on('message')
# def handle_message(message):
#     print('received json:', message)
#     emit('message response', 'received: ' + str(message))
#
#     # emit('handle_message', {'data': 'Stream finished'})
#     # response = zhipuai.model_api.sse_invoke(
#     #     model="chatglm_pro",
#     #     prompt="你好，你可以帮助我做什么？",
#     #     temperature=1,
#     #     top_p=0.7,
#     #     incremental=True
#     # )
#     #
#     # for event in response.events():
#     #     if event.event in ["add", "finish"]:
#     #         emit('message', {'data': event.data})
#     #     elif event.event in ["error", "interrupted"]:
#     #         print('Error or interrupted:', event.data)
#     #         emit('error', {'data': event.data})
#     #
#     # emit('done', {'data': 'Stream finished'})
#
#
# @app.errorhandler(400)
# def handle_bad_request(e):
#     app.logger.error(f"Bad Request: {str(e)}")
#     return 'Bad Request', 400
#
#
# @app.errorhandler(500)
# def handle_server_error(e):
#     app.logger.exception("Internal Server Error")
#     return 'Internal Server Error', 500

