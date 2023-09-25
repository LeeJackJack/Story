import json
import zhipuai
import os
import controllers.game_controller as game_controller
# from controllers.game_controller import get_game, edit_game
from dotenv import load_dotenv
import json
import re
from flask import Response


load_dotenv()  # 加载 .env 文件中的变量

zhipuai.api_key = os.environ['QINGHUA_API_KEY']


# 随机换一换剧情
def get_random_plot(game_id):
    game = game_controller.get_game(id=game_id)
    content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        'content': f'换一换'

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

    json_match = re.search(r'\{.*?\}', full_text, re.DOTALL)
    json_content = json_match.group(0)

    new_response = {
        'role': 'assistant',
        'content': json_content
    }
    prompt.append(new_response)
    content[-1] = json.loads(json_content)
    # 保存最新生成内容到game
    result = game_controller.edit_game(id=game_id, prompt_history=json.dumps(prompt,ensure_ascii=False),
                       content=json.dumps(content,ensure_ascii=False))

    return result


# 提交选项并更新剧情
def submit_plot_choice(game_id, choice):
    game = game_controller.get_game(id=game_id)
    content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        'content': choice
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

    json_match = re.search(r'\{.*?\}', full_text, re.DOTALL)
    json_content = json_match.group(0)

    new_response = {
        'role': 'assistant',
        'content': json_content
    }
    prompt.append(new_response)
    content.append(json.loads(json_content))
    # 保存最新生成内容到game
    result = game_controller.edit_game(id=game_id, prompt_history=json.dumps(prompt, ensure_ascii=False),
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
        temperature=0.7,
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


def create_plot(choice, game_id):
    game = game_controller.get_game(id=game_id)
    game_content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        'content': f'自定义：{choice}'
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

    json_match = re.search(r'\{.*?\}', full_text, re.DOTALL)
    json_content = json_match.group(0)

    new_response = {
        'role': 'assistant',
        'content': json_content
    }
    prompt.append(new_response)
    game_content.append(json.loads(json_content))
    # 保存最新生成内容到game
    result = game_controller.edit_game(id=game['id'], prompt_history=json.dumps(prompt, ensure_ascii=False),
                       content=json.dumps(game_content, ensure_ascii=False))

    return result


# 初始化故事的第一话，生成故事所需要内容
def init_game_data(theme, protagonist):
    theme = json.loads(theme)
    protagonist = json.loads(protagonist)
    re_start_str = f"游戏主题：{theme['description']}，游戏主角：{protagonist['name'] + '，' + protagonist['description']}"
    prompt = [
        {"role": "user",
         "content": "我希望你扮演一个基于文本的冒险游戏，游戏主题：（稍后提供），游戏主角：（稍后提供）。如果你明白了就回复“收到”，之后我会给你介绍这个游戏的规则。"},
        {"role": "assistant",
         "content": " 收到，我已经明白了。请告诉我这个游戏的规则。"},
        {"role": "user",
         "content": "游戏总共 8 回合，每一个回合你都需要生成故事内容和a、b、c三个选项。如果你明白了就回复“收到”，之后我会给你介绍每个回合生成内容的规则。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请告诉我每个回合生成内容的规则。"},
        {"role": "user",
         "content": "每个回合都包含以下的字段，分别是：回合数，章节名，故事内容，故事选项。如果你明白了就回复“收到”，之后我会给你介绍每个字段的规则。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请告诉我每个字段的规则。"},
        {"role": "user",
         "content": "1、回合数：记录当前回合数，整数类型，从0开始增加，到8终止；2、章节名：记录当前章节名字，枚举类型，分别是：故事的开端，情节推进，矛盾产生，关键决策，情节发展，高潮冲突，结局逼近，最终结局，章节名分别与回合数一一对应，回合1对应故事的开端，回合2对应情节推进，回合3对应矛盾产生，回合4对应关键决策，回合5对应情节发展，回合6对应高潮冲突，回合7对应结局逼近，回合8对应最终结局；3、故事内容：根据当前章节名的剧情提示，生成与上一个回合内容及选项相关的故事内容；4、故事选项：根据当前故事内容，生成3个相关的会影响故事发展的选项；如果你明白了就回复“收到”，之后我会给你介绍这个游戏的玩法。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请告诉我这个游戏的玩法。"},
        {"role": "user",
         "content": "1、你需要根据我提供的游戏主题和游戏主角，先生成第一回合的所有内容给我；2、如果我回复游戏选项里的其中一个，你需要根据我回复的选项，生成下一个回合的所有内容给我；3、如果我回复“自定义”，你需要根据我回复的自定义内容，生成下一个回合的所有内容给我；4、如果我回复“换一换”，你需要重新生成当前回合的所有内容给我；如果你明白了就回复“收到”，之后我会给你介绍这个游戏的限制。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请告诉我这个游戏的限制。"},
        {"role": "user",
         "content": "1、每个回合的故事内容必须控制在 80 字以内，游戏在第8回合结束；2、你给我生成的故事内容和故事选项需要是有趣搞怪一点的，前后逻辑有联系的，不要太拘泥于常规的内容，虚幻，古代，现实的题材都可以；3、每个回合的情节结构必须和章节名对应，8个回合8个情节循序渐进，缺一不可；如果你明白了就回复“收到”，之后我会给你介绍你回复的格式要求。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请告诉我回复的格式要求。"},
        {"role": "user",
         "content": "回复的格式必须要json格式，key的对应关系如下：round对应回合数，chapter对应章节名，content对应故事内容，choice对应故事选项；参考示例：{\"round\":\"xxx\",\"chapter\":\"xxx\",\"content\":\"xxx\",\"choice\":[\"a.xxx\",\"b.xxx\",\"c.xxx\"]}；如果你明白了就回复“收到”，之后我就会给你发送游戏主题和游戏主角，然后游戏开始。"},
        {"role": "assistant",
         "content": "收到，我已经明白了。请发送游戏主题和游戏主角，我将开始游戏。"},
        {"role": "user",
         "content": re_start_str}]
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
            meta_info = event.meta
        elif event.event == "error" or event.event == "interrupted":
            print('Error or interrupted:', event.data)
        else:
            print('Unknown event:', event.data)

    json_match = re.search(r'\{.*?\}', full_text, re.DOTALL)
    json_content = json_match.group(0)

    prompt_history = [
        {'role': 'assistant',
         'content': json_content}]

    return prompt+prompt_history


def test_fake_init():
    prompt = [
        {"role":"user","content":"{\"round\":\"xxx\",\"chapter\":\"xxx\",\"content\":\"xxx\",\"choice\":[\"a.xxx\",\"b.xxx\",\"c.xxx\"]}上述这段json格式，我希望后续你的所有回复，都遵循这个格式，其中key必须保持与上述一致。如果你明白了就回复收到。之后我再告诉你xxx的地方的内容怎么创作"},
        {"role":"assistant","content":" 收到，我已经理解了您提供的 JSON 格式，后续的回复将会遵循这个格式。请在您指定的 key 位置提供对应的内容，我会根据您提供的信息进行回复。"},
        {"role":"user","content":"1、我希望你扮演一个基于文本的打工奋斗游戏（游戏主题：主角通过养猪艰难致富的故事，故事主角：张天师）；2、你要基于游戏主题，游戏主角，创建8个回合的游戏，你将回复故事情节内容描述及 3 个选项；3、你需要首先给我第一个场景及情节描述，并给我提供 3 个选项；4、如果我回复“换一换”，则重新生成当前回合的故事情节内容描述及选项（round、chapter不变，content及choice内容重新生成）；5、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；6、如果我回复“自定义”，则根据“自定义”的内容继续生成下一回合内容（round、chapter、content及choice改变，根据自定义内容生成下一回合所需内容）；7、每个回合的故事情节描述必须控制在 80 字以内。故事需要在第八回合结束（在round:8,chapter:最终结局时结束）；8、故事的八个回合的情节结构分别是：故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，八个情节按此顺序逐层递进，缺一不可；9、你给我的故事情节描述需要非常有趣好玩，可以带悬疑解密，也可以搞怪搞笑，前后逻辑有联系；10、你返回给我的内容包含如下：1）round：回合数，是整数，从 1 开始递增，1代表第一回合，2代表第二回合，以此类推；如果回复“换一换”则保持不变（继续在当前回合）；2）chapter：章节名，枚举值，故事的开端（round:1,chapter:故事的开端）、情节推进（round:2,chapter:情节推进）、矛盾产生（round:3,chapter:矛盾产生）、关键决策（（round:4,chapter:关键决策））、情节发展（（round:5,chapter:情节发展））、高潮冲突（round:6,chapter:高潮冲突）、结局逼近（round:7,chapter:解决逼近）、最终结局（round:8,chapter:最终结局）；3）content：具体的故事情节描述内容；"},
        {"role":"assistant","content":"{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"张天师在养猪场工作，立志成为养猪大户。某天，他在清理猪圈时发现了一本神秘的养猪秘籍，决定研究其中的奥秘以提高养猪技术。\",\"choice\":[\"a.研究秘籍\",\"b.忽略秘籍\",\"c.卖出秘籍\"]}"},
        {"role":"user","content":"你给出的选项还不够有趣，你可以发散一下，不要太拘泥于常规的内容"},
        {"role":"assistant","content":"{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"张天师在养猪场工作，立志成为养猪大户。某天，他在清理猪圈时发现了一本神秘的养猪秘籍，决定研究其中的奥秘以提高养猪技术。\",\"choice\":[\"a.研究秘籍\",\"b.把秘籍拿去复印卖钱\",\"c.因不识字把秘籍烧了\"]}"},
        {"role":"user","content":"下面就按照这种有趣程度生成故事。现在我重新给你故事主题和故事主角，重新开始游戏。故事主题：黄飞鸿打战十三姨，故事主角：房飞冯"}]
    response = zhipuai.model_api.invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=0.7,
        top_p=0.7,
    )

    return response

