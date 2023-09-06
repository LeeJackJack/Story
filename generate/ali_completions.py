import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation
from http import HTTPStatus
import json

load_dotenv()  # 加载 .env 文件中的变量
api = os.environ['DASHSCOPE_API_KEY']
dashscope.api_key = api


def call_with_messages():
    print('loading')
    response = Generation.call(
        # model='qwen-v1',
        # model='qwen-7b-chat-v1',
        model='qwen-7b-v1',
        prompt="我希望你扮演一个基于文本的冒险游戏（游戏主题：魔法兔子的秘密）；提供总共8回合的游戏。您将回复故事情节内容的描述。"
               "你需要首先给我第一个场景及情节描述，并给我提供a\\b\\c;以及换一批，四个选项如果我回复选项a\\b\\c，则继续生成下一回合内容"
               "如果我回复换一批选项，则重新生成当前回合内容，给新的选项每个关卡的故事情节必须控制在80字以内你设计的故事需要在八个回合内结束，"
               "故事的情节结构需要包含故事的开端、情节推进、关键决策、情节发展、高潮冲突、结局逼近、最终结局这几个关卡你给我的情节需要有趣好玩，"
               "适合儿童阅读，前后逻辑有联系；你给的格式如下：回合：（是整数，从1开始递增，如果换一批则保持不变）故事结构：（枚举值：故事的开端、"
               "情节推进、关键决策、情节发展、高潮冲突、结局逼近、最终结局，之一）故事内容：选项： a: b: c: 换一批选项："
    )
    if response.status_code == HTTPStatus.OK:
        print(json.dumps(response.output, indent=4, ensure_ascii=False))
        return response.output
    else:
        print('Code: %d, status: %s, message: %s' % (response.status_code, response.code, response.message))
        return response.status_code