import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_redundancies.csv"
data = pd.read_csv(file_path)

# 重命名列以便于理解
data.columns = ['Dataset', 'API1', 'API2', 'API3', 'API4', 'API5']

# 移除包含'Dataset/time'的行
data = data[data['Dataset'] != 'Dataset/time']

# 将数据转换为适合绘制堆叠条形图的长格式
data_long = data.melt(id_vars='Dataset', var_name='API', value_name='Redundancies')

# 将'Redundancies'列转换为数值型，强制将错误转换为NaN然后填充为0
data_long['Redundancies'] = pd.to_numeric(data_long['Redundancies'], errors='coerce').fillna(0)

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
plt.figure(figsize=(14, 6))
data_pivot = data_long.pivot(index='Dataset', columns='API', values='Redundancies')

# 增加条形宽度，通过减少条形间距
bar_width = 0.75  # 可以调整此值以使条形更厚或更薄
ax = data_pivot.plot(kind='barh', stacked=True, color=scatter_palette[:len(data_pivot.columns)], edgecolor='grey', width=bar_width)

# 添加数据标签
for bars in ax.containers:
    ax.bar_label(bars, labels=[f'{int(label)}' if label > 0 else '' for label in bars.datavalues],
                 label_type='center', fontsize=12, color='grey', fontweight='bold')

# 设置标签和标题
plt.xlabel('Redundancies number', fontsize=12)
plt.ylabel('Dataset', fontsize=12)
plt.title('Redundancies in Taxonomic Keys across Different API Runs', fontsize=14)

# 调整图例位置
plt.legend(title='API', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

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

plt.tight_layout()

# 保存为SVG格式
output_path = 'E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_redundancies.svg'
plt.savefig(output_path, format='svg')

# 显示图像
plt.show()
