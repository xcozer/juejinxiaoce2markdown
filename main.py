import logging
import os
import re
import traceback
from urllib.request import urlretrieve

import pdfkit
import requests
import yaml

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)7s: %(message)s')
logger = logging.getLogger(__name__)


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clear_slash(s: str) -> str:
    return s.replace('\\', '').replace('/', '').replace('|', '')


class Juejinxiaoce2Markdown:
    img_pattern = re.compile(r'!\[.*?\]\((.*?)\)', re.S)

    def __init__(self, config: dict):
        logger.info(config)
        pwd = os.path.dirname(os.path.abspath(__file__))
        default_save_dir = os.path.join(pwd, 'book')
        sessionid: str = config['sessionid']
        self.book_ids: list = config['book_ids']
        self.save_dir: str = config.get('save_dir', default_save_dir)
        self.request_headers = {
            'cookie': f'sessionid={sessionid};',
        }
        makedirs(self.save_dir)

    def get_section_res(self, section_id):
        url = f'https://api.juejin.cn/booklet_api/v1/section/get'
        data = {
            'section_id': str(section_id)
        }
        res = requests.post(url, headers=self.request_headers, json=data)
        # logger.info(res.text)
        return res

    def get_book_info_res(self, book_id) -> requests.Response:
        url = f'https://api.juejin.cn/booklet_api/v1/booklet/get'
        data = {
            'booklet_id': str(book_id)
        }
        res = requests.post(url, headers=self.request_headers, json=data)
        # logger.info(res.text)
        return res

    @classmethod
    def save_markdown(cls, markdown_file_path, section_img_dir, markdown_relative_img_dir, markdown_str):
        img_urls = re.findall(cls.img_pattern, markdown_str)
        for img_index, img_url in enumerate(img_urls):
            new_img_url: str = img_url.replace('\n', '')
            if new_img_url.startswith('//'):
                new_img_url = f'https:{new_img_url}'
            try:
                suffix = os.path.splitext(new_img_url)[-1]
                img_file_name = f'{img_index + 1}{suffix}'.replace('?', '')
                md_relative_img_path = os.path.join(markdown_relative_img_dir, img_file_name)
                img_save_path = os.path.join(section_img_dir, img_file_name)
                urlretrieve(new_img_url, img_save_path)
                markdown_str = markdown_str.replace(img_url, md_relative_img_path)
            except Exception as e:
                logger.error({
                    'msg': '处理图片失败',
                    'img_url': new_img_url,
                    'e': repr(e),
                    'traceback': traceback.format_exc(),
                    'markdown_relative_img_dir': markdown_relative_img_dir
                })
        with open(markdown_file_path, 'w', encoding='utf8') as f:
            f.write(markdown_str)

    def deal_a_book(self, book_id):
        log_data = {
            'book_id': book_id,
            'msg': '开始处理小册'
        }
        logger.info(log_data)

        res = self.get_book_info_res(book_id)
        res_json = res.json()
        book_title = res_json['data']['booklet']['base_info']['title']
        section_list = res_json['data']['sections']
        book_title = clear_slash(book_title)
        logger.info({'book_title': book_title})

        section_id_list = [e['section_id'] for e in section_list]
        section_count = len(section_id_list)
        with open(f"book/{book_title}.html", 'a', encoding="utf-8") as html:
            html.writelines("""
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta data-n-head="ssr" name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, viewport-fit=cover">
    <style>.markdown-body{word-break:break-word;line-height:1.75;font-weight:400;font-size:16px;overflow-x:hidden;color:#333}.markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5,.markdown-body h6{line-height:1.5;margin-top:35px;margin-bottom:10px;padding-bottom:5px}.markdown-body h1{font-size:24px;margin-bottom:5px}.markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5,.markdown-body h6{font-size:20px}.markdown-body h2{padding-bottom:12px;border-bottom:1px solid #ececec}.markdown-body h3{font-size:18px;padding-bottom:0}.markdown-body h6{margin-top:5px}.markdown-body p{line-height:inherit;margin-top:22px;margin-bottom:22px}.markdown-body img{max-width:100%}.markdown-body hr{border:none;border-top:1px solid #ddd;margin-top:32px;margin-bottom:32px}.markdown-body code{word-break:break-word;border-radius:2px;overflow-x:auto;background-color:#fff5f5;color:#ff502c;font-size:.87em;padding:.065em .4em}.markdown-body code,.markdown-body pre{font-family:Menlo,Monaco,Consolas,Courier New,monospace}.markdown-body pre{overflow:auto;position:relative;line-height:1.75}.markdown-body pre>code{font-size:12px;padding:15px 12px;margin:0;word-break:normal;display:block;overflow-x:auto;color:#333;background:#f8f8f8}.markdown-body a{text-decoration:none;color:#0269c8;border-bottom:1px solid #d1e9ff}.markdown-body a:active,.markdown-body a:hover{color:#275b8c}.markdown-body table{display:inline-block!important;font-size:12px;width:auto;max-width:100%;overflow:auto;border:1px solid #f6f6f6}.markdown-body thead{background:#f6f6f6;color:#000;text-align:left}.markdown-body tr:nth-child(2n){background-color:#fcfcfc}.markdown-body td,.markdown-body th{padding:12px 7px;line-height:24px}.markdown-body td{min-width:120px}.markdown-body blockquote{color:#666;padding:1px 23px;margin:22px 0;border-left:4px solid #cbcbcb;background-color:#f8f8f8}.markdown-body blockquote:after{display:block;content:""}.markdown-body blockquote>p{margin:10px 0}.markdown-body ol,.markdown-body ul{padding-left:28px}.markdown-body ol li,.markdown-body ul li{margin-bottom:0;list-style:inherit}.markdown-body ol li .task-list-item,.markdown-body ul li .task-list-item{list-style:none}.markdown-body ol li .task-list-item ol,.markdown-body ol li .task-list-item ul,.markdown-body ul li .task-list-item ol,.markdown-body ul li .task-list-item ul{margin-top:0}.markdown-body ol ol,.markdown-body ol ul,.markdown-body ul ol,.markdown-body ul ul{margin-top:3px}.markdown-body ol li{padding-left:6px}.markdown-body .contains-task-list{padding-left:0}.markdown-body .task-list-item{list-style:none}@media (max-width:720px){.markdown-body h1{font-size:24px}.markdown-body h2{font-size:20px}.markdown-body h3{font-size:18px}}</style>
</head>
<body class="markdown-body">
            """)
            for index, section_id in enumerate(section_id_list):
                section_order = index + 1
                logger.info({
                    '进度': f'{section_order}/{section_count}',
                    'msg': '处理 section',
                    'section_id': section_id
                })
                res = self.get_section_res(section_id)
                res_json = res.json()
                section_json = res_json['data']['section']
                markdown_html_str = section_json['content']
                html.writelines(markdown_html_str)
            html.writelines("</body></html>")
        pdfkit.from_file(f'book/{book_title}.html', f'book/{book_title}.pdf')
        os.remove(f'book/{book_title}.html')

        log_data['msg'] = '处理完成'
        logger.info(log_data)

    def main(self):
        for book_id in self.book_ids:
            try:
                self.deal_a_book(book_id)
            except Exception as e:
                log_data = {
                    'book_id': book_id,
                    'e': repr(e),
                    'traceback': traceback.format_exc(),
                    'msg': '处理小册出错'
                }
                logger.error(log_data)


if __name__ == '__main__':
    with open('config.yml', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    helper = Juejinxiaoce2Markdown(config)
    helper.main()
