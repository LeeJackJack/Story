
from main import app  # 从您的主应用文件中导入Flask应用
from controllers.protagonist_controller import get_preset_role

if __name__ == "__main__":
    with app.app_context():  # 创建并使用应用程序上下文
        result = get_preset_role()
        print("Result:", result)
