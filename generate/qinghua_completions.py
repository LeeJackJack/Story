import json
import zhipuai
import os
from controllers.game_controller import get_game, edit_game
from dotenv import load_dotenv
import json


load_dotenv()  # 加载 .env 文件中的变量

zhipuai.api_key = os.environ['QINGHUA_API_KEY']


def init_game_plot():
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt="1、 我希望你扮演一个基于文本的冒险游戏（ 游戏主题： 王子拯救白雪公主的故事， 主角： 勇者人杰）； "
               "2、游戏总共8回合，你将回复故事情节内容描述及3个选项。您将回复故事情节内容的描述；"
               "3、你需要首先给我第一个场景及情节描述，并给我提供3个选项；"
               "4、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容；"
               "5、如果我回复换“换一换”，则重新生成当前回合的故事情节内容描述及选项；"
               "6、每个回合的故事情节必须控制在80字以内。故事需要在八个回合内结束；"
               "7、故事的8个情节结构分别是故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，"
               "8个情节按此顺序逐层递进；8、你给我的情节需要有趣好玩，适合儿童阅读，前后逻辑有联系；"
               "9、你返回给我的内容包含如下：1）round：是整数，从1开始递增，如果“换一换”则保持不变；"
               "2）chapter：枚举值：分别是故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局；"
               "3）content：具体的故事情节描述内容；"
               "4）choice： 故事对应的3个选项，用a、b、c英文字母序号开头（故事的最后一个回合最后一话不提供选项选择）"
               "10、返回的内容封装成json的格式，健值对参考上述序号9的内容（只需要json格式返回，其他格式内容不需要返回）"
               "11、注意，请严格按照下面示例的格式，内容请按照上述1-10点要求创作，"
               "示例：{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你收到了霍格沃茨的入学通知书，"
               "搭乘霍格沃茨特快列车来到了这所神秘的魔法学校。列车穿过山峦和森林，最后抵达了你的目的地。远远望去，"
               "霍格沃茨魔法学校屹立在一座高高的山顶上，城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，跟随其他新生一起走下列车，"
               "准备进入学校开始新的魔法生活。\",\"choice\":[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}",
        temperature=1,
        top_p=0.7,
        incremental=True
    )
    result = {}
    full_text = ""
    meta_info = {}

    for event in response.events():
        if event.event == "add":
            full_text += event.data
        elif event.event == "finish":
            meta_info = event.meta  # 假设 event.meta 是一个字典，包含了 "task_status"、"usage" 等字段
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)

    result['add'] = full_text
    result['meta_info'] = meta_info  # 添加 meta_info 到结果中

    return result


# 随机换一换剧情
def get_random_plot(game_id):
    game = get_game(id=game_id)
    content = json.loads(game['content'])
    # print(content[0])
    round_num = content[0]['round']
    chapter = content[0]['chapter']
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        'content': f'换一换，保留round:{round_num},chapter:{chapter};content与choice内容重新生成，不能和之前的重复'
        # 你可以在这里添加其他键-值对
    }
    prompt.append(new_entry)
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=1,
        top_p=0.7,
        incremental=True
    )
    full_text = ""

    for event in response.events():
        if event.event == "add":
            full_text += event.data
        elif event.event == "finish":
            meta_info = event.meta  # 假设 event.meta 是一个字典，包含了 "task_status"、"usage" 等字段
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)

    new_response = {
        'role': 'assistant',
        'content': full_text
    }
    prompt.append(new_response)
    content[-1] = json.loads(full_text)
    # 保存最新生成内容到game
    result = edit_game(id=game_id, prompt_history=json.dumps(prompt,ensure_ascii=False),
                       content=json.dumps(content,ensure_ascii=False))

    return result


# 提交选项并更新剧情
def submit_plot_choice(game_id, choice):
    game = get_game(id=game_id)
    content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        'content': choice
        # 你可以在这里添加其他键-值对
    }
    prompt.append(new_entry)

    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=1,
        top_p=0.7,
        incremental=True
    )
    full_text = ""

    for event in response.events():
        if event.event == "add":
            full_text += event.data
        elif event.event == "finish":
            meta_info = event.meta  # 假设 event.meta 是一个字典，包含了 "task_status"、"usage" 等字段
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)

    new_response = {
        'role': 'assistant',
        'content': full_text
    }
    prompt.append(new_response)
    # print(full_text)
    content.append(json.loads(full_text))
    # 保存最新生成内容到game
    result = edit_game(id=game_id, prompt_history=json.dumps(prompt, ensure_ascii=False),
                       content=json.dumps(content, ensure_ascii=False))

    return result


# 获取创建图片的描述语
def create_img_prompt(content):
    prompt = f"1、故事内容原文{content}" \
             f"2、现在你是一个对接ai生图模型的角色，根据上述content的故事描述及choice内容，想象一个图片画面来表达。" \
             f"3、图片画面尽量丰富，故事内容强相关。然后你需要把这个画面用文字来表达出来，让ai生图模型能看得懂。" \
             f"4、注意，你只需要输出一段话即可，不超过100个字。" \
             f"5、描述示例：a boy stands against a scaly dragon in a mysterious lair, aiming to rescue a terrified Snow " \
             f"White,The scene is filled with a mix of sunlight and torchlight, surrounded by dense forests"

    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=0.9,
        top_p=0.7,
        incremental=True
    )
    full_text = ""

    for event in response.events():
        if event.event == "add":
            full_text += event.data
        elif event.event == "finish":
            meta_info = event.meta  # 假设 event.meta 是一个字典，包含了 "task_status"、"usage" 等字段
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)
    # print(full_text)
    return full_text


def create_plot(content, choice, game_id):
    new_chapter = [{'round': '1', 'chapter': '故事的开端'}, {'round': '2', 'chapter': '情节推进'},
                   {'round': '3', 'chapter': '矛盾产生'}, {'round': '4', 'chapter': '关键决策'},
                   {'round': '5', 'chapter': '情节发展'}, {'round': '6', 'chapter': '高潮冲突'},
                   {'round': '7', 'chapter': '结局逼近'}, {'round': '8', 'chapter': '最终结局'}]
    round_num = json.loads(content)['round']
    round_final = new_chapter[round_num]['round']
    print(round_final)
    chapter_final = new_chapter[round_num]['chapter']

    game = get_game(id=game_id)
    game_content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    if round_num == 7:
        new_entry = {
            'role': 'user',
            'content': f'自定义：{choice}，进入round：{round_final}，chapter：{chapter_final},故事结局不用提供choice用户选择'
            # 你可以在这里添加其他键-值对
        }
    else:
        new_entry = {
            'role': 'user',
            'content': f'自定义：{choice}，进入round：{round_final}，chapter：{chapter_final}'
            # 你可以在这里添加其他键-值对
        }
    prompt.append(new_entry)
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=0.9,
        top_p=0.7,
        incremental=True
    )
    full_text = ""

    for event in response.events():
        if event.event == "add":
            full_text += event.data
        elif event.event == "finish":
            meta_info = event.meta  # 假设 event.meta 是一个字典，包含了 "task_status"、"usage" 等字段
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)

    new_response = {
        'role': 'assistant',
        'content': full_text
    }
    prompt.append(new_response)
    game_content.append(json.loads(full_text))
    # 保存最新生成内容到game
    result = edit_game(id=game['id'], prompt_history=json.dumps(prompt, ensure_ascii=False),
                       content=json.dumps(game_content, ensure_ascii=False))

    return result
