import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/E_Dicho/E_Dicho_scatter.csv"
data = pd.read_csv(file_path)

# 清洗和整理数据，将每个数据集的实验结果分别处理
api_data = data.melt(id_vars=['Dataset/time'], value_vars=['E_DichoAPI1', 'E_DichoAPI2', 'E_DichoAPI3', 'E_DichoAPI4', 'E_DichoAPI5'],
                     var_name='Trial', value_name='Runtime')
api_data['Method'] = 'API'

web_data = data.melt(id_vars=['Dataset/time'], value_vars=['E_DichoWEB1', 'E_DichoWEB2', 'E_DichoWEB3', 'E_DichoWEB4', 'E_DichoWEB5'],
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

# 检查数据列名
print(combined_data.columns)

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

scatter_palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # 浅红色系
    '#9DC3E7', '#AED8F0', '#ADD8E6','#BFECF9', '#D0F0FF', '#E0F7FF',  # 浅蓝色系
]

# 绘制小提琴图和散点图
plt.figure(figsize=(14, 8))

# 绘制小提琴图
ax = sns.violinplot(data=combined_data, x='Method', y='Runtime', hue='Method',
                    palette=palette, inner=None, linewidth=2, legend=False)

# 移除填充
for collection in ax.collections:
    collection.set_facecolor('none')

# 绘制散点图
sns.stripplot(data=combined_data, x='Method', y='Runtime', hue='Dataset',
              dodge=True, jitter=0.2, marker='o', alpha=1, linewidth=1, palette=scatter_palette, s=15)

# 调整图例
legend = plt.legend(title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, title_fontsize=16)
plt.setp(legend.get_title(), family='Times New Roman')  # 设置图例标题字体
for text in legend.get_texts():
    text.set_family('Times New Roman')  # 设置图例标签字体

# 设置图像标题和标签
plt.title('Comparison of E_Dicho between API, Web, and DELTA Methods', fontsize=22, family='Times New Roman', pad=20)
plt.xlabel('Methods', fontsize=20, family='Times New Roman')
plt.ylabel('E_Dicho Score', fontsize=20, family='Times New Roman', labelpad=20)  # 调整labelpad增加距离

# 设置坐标轴刻度
plt.xticks(fontsize=18, family='Times New Roman')
plt.yticks(fontsize=18, family='Times New Roman')

# 设置坐标轴颜色为黑色
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.label.set_color('black')
ax.yaxis.label.set_color('black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')

# 添加刻度线
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.tick_params(axis='x', direction='out', length=5, width=2, colors='black')
ax.tick_params(axis='y', direction='out', length=5, width=2, colors='black')

# 移除背景网格线，但保留坐标轴
ax.grid(False)

# 显示图像
plt.tight_layout()
plt.show()
