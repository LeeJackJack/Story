import requests
from dotenv import load_dotenv
import os


def get_lan_response():
    load_dotenv()
    api_key = os.environ['GPT_KEY']
    url = os.environ['OPEN_AI_HOST']
    model = os.environ['OPEN_AI_MODEL']
    chapter = []

    message_content = ''
    # prompt = '尝试描述一下一张图片的内容，内容可以丰富一点，包括人物，场景，天气，颜色，气氛等等，控制在100字以内，用英语表达。' \
    #          '例子：expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots ' \
    #          'towering under a blue alien sky, masterful, ghibli'

    prompt = '1、需要生成一个儿童绘本故事主人公。首先给我明确一下故事的主人公，主人公可以是动物，' \
             '也可以是人物，如：一个名叫lily的小女孩。或一只小白兔。参考例子{content:一只小白兔}或者{content:一只小象}' \
             '2、主人公需要拥有姓名，种族，特质3样属性。参考例子{name:lily,type:兔子,traits：可爱}' \
             '3、需要有一段话描述一个画面，主人公在画面中，用于给其他系统理解这是一副什么样的画面，需要用英语表达。参考例子' \
             '{img:expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots' \
             'towering under a blue alien sky, masterful, ghibli}' \
             '4、按照上述参考例子格式，更改一下内容，并且组装成一个标准化json进行输出{content:xxxx,name:xxxx,type:xxxx,traits:xxxx,img:xxxx}'

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    url = url

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        # 打印完整的响应
        print(response_data)

        # 判断response是否包含所需的字段
        if 'choices' in response_data and len(response_data['choices']) > 0:
            message_content = response_data['choices'][0]['message']['content']

    except requests.RequestException as error:
        print(f"Error occurred: {error}")

    return message_content
