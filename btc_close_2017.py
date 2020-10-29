# 制作收盘价走势图：JSON 格式
# 在本节中，你将下载JSON格式的收盘价数据，并使用`json`模块来处理它们。
# Pygal提供了一个适合初学者使用的绘图工具，可以用它对收盘价数据进行可视化，以探索价格的特征。
# 下载数据
from __future__ import (absolute_import, division, print_function, unicode_literals)

try:
    # python2.x 版本
    from urllib2 import urlopen
except ImportError:
    # python 3.x 版本
    from urllib.request import urlopen
import json
import requests
import pygal
import math
from itertools import groupby

# json_url = "https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json"
# response = urlopen(json_url)  # 将json_url网址传入urlopen()函数,返回btc_close_2017.json文件
# # 读取数据
# req = response.read()
# # 将数据写入文件,'wb'表示以二进制格式打开一个文件,只用于写入操作
# with open('btc_close_2017_urllib.json', 'wb') as f:
#     f.write(req)
# # 加载json格式
# file_urllib = json.loads(req)
# print(file_urllib)
#
# # 使用第三方模块requests封装了许多常用的方法,让下载数据和读取方式变得非常简单
#
# json_url = 'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# req = requests.get(json_url)
# # 将数据写入文件
# with open('btc_close_2017_request.json', 'w') as f:
#     f.write(req.text)  # req.text属性可以直接读取文件数据,返回格式字符串
#
# file_requests = req.json()
# print(file_requests)
# print(file_urllib == file_requests)

# 提取相关数据
# 将数据加载到一个列表中
filename = 'btc_close_2017.json'
with open(filename) as f:
    btc_data = json.load(f)

#  打印每一天的信息
for btc_dict in btc_data:
    date = btc_dict['date']
    month = int(btc_dict['month'])
    week = int(btc_dict['week'])
    weekday = btc_dict['weekday']
    close = int(float(btc_dict['close']))
    print("{} is month {} week {}, {}, the close price is {} RMB".format(date, month, week, weekday, close))

# 创建5个列表，分别存储日期和收盘价
dates = []
months = []
weeks = []
weekdays = []
close = []
# 每一天的信息
for btc_dict in btc_data:
    # 绘制收盘价折线图
    dates.append(btc_dict['date'])
    months.append(int(btc_dict['month']))
    weeks.append(int(btc_dict['week']))
    weekdays.append(btc_dict['weekday'])
    close.append(int(float(btc_dict['close'])))

line_chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False)  # ①
line_chart.title = '收盘价（¥）'
line_chart.x_labels = dates
N = 20  # x轴坐标每隔20天显示一次
line_chart.x_labels_major = dates[::N]  # ②
line_chart.add('收盘价', close)
line_chart.render_to_file('收盘价折线图（¥）.svg')

line_chart = pygal.Line(x_label_rotation=20, show_minor_x_labels=False)
line_chart.title = '收盘价对数变换 (¥) '
line_chart.x_labels = dates
N = 20  # x轴坐标每隔20天显示一次
line_chart.x_labels_major = dates[::N]
close_log = [math.log10(_) for _ in close]
line_chart.add('log收盘价', close_log)
line_chart.render_to_file('收盘价对数变换折线图 (¥) .svg')
line_chart


def draw_line(x_data, y_data, title, y_legend):
    xy_map = []
    for x, y in groupby(sorted(zip(x_data, y_data)), key=lambda _: _[0]):
        y_list = [v for _, v in y]
        xy_map.append([x, sum(y_list) / len(y_list)])
    x_unique, y_mean = [*zip(*xy_map)]
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_unique
    line_chart.add(y_legend, y_mean)
    line_chart.render_to_file(title + '.svg')
    return line_chart


# 绘制2017年1月到11月的日均值
idx_month = dates.index('2017-12-01')
line_chart_month = draw_line(
    months[:idx_month], close[:idx_month], '收盘价月日均值（¥）', '月日均值')
line_chart_month

# 绘制前49周(2017-01-02~2017-12-10)的日均值
idx_week = dates.index('2017-12-11')
line_chart_month = draw_line(
    weeks[1:idx_week], close[1:idx_week], '收盘价周日均值（¥）', '周日均值')
line_chart_month

# 绘制每周中各天的均值
idx_week = dates.index('2017-12-11')
wd = ['Monday', 'Tuesday', 'Wednesday',
      'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdays_int = [wd.index(w) + 1 for w in weekdays[1:idx_week]]
line_chart_weekday = draw_line(
    weekdays_int, close[1:idx_week], '收盘价星期均值（¥）', '星期均值')
line_chart_weekday.x_labels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
line_chart_weekday.render_to_file('收盘价星期均值（¥）.svg')
line_chart_weekday

# 收盘价数据仪表盘
with open('收盘价Dashboard.html', 'w', encoding='utf8') as html_file:
    html_file.write(
        '<html><head><title>收盘价Dashboard</title><meta charset="utf-8"></head><body>\n')
    for svg in [
        '收盘价折线图（¥）.svg', '收盘价对数变换折线图（¥）.svg', '收盘价月日均值（¥）.svg',
        '收盘价周日均值（¥）.svg', '收盘价星期均值（¥）.svg'
    ]:
        html_file.write(
            '    <object type="image/svg+xml" data="{0}" height=500></object>\n'.format(svg))
    html_file.write('</body></html>')
