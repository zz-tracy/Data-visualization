import csv
from datetime import datetime

from matplotlib import pyplot as plt

# 从文件中获取日期、最高气温和最低气温
# filename = 'sitka_weather_07-2014.csv'
# filename = 'sitka_weather_2014.csv'
filename = 'death_valley_2014.csv'
with open(filename) as f:
    # 调用vsv.render(),创建一个与该文件相关联的阅读器(render)对象
    reader = csv.reader(f)
    # 模块csv的render类包含next()方法,调用内置函数next()并将一个render作为参数传递给它时,将调用render的next()方法,从而返回文件中的下一行
    header_row = next(reader)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            current_date = datetime.strptime(row[0], "%Y-%m-%d")
            high = int(row[1])
            low = int(row[3])
        except:
            print(current_date, 'missing data')
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

    # print(highs)

    # 对列表调用了enumerate()来获取每个元素的索引及其值.
    # enumerate()内置函数,返回一个可枚举的对象,该对象的next()方法将返回一个tuple元祖
    # for index, column_header in enumerate(header_row):
    # print(index, column_header)

# 根据数据绘制图形
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red', alpha=0.5)  # alpha颜色透明度
plt.plot(dates, lows, c='blue', alpha=0.5)
# 使用fill_between()方法给图表区域着色,接受一个x值系列和两个y值系列,并填充两个y值系列之间的空间.
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

# 设置图形的格式
# plt.title('Daily high temperatures, July 22014', fontsize=24)
# plt.title('Daily high and low temperatures - 2014', fontsize=24)
title = 'Daily high and low temperatures - 2014\nDeath Valley, CA'
plt.title(title, fontsize=20)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()  # 绘制斜的日期标签,以免彼此重叠
plt.ylabel('Temperature(F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)

plt.show()
