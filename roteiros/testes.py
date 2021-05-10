import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

arr = np.array([
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
                ])
l = [[2, 2, 2], [4, 4, 4], [5, 5, 2]]
arr = np.array(l, dtype=int)
# sns.histplot(data=arr[0], discrete=True, color=(1, 0, 0, 1), multiple='stack')
# sns.histplot(data=arr[1], discrete=True, color=(0, 1, 0, 1),  multiple='stack')
# sns.histplot(data=arr[2], discrete=True, color=(0, 0, 1, 1),  multiple='stack')
df = pd.DataFrame(data=arr, columns=['red', 'green', 'blue'])
print(df)
sns.histplot(data=df, discrete=True, color=['r, g, b'] ,multiple='stack')


plt.show()