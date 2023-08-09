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


load_dotenv()
engine_id = os.environ['ENGINE_ID']
api_host = os.environ['API_HOST']
api_key = os.environ['STABILITY_KEY']

# sd参数
random_seed = random.randint(100_000_000, 999_999_999)
steps = 20
cfg_scale = 8.0
width = int(eval(os.environ['IMAGE_WIDTH']))
height = int(eval(os.environ['IMAGE_HEIGHT']))
samples = 1
sampler = generation.SAMPLER_K_DPMPP_2M
style_preset = 'anime'


def generate_and_stream(prompt):
    yield "Image generation started...\n"

    stability_api = client.StabilityInference(
        key=api_key,
        verbose=True,
        engine=engine_id,
    )

    prompt = request.json.get('prompt')
    # print(prompt)

    answers = stability_api.generate(
        prompt=prompt,
        seed=random_seed,
        steps=steps,
        cfg_scale=cfg_scale,
        width=width,
        height=height,
        samples=samples,
        sampler=sampler,
        # style_preset=style_preset,
    )

    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d%H%M%S")
    dir_url = 'out/'+datetime_string
    os.makedirs(dir_url)

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                if not os.path.exists('out'):
                    os.makedirs('out')
                img_path = 'image.png'
                full_img_path = os.path.join(dir_url, img_path)
                img.save(full_img_path)
                yield f"Image generated successfully! URL: {full_img_path}\n"

                # enhanced_img_url = img2img(full_img_path, dir_url)
                # yield f"Enhanced Image generated successfully! URL: {enhanced_img_url}\n"

                upscale_img_url = upscale_pic(full_img_path, dir_url)
                yield f"Upscale Image generated successfully! FI-URL: {upscale_img_url}\n"

    yield "done"
