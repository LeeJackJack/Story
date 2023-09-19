# game_controller.py
from database.models import Game, db, Protagonist, AlbumTheme
from typing import Optional, Dict, Any
import json
from datetime import datetime
# from generate.qinghua_completions import init_game_plot
import generate.qinghua_completions as gpt_completions


def add_game(user_id, protagonist_id, theme_id,
             content=None, prompt_history=None):
    # 获取主角信息
    protagonist_query = Protagonist.query
    protagonist_query = protagonist_query.filter_by(id=protagonist_id, valid='1')
    protagonist = protagonist_query.first()

    # 获取故事主题信息
    theme_query = AlbumTheme.query
    theme_query = theme_query.filter_by(id=theme_id, valid='1')
    theme = theme_query.first()

    gpt = gpt_completions.init_game_plot(protagonist.name)
    # print(gpt['add'])
    new_content = json.loads(gpt['add'])
    new_prompt_history = [{
        'role': 'user',
        'content': f"1、我希望你扮演一个基于文本的冒险游戏（游戏背景：{theme.theme}，游戏主角：{protagonist.name + '，' +protagonist.description}，故事概述：{theme.description}）；"
                   "2、你要基于游戏背景，游戏主角及故事描述，创建8个回合的游戏，你将回复故事情节内容描述及 3 个选项；"
                   "3、你需要首先给我第一个场景及情节描述，并给我提供 3 个选项；"
                   "4、如果我回复“换一换”，则重新生成当前回合的故事情节内容描述及选项（round、chapter不变，content及choice内容重新生成）；"
                   "5、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容（round、chapter、content及choice改变，根据选项生成下一回合所需内容）；"
                   "6、如果我回复“自定义”，则根据“自定义”的内容继续生成下一回合内容（round、chapter、content及choice改变，根据自定义内容生成下一回合所需内容）；"
                   "7、每个回合的故事情节描述必须控制在 80 字以内。故事需要在第八回合结束（在round:8,chapter:最终结局时结束）；"
                   "8、故事的八个回合的情节结构分别是：故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，八个情节按此顺序逐层递进，缺一不可；"
                   "9、你给我的故事情节描述需要非常有趣好玩，可以带悬疑解密，也可以搞怪搞笑，前后逻辑有联系；"
                   "10、你返回给我的内容包含如下："
                   "1）round：回合数，是整数，从 1 开始递增，1代表第一回合，2代表第二回合，以此类推；如果回复“换一换”则保持不变（继续在当前回合）；"
                   "2）chapter：章节名，枚举值，故事的开端（round:1,chapter:故事的开端）、情节推进（round:2,chapter:情节推进）、"
                   "矛盾产生（round:3,chapter:矛盾产生）、关键决策（（round:4,chapter:关键决策））、情节发展（（round:5,chapter:情节发展））、"
                   "高潮冲突（round:6,chapter:高潮冲突）、结局逼近（round:7,chapter:解决逼近）、最终结局（round:8,chapter:最终结局）；"
                   "3）content：具体的故事情节描述内容；"
                   "11、返回的内容输出成 json 的格式，健值对参考上述序号9的内容（注意：你输出的内容只需要 json 格式返回，其他格式内容不需要返回）；"
                   "12、注意，请严格按照下面示例的格式输出（仅参考输出格式，内容请严格按照上述 1-10 点要求创作），示例如下："
                   "{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你收到了霍格沃茨的入学通知书，搭乘霍格沃茨特快列车来到"
                   "了这所神秘的魔法学校。列车穿过山峦和森林，最后抵达了你的目的地。远远望去，霍格沃茨魔法学校屹立在一座高高的山顶上，"
                   "城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，跟随其他新生一起走下列车，准备进入学校开始新的魔法"
                   "生活。\",\"choice\":[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}"
                   "13、输出之前，请仔细检查一次是否均满足上述所说的 12 条规则再输出。"
    },{
        'role': 'assistant',
        'content': gpt['add']
    }]

    # # 如果content和prompt_history没有提供，使用默认值
    # if content is None:
    #     content = [
    #         {
    #             "round": 1,
    #             "chapter": "故事的开端",
    #             "content": f"{protagonist.name}是一位年轻的勇者，他听说白雪公主被邪恶的巨龙抓走了，于是决定去拯救她。他带着他的弓和箭，开始了这段冒险之旅。"
    #                        "他穿过一片阴暗的森林，攀过了险峻的山峰，最后来到了巨龙的巢穴。他看到白雪公主被囚禁在一个坚固的笼子里，他决定救她出来。",
    #             "choice": ["a. 使用魔法攻击巨龙", "b. 偷偷寻找巨龙的弱点", "c. 用食物引开巨龙"]
    #         }
    #     ]
    #
    # if prompt_history is None:
    #     prompt_history = [{"role": "user", "content": f"1、 我希望你扮演一个基于文本的冒险游戏（ 游戏主题： {protagonist.name}拯救白雪公主的故事，"
    #                                                   f"主角： {protagonist.name}）； 2、游戏总共8回合，你将回复故事情节内容描述及3个选项。"
    #                                                   "您将回复故事情节内容的描述；3、你需要首先给我第一个场景及情节描述，"
    #                                                   "并给我提供3个选项；4、如果我回复选项中的其中一个（选项序号），"
    #                                                   "则继续生成下一回合内容；5、如果我回复换“换一换”，则重新生成当前回合的故事"
    #                                                   "情节内容描述及选项；6、每个回合的故事情节必须控制在80字以内。故事需要在八"
    #                                                   "个回合内结束；7、故事的8个情节结构分别是故事的开端、情节推进、矛盾产生、"
    #                                                   "关键决策、情节发展、高潮冲突、结局逼近、最终结局，8个情节按此顺序逐层递进；"
    #                                                   "8、你给我的情节需要有趣好玩，适合儿童阅读，前后逻辑有联系；"
    #                                                   "9、你返回给我的内容包含如下：1）round：是整数，从1开始递增，如果“换一换”"
    #                                                   "则保持不变；2）chapter：枚举值：分别是故事的开端、情节推进、矛盾产生、"
    #                                                   "关键决策、情节发展、高潮冲突、结局逼近、最终结局；3）content：具体的故"
    #                                                   "事情节描述内容；4）choice： 故事对应的3个选项，用a、b、c英文字母序号开"
    #                                                   "头（故事的最后一个回合最后一话不提供选项选择）10、返回的内容封装成json"
    #                                                   "的格式，健值对参考上述序号9的内容（只需要json格式返回，其他格式内容不需"
    #                                                   "要返回）11、注意，请严格按照下面示例的格式，内容请按照上述1-10点要求创作，"
    #                                                   "示例：{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你"
    #                                                   "收到了霍格沃茨的入学通知书，搭乘霍格沃茨特快列车来到了这所神秘的魔法学校。"
    #                                                   "列车穿过山峦和森林，最后抵达了你的目的地。远远望去，霍格沃茨魔法学校屹立在"
    #                                                   "一座高高的山顶上，城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，"
    #                                                   "跟随其他新生一起走下列车，准备进入学校开始新的魔法生活。\",\"choice\":"
    #                                                   "[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}"
    #                                                   ""}, {"role": "assistant", "content": "{\"round\":1,\"chapter\""
    #                                                                                         ":\"故事的开端\",\"content\":"
    #                                                                                         "\"人杰是一位年轻的勇者，他听说"
    #                                                                                         "白雪公主被邪恶的巨龙抓走了，"
    #                                                                                         "于是决定去拯救她。他带着他的剑"
    #                                                                                         "和盾牌，开始了这段冒险之旅。"
    #                                                                                         "他穿过了森林，越过了山脉，"
    #                                                                                         "最后来到了巨龙的巢穴。他看到"
    #                                                                                         "白雪公主被囚禁在一个笼子里，"
    #                                                                                         "他决定救她出来。\",\"cho"
    #                                                                                         "ice\":[\"a. 直接攻击"
    #                                                                                         "巨龙\",\"b. 先找到"
    #                                                                                         "巨龙的弱点\",\"c. 用食物引开巨龙\"]}"}]
    #
    # 创建新的Game对象
    new_game = Game(
        user_id=user_id,
        protagonist_id=protagonist_id,
        theme_id=theme_id,
        content=json.dumps([new_content],ensure_ascii=False),  # 序列化为JSON字符串
        prompt_history=json.dumps(new_prompt_history,ensure_ascii=False),  # 序列化为JSON字符串
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        valid=True,
        if_finish=False
    )

    # 添加到数据库
    db.session.add(new_game)
    db.session.commit()

    # 返回新创建的游戏的ID
    return new_game.id


