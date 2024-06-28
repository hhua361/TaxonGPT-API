import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取CSV文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Running_Time/Running time.csv"  # 修改为你的文件路径
data = pd.read_csv(file_path)

# 清洗和整理数据，将每个数据集的5次实验结果分别处理
api_data = data.melt(id_vars=['dataset/time'], value_vars=['API time1', 'API time2', 'API time3', 'API time4', 'API time5'],
                     var_name='Trial', value_name='Runtime')
api_data['Method'] = 'API'

web_data = data.melt(id_vars=['dataset/time'], value_vars=['WEB time1', 'WEB time2', 'WEB time3', 'WEB time4', 'WEB time5'],
                     var_name='Trial', value_name='Runtime')
web_data['Method'] = 'Web'

# 合并API和Web数据
combined_data = pd.concat([api_data, web_data])

# 更改列名
combined_data.rename(columns={'dataset/time': 'Dataset'}, inplace=True)

# 设置字体
plt.rcParams["font.family"] = "Times New Roman"

# 设置样式
sns.set(style="whitegrid")

# 定义颜色
api_color = '#EF7A6D'  # 浅红色
web_color = '#9DC3E7'  # 浅蓝色
palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # 浅红色系
    '#9DC3E7', '#AED8F0', '#ADD8E6','#BFECF9', '#D0F0FF', '#E0F7FF',  # 浅蓝色系
]

# 绘制箱型图和散点图
plt.figure(figsize=(14, 8))

# 绘制API方法的箱型图，设置颜色
ax = sns.boxplot(data=combined_data[combined_data['Method'] == 'API'], x='Method', y='Runtime', showfliers=False, width=0.6, linewidth=1.7, boxprops=dict(facecolor='none', edgecolor='black'), medianprops=dict(color='black'))

# 绘制Web方法的箱型图，设置颜色
sns.boxplot(data=combined_data[combined_data['Method'] == 'Web'], x='Method', y='Runtime', showfliers=False, width=0.6, linewidth=1.7, boxprops=dict(facecolor='none', edgecolor='black'), medianprops=dict(color='black'))

# 绘制散点图，保留不同数据集的颜色，统一色调
sns.stripplot(data=combined_data, x='Method', y='Runtime', hue='Dataset', dodge=True, jitter=0.2, marker='o', palette=palette, alpha=1, linewidth=1, edgecolor='auto', s=15)

# 标注中位数
medians = combined_data.groupby(['Method'])['Runtime'].median().values
for i, median in enumerate(medians):
    ax.text(i, median + 2, f'{int(median)}', ha='center', va='bottom', fontweight='bold', color='grey', fontsize=18, family='Times New Roman')

# 调整图例
legend = plt.legend(title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, title_fontsize=16)
plt.setp(legend.get_title(), family='Times New Roman')  # 设置图例标题字体
for text in legend.get_texts():
    text.set_family('Times New Roman')  # 设置图例标签字体

# 设置图像标题和标签
plt.title('Comparison of Runtime between API and Web Methods', fontsize=22, family='Times New Roman',pad=20)
plt.xlabel('Methods', fontsize=20, family='Times New Roman')
plt.ylabel('Runtime (seconds)', fontsize=20, family='Times New Roman', labelpad=20)  # 调整labelpad增加距离

# 设置坐标轴刻度
plt.xticks(fontsize=18, family='Times New Roman')
plt.yticks(fontsize=18, family='Times New Roman')

ax.grid(False)

# 显示图像
plt.tight_layout()
plt.show()

