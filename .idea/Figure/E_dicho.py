import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# 读取数据
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/E_Dicho/E_Dicho_simplify.csv"
data = pd.read_csv(file_path)

# 选择需要的列并重命名
df = data[['Dataset/time', 'E_DichoAPI (average)', 'E_DichoWEB (average)', 'E_DichoDELTA']]
df.columns = ['Dataset', 'API', 'Web', 'Delta']

# 设置索引
df.set_index('Dataset', inplace=True)

# 移除包含 NaN 值的行
df_cleaned = df.dropna()

# 确保分数保留三位小数
df_cleaned = df_cleaned.round(3)

# 使用 sns.light_palette 创建一个浅色透明的颜色渐变，颜色越深代表分数越高
cmap = sns.light_palette("#F5A79E", as_cmap=True)

# 重新绘制热力图，并设置字体为Times New Roman
plt.figure(figsize=(14, 6))
sns.set(font='Times New Roman')

# 创建热力图
ax = sns.heatmap(df_cleaned, annot=True, fmt=".3f", cmap=cmap, cbar_kws={'orientation': 'vertical', 'shrink': 0.8}, annot_kws={"fontsize":18, "color": "black", "fontname": "Times New Roman"})

# 添加标题和标签，并设置字体
plt.title('Comparison of Ways on Different Datasets', fontsize=20, fontname='Times New Roman', pad=20)
plt.xlabel('Methods', fontsize=18, fontname='Times New Roman')
plt.ylabel('Datasets', fontsize=18, fontname='Times New Roman')

# 设置刻度字体
ax.set_xticklabels(ax.get_xticklabels(), fontsize=18, fontname='Times New Roman', rotation=0)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=16, fontname='Times New Roman')

ax.tick_params(left=True, bottom=True, length=10, width=2, colors='black', grid_color='black', grid_alpha=0.5, pad=10)

# 确保仅左边和下边显示边框
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    else:
        spine.set_visible(False)

# 调整色条位置和刻度标签
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=16, labelcolor='black')
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=16, fontname='Times New Roman')

# 添加色条标签到上方
cbar.ax.set_title('E_Dicho', fontsize=18, fontname='Times New Roman', pad=10)

# 显示图像
plt.tight_layout()
plt.show()

