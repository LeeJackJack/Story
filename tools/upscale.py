import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from dotenv import load_dotenv
import random
from datetime import datetime
from flask import url_for

# sd参数
random_seed = random.randint(100_000_000, 999_999_999)
steps = 10
cfg_scale = 8.0
width = int(eval(os.environ['IMAGE_WIDTH'])) * 2
samples = 1
sampler = generation.SAMPLER_K_DPMPP_2M
prompt = "masterpiece,high quality,best quality,"

load_dotenv()
engine_id = os.environ['UPSCALE_ENGINE_ID']
api_key = os.environ['STABILITY_KEY']


def upscale_pic(img_url, dir_url):

    stability_api = client.StabilityInference(
        key=api_key,
        upscale_engine=engine_id,
        verbose=True,
    )

    img = Image.open(img_url)

    answers = stability_api.upscale(
        init_image=img,
        width=width,
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please submit a different image and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                big_img = Image.open(io.BytesIO(artifact.binary))
                img_path = 'image_upscale.png'
                full_img_path = os.path.join(dir_url, img_path)
                big_img.save(full_img_path)
                print(dir_url)
                print(img_path)
                print(full_img_path)

                upscale_img_url = url_for('static', filename=dir_url.split('/')[1]+'/'+img_path)

                return upscale_img_url
