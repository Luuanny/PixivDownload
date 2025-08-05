import os
import time
from res import *
from headers import ask_input


def main():
    urls = []
    lang = "zh"
    save_count = [0]
    illust_count = [0]
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        uid = input("请输入Pixiv用户ID (留空自动退出): ").strip().lower()
        if uid == "":
            print(f"已结束运行\n")
            return
        illust_ids = get_illust_ids(uid, lang)
        illust_sum = get_illust_sum(uid, lang)
        for illust_id in illust_ids:
            url, count = get_illust_url(illust_id, lang)
            urls.extend(url)
            illust_count[0] += count
            progress_bar(illust_count[0], illust_sum, prefix="正在加载插画链接")
        print(f"获取插画数量: {illust_count[0]}")
        if illust_count >= 50:
            print("图片数量较多，下载过程中可能会被拦截，如果下载失败，请稍后重新运行以继续下载")
        if ask_input("是否开始下载"):
            for illust_url in urls:
                finish_count,  suffix = save_illust(illust_url, uid)
                save_count[0] += int(finish_count)
                os.system('cls' if os.name == 'nt' else 'clear')
                progress_bar(save_count[0], illust_sum, prefix="正在下载", suffix=suffix)
            print("下载完成！")
        else:
            print("下载取消。")
    except Exception:
        print(f"请确保输入正确的用户ID\n")
        time.sleep(2)
        main()
    return


if __name__ == "__main__":
    main()  # 执行主函数
