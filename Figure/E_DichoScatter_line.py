import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import numpy as np

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/E_Dicho/E_Dicho_simplify.csv"
data = pd.read_csv(file_path)

# 清洗和整理数据，将每个数据集的实验结果分别处理
api_data = data.melt(id_vars=['Dataset/time'], value_vars=['E_DichoAPI (average)'],
                     var_name='Trial', value_name='Runtime')
api_data['Method'] = 'API'

web_data = data.melt(id_vars=['Dataset/time'], value_vars=['E_DichoWEB (average)'],
                     var_name='Trial', value_name='Runtime')
web_data['Method'] = 'Web'

delta_data = data.melt(id_vars=['Dataset/time'], value_vars=['E_DichoDELTA'],
                       var_name='Trial', value_name='Runtime')
delta_data['Method'] = 'DELTA'

# 合并API、Web和DELTA数据
combined_data = pd.concat([api_data, web_data, delta_data])

# 更改列名
combined_data.rename(columns={'Dataset/time': 'Dataset'}, inplace=True)

# 替换"Na"字符串为NaN
combined_data['Runtime'] = combined_data['Runtime'].replace("Na", pd.NA)

# 将Runtime列转换为数值型，并处理非数值值
combined_data['Runtime'] = pd.to_numeric(combined_data['Runtime'], errors='coerce')

# 去除NA值
combined_data.dropna(subset=['Runtime'], inplace=True)

# 创建一个列表示方法的顺序
method_order = {'API': 0, 'Web': 1, 'DELTA': 2}
combined_data['MethodOrder'] = combined_data['Method'].map(method_order)

# 设置字体
plt.rcParams["font.family"] = "Times New Roman"

# 设置样式
sns.set(style="whitegrid")

# 定义颜色
palette = {
    'API': '#EF7A6D',
    'Web': '#9DC3E7',
    'DELTA': '#7FB77E'
}

# 定义散点和连接线颜色
scatter_palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # 浅红色系
    '#9DC3E7', '#AED8F0', '#ADD8E6','#BFECF9', '#D0F0FF', '#E0F7FF',  # 浅蓝色系
]

# 绘制小提琴图
plt.figure(figsize=(14, 8))
ax = sns.violinplot(data=combined_data, x='Method', y='Runtime', hue='Method',
                    palette=palette, inner=None, linewidth=2, legend=False)

# 移除填充
for collection in ax.collections:
    collection.set_facecolor('none')

# 为同一数据集在不同方法间添加连接线和散点
for i, dataset in enumerate(combined_data['Dataset'].unique()):
    subset = combined_data[combined_data['Dataset'] == dataset]
    x = subset['MethodOrder'].values + np.random.uniform(-0.1, 0.1, size=len(subset))
    y = subset['Runtime'].values
    plt.plot(x, y, marker='o', markersize=15, linestyle='-', linewidth=3, alpha=0.7, color=scatter_palette[i], markeredgecolor='black')

# 创建自定义图例
custom_lines = [Line2D([0], [0], color=scatter_palette[i], lw=4) for i in range(len(combined_data['Dataset'].unique()))]
legend = plt.legend(custom_lines, combined_data['Dataset'].unique(), title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, title_fontsize=16)
plt.setp(legend.get_title(), family='Times New Roman')
for text in legend.get_texts():
    text.set_family('Times New Roman')

# 设置图像标题和标签
plt.title('Comparison of E_Dicho between API, Web, and DELTA Methods', fontsize=22, family='Times New Roman', pad=20)
plt.xlabel('Methods', fontsize=20, family='Times New Roman')
plt.ylabel('E_Dicho Score', fontsize=20, family='Times New Roman', labelpad=20)

# 设置坐标轴刻度
plt.xticks(ticks=[0, 1, 2], labels=['API', 'Web', 'DELTA'], fontsize=18, family='Times New Roman')
plt.yticks(fontsize=18, family='Times New Roman')

# 设置坐标轴颜色为黑色
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.spines['right'].set_color('black')
ax.xaxis.label.set_color('black')
ax.yaxis.label.set_color('black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# 移除背景网格线，但保留坐标轴
ax.grid(False)

# 显示图像
plt.tight_layout()
plt.show()

