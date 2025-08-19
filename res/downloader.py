import json
import os

import requests

from res.ask_info import ask_input
from res.config import read_headers, read_save_path
from res.get_info import get_illust_ids, get_user_name, get_illust_url
from res.progress_bar import progress_bar


def downloader() -> None:
    """ 下载程序主函数 """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        uid = input("请输入Pixiv用户ID (留空自动退出): ").strip().lower()
        if uid == "":
            print(f"已结束运行")
            return None
        illust_ids = get_illust_ids(uid, "zh")
        if len(illust_ids) >= 50:
            print("图片数量较多，下载过程中可能会被拦截，如果下载失败，请稍后重新运行以继续下载")
        urls = load_illust(illust_ids, "zh")
        if ask_input("是否开始下载"):
            download_log = save_illusts(urls, uid)
            print("下载完成！")
            print(json.dumps(download_log, ensure_ascii=False, indent=2))
        else:
            print("下载取消。")
    except Exception as e:
        print(e)
        print(f"请确保输入正确的用户ID\n")
    return None


def load_illust(illust_ids: list, lang: str = "zh") -> list:
    """ 加载插画数据
    :param illust_ids: 插画 ID 列表 (list)
    :param lang: 语言选项，默认为中文 (str)
    :return: 插画原图链接列表 (list)
    """
    urls: list = []
    illust_count: list[int] = [0]
    for illust_id, current in zip(illust_ids, range(1, len(illust_ids) + 1)):
        url, count = get_illust_url(illust_id, lang)
        urls.extend(url)
        illust_count[0] += count
        progress_bar(current, len(illust_ids), prefix="正在加载插画链接")
    print(f"获取插画数量: {illust_count[0]}")
    return urls


def save_illusts(urls: list, uid: str) -> list:
    """ 批量下载插画
    :param urls: 插画原图链接列表 (list)
    :param uid: 用户 ID (str)
    """
    save_count: int = 0
    download_log: list = []
    for illust_url in urls:
        finish_count, log = save_illust(illust_url, uid)
        save_count += int(finish_count)
        download_log.append(log)
        os.system('cls' if os.name == 'nt' else 'clear')
        progress_bar(save_count, len(urls), prefix="正在下载")
    return download_log


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
        download_count = 1
        download_info = f"{save_path} 文件已存在，跳过下载"
        return download_count, download_info
    for attempt in range(max_retry + 1):
        try:
            illust = requests.get(url, headers=read_headers(), timeout=15)
            illust.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(illust.content)
            download_count = 1
            download_info = f"{save_path} 下载成功！"
        except Exception as e:
            if attempt < max_retry:
                continue
            download_info = f"{illust_name} 下载失败 \n{e}"
    return download_count, download_info


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
