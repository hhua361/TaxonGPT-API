import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 读取CSV文件
file_path = 'E:/Evaluate_results_for_all_datasets/Evaluate_table/Running_Time/Running time.csv'
data = pd.read_csv(file_path)

# 提取API和WEB运行时间
data_api = data[['dataset/time', 'API time', 'species number', 'character numbers']]
data_api = data_api.rename(columns={'API time': 'Runtime'})
data_api['Program'] = 'API'

data_web = data[['dataset/time', 'WEB time', 'species number', 'character numbers']]
data_web = data_web.rename(columns={'WEB time': 'Runtime'})
data_web['Program'] = 'WEB'

# 合并数据
data_combined = pd.concat([data_api, data_web])

# 设置字体
plt.rcParams['font.family'] = 'Times New Roman'

# 绘制API和WEB程序的运行时间与物种数量的关系
plt.figure(figsize=(12, 6))
sns.scatterplot(data=data_combined, x='species number', y='Runtime', hue='Program', style='Program', markers=["o", "X"], s=100, palette={'API': '#D76364', 'WEB': '#5F97D2'})
sns.regplot(data=data_combined[data_combined['Program'] == 'API'], x='species number', y='Runtime', scatter=False, color='#EF7A6D',line_kws={'linewidth': 3}, label='API fit')
sns.regplot(data=data_combined[data_combined['Program'] == 'WEB'], x='species number', y='Runtime', scatter=False, color='#9DC3E7',line_kws={'linewidth': 3}, label='WEB fit')
plt.xlabel('Species Number', fontsize=18, fontname='Times New Roman')
plt.ylabel('Runtime (seconds)', fontsize=18, fontname='Times New Roman')
plt.title('Runtime with different Species Number', fontsize=20, fontname='Times New Roman')
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = ['API', 'Web', 'API fit', 'Web fit']
plt.legend(handles=handles[0:], labels=new_labels, title='Type')
plt.ylim(0, None)
plt.show()

# 绘制API和WEB程序的运行时间与形态特征数量的关系
plt.figure(figsize=(12, 6))
sns.scatterplot(data=data_combined, x='character numbers', y='Runtime', hue='Program', style='Program', markers=["o", "X"], s=100,palette={'API': '#D76364', 'WEB': '#5F97D2'})
sns.regplot(data=data_combined[data_combined['Program'] == 'API'], x='character numbers', y='Runtime', scatter=False, color='#EF7A6D', line_kws={'linewidth': 3},label='API fit')
sns.regplot(data=data_combined[data_combined['Program'] == 'WEB'], x='character numbers', y='Runtime', scatter=False, color='#9DC3E7', line_kws={'linewidth': 3},label='WEB fit')
plt.xlabel('Character Numbers', fontsize=18, fontname='Times New Roman')
plt.ylabel('Runtime (seconds)', fontsize=18, fontname='Times New Roman')
plt.title('Runtime with different Character Numbers', fontsize=20, fontname='Times New Roman')
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = ['API', 'Web', 'API fit', 'Web fit']
plt.legend(handles=handles[0:], labels=new_labels, title='Type')
plt.ylim(0, None)
plt.show()
