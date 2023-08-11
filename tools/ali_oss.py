import oss2
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()


def upload_pic(img_path, full_img_path):

    # 首先, 初始化 AccessKeyId, AccessKeySecret,BucketName 和 Endpoint.
    auth = oss2.Auth(os.environ['OSS_KEY'], os.environ['OSS_SECRET'])
    bucket = oss2.Bucket(auth, os.environ['OSS_ENDPOINT'], os.environ['OSS_BUCKETNAME'])

    local_file_path = os.path.join('out/20230810155026', 'image.png')

    # 使用 put_object_from_file 方法来上传一个本地文件。该方法会返回 PutObjectResult 对象。
    # 如果 PutObjectResult.status == 200，那么表示文件上传成功。
    # result = bucket.put_object_from_file(img_path, full_img_path)
    result = bucket.put_object_from_file('image.png', local_file_path)

    image_url = f"https://{os.environ['OSS_BUCKETNAME']}.{os.environ['OSS_ENDPOINT']}/image.png"

    print(image_url)
    return f"HTTP response status: {result.status}/n URL:{image_url}"

