import json

from logging import getLogger, StreamHandler, DEBUG, Formatter

import model

# setting load
config_file = open("./settings/setting.json", "r")
conf = json.load(config_file)
config_file.close()

# log
logger = getLogger(__name__)
logger.setLevel(DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
handler_format = Formatter(conf["logger"]["format"])
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# conf
top_url = conf["urasunday"]["url"]["top"]

def main():
    try:
        logger.debug("start")
        target_list = {}

        ud = model.Urasunday()
        ud.page_move(top_url, 3)
        up_list = ud.get_upload_list()
        
        for l in up_list:
            is_update, title = ud.is_update_target(l)
            if is_update:
                href = ud.get_href_of_element(l)
                target_list[title] = href

        for k, v in target_list.items():
            logger.info("[{}]のダウンロードを開始します。".format(k))
            ud.page_move(v, 3)
            number_of_stories = ud.get_number_of_stories()
            logger.info("[{}] {}".format(k, number_of_stories))
            save_dir = ud.create_manga_directory(k, number_of_stories)

            ud.page_prev()
            img_src_list = ud.get_img_src()
            min_number, zero = ud.get_min_filenumber(save_dir)
            for src in img_src_list:
                file_name = str(min_number).zfill(zero) + ".png"
                ud.save_image(src, save_path=save_dir + "\\" + file_name)
                min_number += 1
        
        if len(target_list) == 0:
            logger.info("更新対象はありませんでした")

    except Exception as e:
        logger.error(e)
    else:
        logger.info("正常終了！")
    finally:
        ud._quit()


if __name__ == "__main__":
    main()

"""
残課題
・画像ファイルの形式を変更する必要がありそう（pngじゃなさそうwebp？？）
　⇒ついでに保存済みのやつも変換できるように

・別件だけど、Chrome保存してたページから画像だけ引っ張ってきたい
　しないと一生読めないｗ

"""