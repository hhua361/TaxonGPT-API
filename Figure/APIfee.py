import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

# 读取用户上传的文件
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/API_fee/API fee.csv"
data_fee = pd.read_csv(file_path)

# 清理数据，将价格列转换为浮点数
data_fee['5 times money'] = data_fee['5 times money'].str.replace('$', '').astype(float)

# 创建一个三维图
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制三维散点图
scatter = ax.scatter(data_fee['species number'], data_fee['character number'], data_fee['5 times money'], c='#EF7A6D', marker='o', s=100, alpha=0.6)

# 添加坐标轴标签
ax.set_xlabel('Species Number', fontsize=18)
ax.set_ylabel('Character Number', fontsize=18)
ax.set_zlabel('API Fee (5 times)', fontsize=18)

# 添加标题
ax.set_title('Effect of Species and Character Numbers on API Fee', fontsize=20)

# 计算线性回归平面
X = data_fee[['species number', 'character number']]
X = sm.add_constant(X)
model = sm.OLS(data_fee['5 times money'], X).fit()
x_surf, y_surf = np.meshgrid(np.linspace(X['species number'].min(), X['species number'].max(), 100),
                             np.linspace(X['character number'].min(), X['character number'].max(), 100))
z_surf = model.params[0] + model.params[1] * x_surf + model.params[2] * y_surf

# 绘制线性回归平面
ax.plot_surface(x_surf, y_surf, z_surf, color='#9DC3E7', alpha=0.3)

# 添加回归方程到图像中
equation_text = f'API Fee = {model.params[0]:.2f} + {model.params[1]:.2f}*Species Number + {model.params[2]:.2f}*Character Number'
ax.text2D(0.05, 0.775, equation_text, transform=ax.transAxes, fontsize=16, color='black', horizontalalignment='left', verticalalignment='top')

# 调整视角
ax.view_init(elev=40, azim=120)

# 添加图例
scatter_proxy = plt.Line2D([0], [0], linestyle="none", c='#EF7A6D', marker='o')
surface_proxy = plt.Line2D([0], [0], linestyle="none", c='#9DC3E7', marker='s', markersize=10)
ax.legend([scatter_proxy, surface_proxy], ['Data Points', 'Regression Plane'], numpoints=1, loc='upper right', fontsize=12, frameon=True, fancybox=True, framealpha=0.7)

plt.show()

