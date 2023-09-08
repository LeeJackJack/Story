# game_controller.py
from database.models import Game, db
from typing import Optional, Dict, Any
import json
from datetime import datetime


from datetime import datetime
import json  # 用于序列化和反序列化JSON数据

def add_game(user_id, protagonist_id, theme_id=None, 
             content=None, prompt_history=None):
    """
    添加新游戏到数据库。
    
    参数:
        user_id (int): 用户ID
        protagonist_id (int): 主角ID
        theme_id (int): 主题ID
        content (list): 故事内容，默认为None
        prompt_history (list): 提示历史，默认为None
        
    返回:
        int: 新创建的游戏的ID
    """
    # 如果content和prompt_history没有提供，使用默认值
    if content is None:
        content = [
            {
                "round": 1, 
                "chapter": "故事的开端", 
                "content": "人杰是一位年轻的勇者，他听说白雪公主被邪恶的巨龙抓走了，于是决定去拯救她。他带着他的弓和箭，开始了这段冒险之旅。他穿过一片阴暗的森林，攀过了险峻的山峰，最后来到了巨龙的巢穴。他看到白雪公主被囚禁在一个坚固的笼子里，他决定救她出来。",
                "choice": ["a. 使用魔法攻击巨龙", "b. 偷偷寻找巨龙的弱点", "c. 用食物引开巨龙"]
            }
        ]
    
    if prompt_history is None:
        prompt_history = [
            {
                "role": "user",
                "content": "1、 我希望你扮演一个基于文本的冒险游戏（ 游戏主题： 王子拯救白雪公主的故事， 主角： 勇者人杰）； 2、游戏总共8回合，你将回复故事情节内容描述及3个选项。您将回复故事情节内容的描述；3、你需要首先给我第一个场景及情节描述，并给我提供3个选项；4、如果我回复选项中的其中一个（选项序号），则继续生成下一回合内容；5、如果我回复换“换一换”，则重新生成当前回合的故事情节内容描述及选项；6、每个回合的故事情节必须控制在80字以内。故事需要在八个回合内结束；7、故事的8个情节结构分别是故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局，8个情节按此顺序逐层递进；8、你给我的情节需要有趣好玩，适合儿童阅读，前后逻辑有联系；9、你返回给我的内容包含如下：1）round：是整数，从1开始递增，如果“换一换”则保持不变；2）chapter：枚举值：分别是故事的开端、情节推进、矛盾产生、关键决策、情节发展、高潮冲突、结局逼近、最终结局；3）content：具体的故事情节描述内容；4）choice： 故事对应的3个选项，用a、b、c英文字母序号开头（故事的最后一个回合最后一话不提供选项选择）10、返回的内容封装成json的格式，健值对参考上述序号9的内容（只需要json格式返回，其他格式内容不需要返回）11、注意，请严格按照下面示例的格式，内容请按照上述1-10点要求创作，示例：{\"round\":1,\"chapter\":\"故事的开端\",\"content\":\"你收到了霍格沃茨的入学通知书，搭乘霍格沃茨特快列车来到了这所神秘的魔法学校。列车穿过山峦和森林，最后抵达了你的目的地。远远望去，霍格沃茨魔法学校屹立在一座高高的山顶上，城堡式的建筑气势恢宏，令人叹为观止。你怀揣着激动的心情，跟随其他新生一起走下列车，准备进入学校开始新的魔法生活。\",\"choice\":[\"a. 走进学校大门\",\"b. 先去参观大礼堂\",\"c. 沿着湖边小路走\"]}"
            }
            ]
    
    # 创建新的Game对象
    new_game = Game(
        user_id=user_id,
        protagonist_id=protagonist_id,
        theme_id=theme_id,
        content=json.dumps(content),  # 序列化为JSON字符串
        prompt_history=json.dumps(prompt_history),  # 序列化为JSON字符串
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