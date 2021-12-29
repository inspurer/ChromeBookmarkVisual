# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# create_time:      2021/12/28 22:18
# 运行环境           Python3.6+
# github            https://github.com/inspurer
# 微信公众号         月小水长

from lxml import etree

import json

bookmark_html_file = 'bookmarks.html'
bookmark_json_file = 'bookmarks.json'


def get_regular_html():
    with open(bookmark_html_file, mode='r', encoding='utf-8-sig') as fp:
        html_content = fp.read()
    '''
     先规则 html 标签
    '''
    html_content = html_content.replace(r'<p>', '')
    html_content = html_content.replace(r'</H3>', r'</H3></DT>')
    html_content = html_content.replace(r'</A>', r'</A></DT>')
    return html_content


html = etree.HTML(get_regular_html())

root_name = '书签'
name_key, children_key = 'name', 'children'
url_key = 'url'
bookmark_map_json = {
    name_key: root_name,
}
root = html.xpath('//dl[1]/dl[1]')[0]

exclude_collection = ['编程', '算法', '网课', '杂', '快酷', '开发者信息中心']
# exclude_collection = ['杂', '算法', '网课', '博客']


def parse_html_recursive(root_html):
    children = []
    children_html = root_html.xpath('./child::*')
    for index, ele in enumerate(children_html):
        tag_name = ele.tag.strip()
        if tag_name == 'dt':
            if ele.xpath('./h3'):
                name = ele.xpath('./h3/text()')[0].strip()
                if name in exclude_collection:
                    continue
                children.append({
                    name_key: name,
                    children_key: parse_html_recursive(children_html[index + 1])
                })
            elif ele.xpath('./a'):
                if len(ele.xpath('./a/text()')) == 0:
                    print('过滤掉没有书签名的')
                    continue
                url = ele.xpath('./a/@href')[0]
                name = ele.xpath('./a/text()')[0].strip()
                children.append({
                    name_key: name,
                    url_key: url
                })
    return children


bookmark_map_json[children_key] = parse_html_recursive(root)

with open(bookmark_json_file, 'w', encoding='utf-8-sig') as f:
    f.write(json.dumps(bookmark_map_json, indent=2, ensure_ascii=False))

print(bookmark_map_json)

links = html.xpath('//dt/a')
print(len(links))
