import os
from flask import url_for
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
from dotenv import load_dotenv
import random
import warnings
from datetime import datetime

load_dotenv()
engine_id = os.environ['ENGINE_ID']
api_host = os.environ['API_HOST']
api_key = os.environ['STABILITY_KEY']

prompt = "masterpiece,high quality,best quality,"
start_schedule = 0.1
random_seed = random.randint(100_000_000, 999_999_999)
steps = 20
cfg_scale = 8.0
width = int(eval(os.environ['IMAGE_WIDTH']))
height = int(eval(os.environ['IMAGE_HEIGHT']))
samples = 1
sampler = generation.SAMPLER_K_DPMPP_2M
style_preset = 'anime'


def generate_and_stream(img_path, dir_url):
    print("Image generation started...")
    with open(img_path, 'rb') as f:
        img_data = f.read()
    init_image = Image.open(io.BytesIO(img_data))

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    answers = stability_api.generate(
        prompt="masterpiece,high quality,best quality,",
        init_image=init_image,
        start_schedule=start_schedule,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        sampler=generation.SAMPLER_K_DPMPP_2M,
        style_preset=style_preset,
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img_path = 'image_img2img.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)

                return full_img_path
