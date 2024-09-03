import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_valid.csv"
data = pd.read_csv(file_path)

# 移除第一行（包含方法的列名）
data_cleaned = data.drop(0)

# 函数将百分比字符串转换为浮点数
def convert_to_float(value):
    if isinstance(value, str) and '%' in value:
        return float(value.replace('%', '')) / 100
    return float(value)

# 应用转换到相关列
for col in data_cleaned.columns[1:]:
    data_cleaned[col] = data_cleaned[col].apply(convert_to_float)

# 提取数据集、api_data 和 web_data
datasets = data_cleaned['Valid-state'].values
api_data = data_cleaned.iloc[:, 1:6].values
web_data = data_cleaned.iloc[:, 6:11].values

# 改进的条形图，具有增强的美学效果
fig, ax1 = plt.subplots(figsize=(16, 7))

# 为每个数据集绘图
width = 0.6  # 条形的宽度
x_labels = []

methods = ['API', 'Web']  # 定义方法用于定位
x = np.arange(len(datasets) * 2, step=2)  # 增加组之间的间距

api_means_list = []
web_means_list = []
p_values = []

for i, dataset in enumerate(datasets):
    api_means = api_data[i].mean()
    api_errors = api_data[i].std() / np.sqrt(len(api_data[i]))
    web_means = web_data[i].mean()
    web_errors = web_data[i].std() / np.sqrt(len(web_data[i]))

    api_means_list.append(api_means)
    web_means_list.append(web_means)

    ax1.bar(x[i] - width/2, api_means, width, yerr=api_errors, capsize=8, color='#F0AFA8', label='API' if i == 0 else "")
    ax1.bar(x[i] + width/2, web_means, width, yerr=web_errors, capsize=8, color='#C0DAF2', label='Web' if i == 0 else "")
    x_labels.extend([f'{dataset}'])

    # 计算 t 检验的 p 值
    t_stat, p_val = ttest_ind(api_data[i], web_data[i])
    p_values.append(p_val)

# 设置字体为Arial
plt.rc('font', family='Arial')
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels, rotation=0, ha='center', fontsize=12, family='Arial')
ax1.set_ylabel('Valid Classification State Probability', fontsize=18, family='Arial')
ax1.set_ylim(0.95, 1.1)  # 调整y轴范围以提高可见性

# 为折线图添加第二个y轴
ax2 = ax1.twinx()
ax2.plot(x, api_means_list, marker='o', color='#EF7A6D', label='API Mean', linewidth=4)
ax2.plot(x, web_means_list, marker='o', color='#9DC3E7', label='Web Mean', linewidth=4)
ax2.set_ylim(0.8, 1.1)  # 确保折线图的y轴范围与条形图的y轴范围一致

# 为两个图添加图例
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

fig.legend(handles, labels, fontsize=12, loc='upper right', bbox_to_anchor=(1, 1), ncol=1, prop={'family': 'Arial'})

fig.suptitle('Comparison of Valid Classification State Probability for Each Dataset between API and Web Methods', fontsize=22, family='Arial')
plt.grid(False)  # 移除网格线
plt.tight_layout()

# 添加显著性标记
def add_significance(ax, x1, x2, y, h, p_val):
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color='black')
    ax.text((x1 + x2) * .5, y + h, f'p={p_val:.3f}', ha='center', va='bottom', color='black', fontsize=12)

# 获取所有条形的高度
max_height = 1.05  # 预设的最大高度

# 根据 t 检验的 p 值添加显著性标记
for i in range(len(datasets)):
    x1 = x[i] - width/2
    x2 = x[i] + width/2
    y = max(api_means_list[i], web_means_list[i])  # 获取每组最大值作为y的基准
    h = 0.02  # 显著性标记的高度
    add_significance(ax1, x1, x2, y, h, p_values[i])

# 保存为SVG格式
output_path = 'E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_valid.svg'
plt.savefig(output_path, format='svg')

# 显示图像
plt.show()
