import numpy as np
import imgx.morphology.operations as op
import time

se = [[0, 1, 0],
      [1, 1, 1],
      [0, 1, 0]]

# se = [[0, 1, 0, 0, 0],
#       [1, 1, 1, 0, 0],
#       [0, 1, 0, 0, 0],
#       [0, 1, 0, 0, 0],
#       [0, 1, 0, 0, 0]]

img = [[0, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 1, 1, 0, 1, 0],
       [0, 1, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 0]]

img = np.array(img, dtype=int)

# img = np.zeros(shape=(3000, 1500), dtype=int)

t1 = time.time()
print(op.erode(img, np.array(se, dtype=int)))
t2 = time.time()
print(t2 - t1)
