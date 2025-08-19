import os

import requests

from res.config import read_headers, read_save_path
from res.get_info import get_user_name


def save_dir(uid: str) -> str:
    """ 根据用户 ID 获取用户名，创建以用户名为名的文件夹，返回目录名。
    :param uid: 用户ID (str)
    :return: 保存目录名 (str)
    """
    user_name: str = get_user_name(uid).strip()
    for ch in '\\/.:*?"<>|':
        user_dir = user_name.replace(ch, '-')
        if user_dir != user_name:
            break
    father_dir = read_save_path()
    save_directory: str = f"{father_dir}\\{user_dir}"
    os.makedirs(save_directory, exist_ok=True)  # 创建目录，如果已存在则不报错
    return save_directory


def save_illust(url: str, uid: str, max_retry: int = 1) -> tuple[int, str]:
    """ 保存图片并保存到指定目录，失败时自动重试。
    :param url: 图片链接 (str)
    :param uid: 用户 ID (str)
    :param max_retry: 最大重试次数，默认为 1 (int)
    :return: 下载完成数量 (int), 下载信息 (str)
    """
    download_count: int = 0
    download_info: str = ""
    illust_name = url.split("/")[-1]
    save_path = os.path.join(save_dir(uid), illust_name)
    if os.path.exists(save_path):
        download_count += 1
        download_info = f"\n{save_path} 文件已存在，跳过下载"
    for attempt in range(max_retry + 1):
        try:
            illust = requests.get(url, headers=read_headers(), timeout=15)
            illust.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(illust.content)
            download_count += 1
            download_info = f"\n{save_path} 下载成功！"
        except Exception as e:
            if attempt < max_retry:
                continue
            download_info = f"\n{illust_name} 下载失败 \n{e}"
    return download_count, download_info
