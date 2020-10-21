import matplotlib.pyplot as plt

# 绘制一系列点
# x_values = [1, 2, 3, 4, 5]
# y_values = [1, 4, 9, 16, 25]

# 自动计算数据
x_values = list(range(1, 1001))
y_values = [x ** 2 for x in x_values]

# 使用颜色映射(colormap)
# 将c设置为一个y值列表,并使用参数cmap告诉pyplot使用哪个颜色樱色
plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, edgecolors='none', s=40)

# 传递实参edgecolor='none':删除数据点的轮廓
# 向scatter()传递参数c,并将其设置为要使用的颜色的名称c=red
# 也可以使用RGB颜色模式自定义颜色,将参数c设置为一个元祖c=(0, 0 ,0.8)
# plt.scatter(x_values, y_values, c=(0, 0, 0.8), edgecolor='none', s=40)

# 设置图表标题并给坐标轴加上标签
plt.title('Square Numbers', fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Square of value', fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=14)

# 设置每个坐标轴的屈指范围
plt.axis([0, 1100, 0, 1100000])

# plt.show()
# 自动保存图表
# 第一个实参指定要以什么样的文件名保存图表,这个文件将存储到scatter_squares.py所在的目录中
# 第二个实参指定将图表多余的空白区域拆剪掉.如果要保留图表周围多余的空白区域,可省略这个实参.
plt.savefig('squares_pot.png', bbox_inches='tight')