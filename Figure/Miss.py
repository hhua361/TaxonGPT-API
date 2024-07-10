import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_miss.csv"
data_new = pd.read_csv(file_path)

# 重命名列以便于理解
data_new.columns = ['Dataset', 'API1', 'API2', 'API3', 'API4', 'API5', 'Web1', 'Web2', 'Web3', 'Web4', 'Web5']

# 移除包含'Dataset/time'的行
data_new = data_new[data_new['Dataset'] != 'Dataset/time']

# 将所有值转换为数值型，并处理任何潜在的非数值问题
for col in data_new.columns[1:]:
    data_new[col] = pd.to_numeric(data_new[col], errors='coerce').fillna(0)

# 将数据转换为适合绘制堆叠条形图的长格式
data_long_new = data_new.melt(id_vars='Dataset', var_name='Method', value_name='Miss-rate')

# 设置seaborn样式
sns.set(style="white")

# 设置字体为Arial
plt.rcParams['font.family'] = 'Arial'

# 自定义颜色调色板
scatter_palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # 浅红色系
    '#9DC3E7', '#AED8F0', '#ADD8E6','#BFECF9', '#D0F0FF', '#E0F7FF'   # 浅蓝色系
]

# 绘制水平堆叠条形图
plt.figure(figsize=(14, 8))  # 调整图像大小
data_pivot_new = data_long_new.pivot(index='Dataset', columns='Method', values='Miss-rate')

# 增加条形宽度，通过减少条形间距
bar_width = 0.85  # 可以调整此值以使条形更厚或更薄
ax = data_pivot_new.plot(kind='barh', stacked=True, color=scatter_palette[:len(data_pivot_new.columns)], edgecolor='grey', width=bar_width)

# 仅在指定位置添加数据标签以避免重叠
for bars in ax.containers:
    for bar, label in zip(bars, bars.datavalues):
        method = bars.get_label()
        if label > 0:
            if method == 'API3' and label == 0.053:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')
            elif method == 'API4' and label == 0.041:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')
            elif label not in [0.053, 0.041]:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')

# 设置标签和标题
plt.xlabel('Missed Species Percentage', fontsize=12)
plt.ylabel('Dataset', fontsize=12)
plt.title('Missed Species Percentage in Taxonomic Keys across Different Methods', fontsize=14)

# 调整图例位置
plt.legend(title='Method', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# 使轴线更突出
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.xaxis.label.set_size(12)
ax.yaxis.label.set_size(12)
ax.tick_params(axis='x', which='major', labelsize=10, length=6, width=2, direction='out', color='black')
ax.tick_params(axis='y', which='major', labelsize=10, length=6, width=2, direction='out', color='black')

# 仅在底部和左侧添加刻度线
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.tick_params(axis='x', direction='out', length=5, width=1, colors='black')
ax.tick_params(axis='y', direction='out', length=5, width=1, colors='black')

# 将x轴设置为百分比
ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))

plt.tight_layout()

# 保存为SVG格式
output_path = 'E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_miss.svg'
plt.savefig(output_path, format='svg')

# 显示图像
plt.show()
