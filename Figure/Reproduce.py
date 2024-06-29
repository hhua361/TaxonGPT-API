import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取用户上传的数据文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Reproducibility/Reproducibility.csv"
data = pd.read_csv(file_path)

# 自定义调色板
scatter_palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # 浅红色系
    '#9DC3E7', '#AED8F0', '#ADD8E6', '#BFECF9', '#D0F0FF', '#E0F7FF',  # 浅蓝色系
]

# 设置全局字体属性为新罗马字体
plt.rcParams['font.family'] = 'Times New Roman'

# 创建一个更加紧凑且美观的散点图
fig, ax = plt.subplots(figsize=(12, 6))

# 创建新的DataFrame来包含API和Web的不同方法
data_melted = pd.melt(data, id_vars=['dataset/time'], value_vars=['API', 'Web'],
                      var_name='Method', value_name='Reproducibility Score')

# 绘制小提琴图，不显示图例
sns.violinplot(x='Reproducibility Score', y='Method', data=data_melted, hue='Method',
               palette=['#F0AFA8', '#C0DAF2'], alpha=0.5, inner=None, linewidth=0.5, ax=ax, legend=False)

# 添加随机抖动到y轴位置
api_y_positions = np.random.uniform(-0.1, 0.1, len(data))
web_y_positions = np.random.uniform(0.9, 1.1, len(data))

# 绘制API结果的散点图，调整散点大小和边框颜色
sns.scatterplot(x=data['API'], y=api_y_positions, hue=data['dataset/time'], palette=scatter_palette, s=150, edgecolor='black', linewidth=0.5, ax=ax)
# 绘制Web结果的散点图，调整散点大小和边框颜色
sns.scatterplot(x=data['Web'], y=web_y_positions, hue=data['dataset/time'], palette=scatter_palette, s=150, edgecolor='black', linewidth=0.5, ax=ax, legend=False)

# 调整y轴标签以区分API和Web结果
ax.set_yticks([0, 1])
ax.set_yticklabels(['API', 'Web'])

# 设置轴标签和标题
ax.set_xlabel('Reproducibility Score', fontsize=20)
ax.set_ylabel('Method', fontsize=20)
ax.set_title('Reproducibility Scores for API and Web Methods', fontsize=22)

# 调整刻度标签的字体大小
ax.tick_params(axis='both', which='major', labelsize=16)

# 美化图例
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title='Dataset/Time', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, title_fontsize=16)

# 美化图表
sns.despine()

plt.tight_layout()
plt.show()
