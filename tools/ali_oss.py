import oss2
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()


def upload_pic(img_name, dir_name):
    # 首先, 初始化 AccessKeyId, AccessKeySecret, BucketName 和 Endpoint.
    auth = oss2.Auth(os.environ['OSS_KEY'], os.environ['OSS_SECRET'])
    bucket = oss2.Bucket(auth, os.environ['OSS_ENDPOINT'], os.environ['OSS_BUCKETNAME'])

    # 创建模拟的OSS文件夹结构
    oss_object_key = os.path.join(dir_name, img_name).replace('\\', '/')

    # 本地文件路径
    local_file_path = os.path.join(dir_name, img_name)

    # 使用 put_object_from_file 方法来上传一个本地文件。
    result = bucket.put_object_from_file(oss_object_key, local_file_path)

    # 生成已上传图片的完整URL
    image_url = f"https://{os.environ['OSS_BUCKETNAME']}.{os.environ['OSS_ENDPOINT']}/{oss_object_key}"

    return image_url


