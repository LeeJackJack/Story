import os
from flask import request, url_for
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
from dotenv import load_dotenv
import random
import warnings
from datetime import datetime
from generate.image_to_image import generate_and_stream as img2img
from tools.upscale import upscale_pic
from tools.ali_oss import upload_pic
from controllers.image_controller import add_image
from controllers.protagonist_image_controller import add_protagonist_image
from app_instance import app


load_dotenv()
engine_id = os.environ['ENGINE_ID']
api_host = os.environ['API_HOST']
api_key = os.environ['STABILITY_KEY']

# sd参数
random_seed = random.randint(100_000_000, 999_999_999)
steps = 30
cfg_scale = 8.0
width = int(eval(os.environ['IMAGE_WIDTH']))
height = int(eval(os.environ['IMAGE_HEIGHT']))
samples = 3
sampler = generation.SAMPLER_K_DPMPP_2M
style_preset = 'pixel-art'


def test_generate_and_stream():
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    # prompt = request.json.get('prompt')
    prompt = "a young hero, brandishing a sword and shield, stands before a massive dragon's lair, determined to " \
             "rescue the captured Snow White. The scene is filled with an eerie atmosphere, surrounded by the " \
             "darkness of the lair and the light of the hero's determination.,master piece,cg,4k,best quality,"
    # print(prompt)

    answers = stability_api.generate(
        # prompt=prompt,
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=1,
        sampler=sampler,
        style_preset=style_preset,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = 'out/' + datetime_string
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                generate_result = upload_pic(img_path, dir_url)

                yield f"Upscale Image generated successfully! FI-URL: {generate_result}\n"

    yield "done"


def generate_and_stream(prompt):
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    # prompt = request.json.get('prompt')
    prompt = "Hogwarts School of Witchcraft and Wizardry, a magical school with towering castles and buildings " \
             "intertwined, surrounded by a mysterious atmosphere. A new student stands beneath a castle, holding " \
             "a mysterious letter that contains a clue to the Holy Grail. The letters on the letter look like magical " \
             "runes, evoking a sense of adventure. The overcast sky surrounding the scene adds to the dark and mysterious " \
             "ambiance, reflecting the protagonist's curiosity and determination. The scene hides countless secrets that " \
             "await brave explorers to uncover."
    # print(prompt)

    answers = stability_api.generate(
        # prompt=prompt,
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=samples,
        sampler=sampler,
        style_preset=style_preset,
    )

    # 图片数组
    images = []

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = 'out/' + datetime_string
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                generate_result = upload_pic(img_path, dir_url)
                # 把生成图片存储到数据库
                add_image(image_url=generate_result, description=prompt, user_id=1)
                yield f"Image generated successfully! URL: {full_img_path}\n"

                # 图生图方法
                # enhanced_img_url = img2img(full_img_path, dir_url)
                # yield f"Enhanced Image generated successfully! URL: {enhanced_img_url}\n"

                # 放大图片方法
                upscale_img_url = upscale_pic(full_img_path, dir_url)

                # 上传图片到alioss并返回网络地址
                final_url = ''
                if upscale_img_url:
                    final_url = upload_pic('image_upscale.png', dir_url)
                    images.append(final_url)

                    # 把生成图片存储到数据库
                    add_image(image_url=final_url, description=prompt, user_id=1)

                # print(images)
                yield f"Upscale Image generated successfully! FI-URL: {images}\n"

    yield "done"


def generate_and_stream_protagonist(prompt, protagonist_id):
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    prompt = "There is a lively little elephant."
    protagonist_id = 1

    answers = stability_api.generate(
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=1,
        sampler=sampler,
        style_preset=style_preset,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = 'out/' + datetime_string
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                generate_result = upload_pic(img_path, dir_url)
                # 把生成图片存储到数据库
                add_protagonist_image(image_url=generate_result, protagonist_id=protagonist_id, user_id=1)
                # print(generate_result)
                yield f"Upscale Image generated successfully! FI-URL: {generate_result}\n"

    yield "done"


def generate_and_stream_plot_four_image(content):
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    prompt = content

    answers = stability_api.generate(
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=samples,
        sampler=sampler,
        style_preset=style_preset,
    )

    # 图片数组
    images = []

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = 'out/' + datetime_string
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                # 把图片存储到阿里云oss
                generate_result = upload_pic(img_path, dir_url)
                # 把生成图片存储到数据库
                add_image(image_url=generate_result, description=prompt, user_id=1)
                images.append(generate_result)

                # print(images)
                yield f"Upscale Image generated successfully! FI-URL: {images}\n"

    yield "done"


def generate_and_stream_plot_image(content):
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    prompt = content

    answers = stability_api.generate(
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=1,
        sampler=sampler,
        style_preset=style_preset,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = 'out/' + datetime_string
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                # 把图片存储到阿里云oss
                generate_result = upload_pic(img_path, dir_url)

                yield generate_result

    yield "done"


def generate_and_save_plot_image(description, user_id, protagonist_id=None ):
    yield "Image generation started...\n"
    # print("Image generation started...")  # 打印日志

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    prompt = description

    answers = stability_api.generate(
        prompt=prompt,
        seed=random.randint(100_000_000, 999_999_999),
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=1,
        sampler=sampler,
        style_preset=style_preset,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                now = datetime.now()
                datetime_string = now.strftime("%Y%m%d%H%M%S")
                dir_url = os.path.join('out', datetime_string)  # 使用 os.path.join 连接
                os.makedirs(dir_url)
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)

                # 把图片存储到阿里云oss
                generate_result = upload_pic(img_path, dir_url)
                # 把图片存储到protagonist_image表
                with app.app_context():
                    image_id = add_protagonist_image(
                        image_url=generate_result,
                        image_description=description,
                        protagonist_id = protagonist_id,
                        user_id=user_id
                    )


                # 合并 generate_result 和 image_details 到一个字典中并返回
                combined_result = {
                    "generated_image_url": generate_result,
                    "image_id": image_id
                }
                # print(f"Image generated, URL: {generate_result}")  # 打印日志
                yield combined_result

    # print("Done")  # 打印日志
    yield "done"

