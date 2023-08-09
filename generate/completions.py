import requests
from dotenv import load_dotenv
import os


def get_lan_response(prompt):
    load_dotenv()
    api_key = os.environ['GPT_KEY']
    url = os.environ['OPEN_AI_HOST']
    model = os.environ['OPEN_AI_MODEL']

    message_content = ''
    prompt = '尝试描述一下一张图片的内容，内容可以丰富一点，包括人物，场景，天气，颜色，气氛等等，控制在100字以内，用英语表达。' \
             '例子：expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots ' \
             'towering under a blue alien sky, masterful, ghibli'

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

        # 判断response是否包含所需的字段
        if 'choices' in response_data and len(response_data['choices']) > 0:
            message_content = response_data['choices'][0]['message']['content']
            # print(f"Reply: {message_content}")

    except requests.RequestException as error:
        print(f"Error occurred: {error}")

    return message_content