def get_game(id: int) -> dict:
    game_query = Game.query
    if id:
        game_query = game_query.filter_by(id=id, valid='1')

    game = game_query.first()

    # 根据查询结果返回相应的值
    if game:
        return {
            "id": game.id,
            "user_id": game.user_id,
            "theme_id": game.theme_id,
            "protagonist_id": game.protagonist_id,
            "content": game.content,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
            "valid": game.valid,
            "if_finish": game.if_finish,
            "prompt_history": game.prompt_history,
        }
    else:
        return {}


def edit_game(id: int,
              user_id: Optional[int] = None,
              protagonist_id: Optional[int] = None,
              theme_id: Optional[int] = None,
              content: Optional[str] = None,
              if_finish: Optional[str] = None,
              prompt_history: Optional[str] = None) -> Dict[str, Any]:
    game_query = Game.query
    if id:
        game_query = game_query.filter_by(id=id, valid='1')

    game = game_query.first()

    # 根据查询结果返回相应的值
    if game:
        if user_id:
            game.user_id = user_id
        if protagonist_id:
            game.protagonist_id = protagonist_id
        if theme_id:
            game.theme_id = theme_id
        if if_finish:
            game.if_finish = if_finish
        if content:
            game.content = content
        if prompt_history:
            game.prompt_history = prompt_history

        db.session.commit()

        return {
            "id": game.id,
            "user_id": game.user_id,
            "theme_id": game.theme_id,
            "protagonist_id": game.protagonist_id,
            "content": game.content,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
            "valid": game.valid,
            "if_finish": game.if_finish,
            "prompt_history": game.prompt_history,
        }
    else:
        return {}


def del_game():
    return ''


def reset_game_plot(game_id):
    game_query = Game.query
    if game_id:
        game_query = game_query.filter_by(id=game_id, valid='1')

    game = game_query.first()

    # 根据查询结果返回相应的值
    if game:
        content_arr = json.loads(game.content)
        prompt_history_arr = json.loads(game.prompt_history)
        # print(content_arr)
        # print(prompt_history_arr)
        game.content = json.dumps([content_arr[0]], ensure_ascii=False)
        game.prompt_history = json.dumps(prompt_history_arr[:2], ensure_ascii=False)

        db.session.commit()

        return {
            "id": game.id,
            "user_id": game.user_id,
            "theme_id": game.theme_id,
            "protagonist_id": game.protagonist_id,
            "content": game.content,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
            "valid": game.valid,
            "if_finish": game.if_finish,
            "prompt_history": game.prompt_history,
        }
    else:
        return {}


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except json.JSONDecodeError:
        return False
    return True