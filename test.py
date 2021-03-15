import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression

dataset = load_boston()
df = pd.DataFrame(dataset.data, columns = dataset.feature_names)
df['MEDV'] = dataset.target

df.head()  # 상위 5개 행만 리턴하는 함수인듯

#---get the top 3 features that has the highest correlation---
print(df.corr().abs().nlargest(3, 'MEDV').index)
#---print the top 3 correlation values---
print(df.corr().abs().nlargest(3, 'MEDV').values[:,13])


plt.scatter(df['LSTAT'], df['MEDV'], marker='o')
plt.xlabel('LSTAT')
plt.ylabel('MEDV')
model = LinearRegression()
model.fit(X=df['LSTAT'].to_numpy().reshape(-1,1), y=df['MEDV'].to_numpy().reshape(-1,1))
plt.plot(df['LSTAT'], model.predict(df['LSTAT'].to_numpy().reshape(-1,1)), color='r')

plt.show()

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(18,15))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['LSTAT'],
 df['RM'],
 df['MEDV'],
 c='c')
ax.set_xlabel("LSTAT")
ax.set_ylabel("RM")
ax.set_zlabel("MEDV")
ax.view_init(10, 45)
plt.show()