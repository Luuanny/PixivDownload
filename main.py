import os
import time
from res import *
from headers import ask_input


def main() -> None:
    """ 下载程序主函数 """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        uid = input("请输入Pixiv用户ID (留空自动退出): ").strip().lower()
        if uid == "":
            print(f"已结束运行\n")
            return
        illust_ids = get_illust_ids(uid, "zh")
        if len(illust_ids) >= 50:
            print("图片数量较多，下载过程中可能会被拦截，如果下载失败，请稍后重新运行以继续下载")
        urls = load_illust(illust_ids, "zh")
        if ask_input("是否开始下载"):
            download_illust(urls, uid)
            print("下载完成！")
        else:
            print("下载取消。")
    except Exception:
        print(f"请确保输入正确的用户ID\n")
        time.sleep(2)
        main()
    return


def load_illust(illust_ids: list, lang: str = "zh") -> list:
    """ 加载插画数据
    :param illust_ids: 插画 ID 列表 (list)
    :param lang: 语言选项，默认为中文 (str)
    :return: 插画原图链接列表 (list)
    """
    urls: list = []
    illust_count: list[int] = [0]
    for illust_id, current in zip(illust_ids, range(1, len(illust_ids)+1)):
        url, count = get_illust_url(illust_id, lang)
        urls.extend(url)
        illust_count[0] += count
        progress_bar(current, len(illust_ids), prefix="正在加载插画链接")
    print(f"获取插画数量: {illust_count[0]}")
    return urls


def download_illust(urls: list, uid: str) -> None:
    """ 批量下载插画
    :param urls: 插画原图链接列表 (list)
    :param uid: 用户 ID (str)
    """
    save_count: int = 0
    for illust_url in urls:
        finish_count,  suffix = save_illust(illust_url, uid)
        save_count += int(finish_count)
        os.system('cls' if os.name == 'nt' else 'clear')
        progress_bar(save_count, len(urls), prefix="正在下载", suffix=suffix)
    return


if __name__ == "__main__":
    main()  # 执行主函数
