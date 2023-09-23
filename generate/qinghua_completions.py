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


def init_game_plot(protagonist_name):
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=f"1、我希望你扮演一个基于文本的冒险游戏（游戏主题：{protagonist_name}奇幻历险记，主角：{protagonist_name}）；"
               "2、游戏总共 8 回合，你将回复故事情节内容描述及 3 个选项；"
               "3、你需要首先给我第一个场景及情节描述，并给我提供 3 个选项；"
               "4、如果我回复选项中的其中一个，则根据选项继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；"
               "5、如果我回复换“换一换”，则在当前回合重新生成故事情节内容描述及选项（round、chapter不变，重新生成content及choice内容）；"
               "6、如果我回复“自定义”，则根据“自定义”的内容继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；"
               "7、每个回合的故事情节描述必须控制在 80 字以内。故事需要在第八回合结束（在round:8,chapter:最终结局时结束）；"
               "8、故事的八个回合的情节结构分别是：故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，八个情节按此顺序逐层递进，缺一不可；"
               "9、你给我的故事情节描述需要有趣好玩，适合儿童阅读，前后逻辑有联系；"
               "10、你返回给我的内容包含如下："
               "1）round：回合数，是整数，从 1 开始递增，1代表第一回合，2代表第二回合，以此类推；如果回复“换一换”则保持不变（继续在当前回合）；"
               "2）chapter：章节名，枚举值：故事的开端（round:1,chapter:故事的开端）、情节推进（round:2,chapter:情节推进）、矛盾产生（round:3,chapter:矛盾产生）、关键决策（（round:4,chapter:关键决策））、情节发展（（round:5,chapter:情节发展））、高潮冲突（round:6,chapter:高潮冲突）、结局逼近（round:7,chapter:解决逼近）、最终结局（round:8,chapter:最终结局）；"
               "3）content：具体的故事情节描述内容；"
               "4）choice：故事对应的 3 个选项，用 a、b、c 英文字母序号开头（故事的最后一个回合不提供选项选择）；"
               "11、返回的内容输出成 json 的格式，健值对参考上述序号 10的内容（注意：你输出的内容只需要 json 格式返回，其他格式内容不需要返回）；"
               "12、注意，请严格按照下面示例的格式，内容请按照上述 1-11 点要求创作，示例如下："
               "{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你收到了霍格沃茨的入学通知书，搭乘霍格沃茨特快列车来到了这所神秘的魔法学校。列车穿过山峦和森林，最后抵达了你的目的地。远远望去，霍格沃茨魔法学校屹立在一座高高的山顶上，城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，跟随其他新生一起走下列车，准备进入学校开始新的魔法生活。\",\"choice\":[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}"
               "13、输出之前，请仔细检查一次是否均满足上述所说的 12 条规则再输出。",
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
    game = game_controller.get_game(id=game_id)
    content = json.loads(game['content'])
    chapter = ['故事的开端', '情节推进', '矛盾产生', '关键决策', '情节发展', '高潮冲突', '结局逼近', '最终结局']
    # print(content[0])
    # round_num = content[0]['round']
    prompt = json.loads(game['prompt_history'])
    new_entry = {
        'role': 'user',
        # 'content': f'换一换（round、chapter不变，重新生成content及choice内容;故事主角不变；）
        'content': f'换一换，你这个回复中内容和选项都不太有趣，再生成一次'

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
    content[-1] = json.loads(full_text)
    # 保存最新生成内容到game
    result = game_controller.edit_game(id=game_id, prompt_history=json.dumps(prompt,ensure_ascii=False),
                       content=json.dumps(content,ensure_ascii=False))

    return result


# 提交选项并更新剧情
def submit_plot_choice(game_id, choice):
    game = game_controller.get_game(id=game_id)
    content = json.loads(game['content'])
    prompt = json.loads(game['prompt_history'])
    print(prompt)
    new_entry = {
        'role': 'user',
        'content': choice
        # 你可以在这里添加其他键-值对
    }
    prompt.append(new_entry)

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

    print(full_text)

    new_response = {
        'role': 'assistant',
        'content': full_text
    }
    prompt.append(new_response)
    # print(full_text)
    content.append(json.loads(full_text))
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
    # print(round_final)
    chapter_final = new_chapter[round_num]['chapter']

    game = game_controller.get_game(id=game_id)
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
    result = game_controller.edit_game(id=game['id'], prompt_history=json.dumps(prompt, ensure_ascii=False),
                       content=json.dumps(game_content, ensure_ascii=False))

    return result


# 初始化故事的第一话，生成故事所需要内容
def init_game_data(theme, protagonist):
    theme = json.loads(theme)
    protagonist = json.loads(protagonist)
    re_start_str = f"下面就按照这种有趣程度生成故事。现在我重新给你故事主题和故事主角，重新开始游戏。故事主题：{theme['description']}，故事主角：{protagonist['name'] + '，' + protagonist['description']}"
    prompt = [
        {"role": "user",
         "content": "{\"round\":\"xxx\",\"chapter\":\"xxx\",\"content\":\"xxx\",\"choice\":[\"a.xxx\",\"b.xxx\",\"c.xxx\"]}上述这段json格式，我希望后续你的所有回复，都遵循这个格式，其中key必须保持与上述一致。如果你明白了就回复收到。之后我再告诉你xxx的地方的内容怎么创作"},
        {"role": "assistant",
         "content": " 收到，我已经理解了您提供的 JSON 格式，后续的回复将会遵循这个格式。请在您指定的 key 位置提供对应的内容，我会根据您提供的信息进行回复。"},
        {"role": "user",
         "content": "1、我希望你扮演一个基于文本的打工奋斗游戏（游戏主题：主角通过养猪艰难致富的故事，故事主角：张天师）；2、你要基于游戏主题，游戏主角，创建8个回合的游戏，你将回复故事情节内容描述及 3 个选项；3、你需要首先给我第一个场景及情节描述，并给我提供 3 个选项；4、如果我回复“换一换”，则重新生成当前回合的故事情节内容描述及选项（round、chapter不变，content及choice内容重新生成）；5、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；6、如果我回复“自定义”，则根据“自定义”的内容继续生成下一回合内容（round、chapter、content及choice改变，根据自定义内容生成下一回合所需内容）；7、每个回合的故事情节描述必须控制在 80 字以内。故事需要在第八回合结束（在round:8,chapter:最终结局时结束）；8、故事的八个回合的情节结构分别是：故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，八个情节按此顺序逐层递进，缺一不可；9、你给我的故事情节描述需要非常有趣好玩，可以带悬疑解密，也可以搞怪搞笑，前后逻辑有联系；10、你返回给我的内容包含如下：1）round：回合数，是整数，从 1 开始递增，1代表第一回合，2代表第二回合，以此类推；如果回复“换一换”则保持不变（继续在当前回合）；2）chapter：章节名，枚举值，故事的开端（round:1,chapter:故事的开端）、情节推进（round:2,chapter:情节推进）、矛盾产生（round:3,chapter:矛盾产生）、关键决策（（round:4,chapter:关键决策））、情节发展（（round:5,chapter:情节发展））、高潮冲突（round:6,chapter:高潮冲突）、结局逼近（round:7,chapter:解决逼近）、最终结局（round:8,chapter:最终结局）；3）content：具体的故事情节描述内容；"},
        {"role": "assistant",
         "content": "{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"张天师在养猪场工作，立志成为养猪大户。某天，他在清理猪圈时发现了一本神秘的养猪秘籍，决定研究其中的奥秘以提高养猪技术。\",\"choice\":[\"a.研究秘籍\",\"b.忽略秘籍\",\"c.卖出秘籍\"]}"},
        {"role": "user", "content": "你给出的选项还不够有趣，你可以发散一下，不要太拘泥于常规的内容"},
        {"role": "assistant",
         "content": "{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"张天师在养猪场工作，立志成为养猪大户。某天，他在清理猪圈时发现了一本神秘的养猪秘籍，决定研究其中的奥秘以提高养猪技术。\",\"choice\":[\"a.研究秘籍\",\"b.把秘籍拿去复印卖钱\",\"c.因不识字把秘籍烧了\"]}"},
        {"role": "user",
         "content": re_start_str}]
    # prompt = f"1、我希望你扮演一个基于文本的{theme['theme']}游戏（游戏主题：{theme['description']}，故事主角：{protagonist['name'] + '，' + protagonist['description']}）；" \
    #          f"2、你要基于游戏背景，游戏主角及故事描述，创建8个回合的游戏，你将回复故事情节内容描述及 3 个选项；" \
    #          f"3、你需要首先给我第一个场景及情节描述，并给我提供 3 个选项；" \
    #          f"4、如果我回复“换一换”，则重新生成当前回合的故事情节内容描述及选项（round、chapter不变，content及choice内容重新生成）；" \
    #          f"5、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；" \
    #          f"6、如果我回复“自定义”，则根据“自定义”的内容继续生成下一回合内容（round、chapter、content及choice改变，根据自定义内容生成下一回合所需内容）；" \
    #          f"7、每个回合的故事情节描述必须控制在 80 字以内。故事需要在第八回合结束（在round:8,chapter:最终结局时结束）；" \
    #          f"8、故事的八个回合的情节结构分别是：故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，八个情节按此顺序逐层递进，缺一不可；" \
    #          f"9、你给我的故事情节描述需要非常有趣好玩，可以带悬疑解密，也可以搞怪搞笑，前后逻辑有联系；" \
    #          f"10、你返回给我的内容包含如下：1）round：回合数，是整数，从 1 开始递增，1代表第一回合，2代表第二回合，以此类推；如果回复“换一换”则保持不变（继续在当前回合）；" \
    #          f"2）chapter：章节名，枚举值，故事的开端（round:1,chapter:故事的开端）、情节推进（round:2,chapter:情节推进）、" \
    #          f"矛盾产生（round:3,chapter:矛盾产生）、关键决策（（round:4,chapter:关键决策））、情节发展（（round:5,chapter:情节发展））、" \
    #          f"高潮冲突（round:6,chapter:高潮冲突）、结局逼近（round:7,chapter:解决逼近）、最终结局（round:8,chapter:最终结局）；" \
    #          f"3）content：具体的故事情节描述内容；" \
    #          f"11、返回的内容输出成 json 的格式，健值对参考上述序号9的内容（注意：你输出的内容只需要 json 格式返回，其他格式内容不需要返回）；" \
    #          "12、注意，请严格按照下面示例的格式输出（仅参考输出格式，内容请严格按照上述 1-10 点要求创作），示例如下：{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你收到了霍格沃茨的入学通知书，搭乘霍格沃茨特快列车来到了这所神秘的魔法学校。列车穿过山峦和森林，最后抵达了你的目的地。远远望去，霍格沃茨魔法学校屹立在一座高高的山顶上，城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，跟随其他新生一起走下列车，准备进入学校开始新的魔法生活。\",\"choice\":[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}" \
    #          f"13、输出之前，请仔细检查一次是否均满足上述所说的 12 条规则再输出。"
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=0.9,
        top_p=1,
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

    # print(full_text)
    json_match = re.search(r'\{.*?\}', full_text, re.DOTALL)
    # print(json_match)
    json_content = json_match.group(0)
    # print(json_content)

    prompt_history = [
        {
        'role': 'assistant',
        'content': json_content
    }]
    # print(json.loads(prompt+prompt_history))

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
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_pro",
        prompt=prompt,
        temperature=0.9,
        top_p=1,
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

    return json_content
