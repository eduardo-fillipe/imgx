import numpy as np
import imgx.morphology.operations as op

se = [[0, 1, 0],
      [1, 1, 1],
      [0, 1, 0]]

img = [[0, 0, 0, 0, 0, 0],
       [0, 1, 0, 1, 1, 0],
       [0, 1, 1, 0, 0, 0],
       [0, 1, 1, 1, 0, 1],
       [1, 0, 0, 0, 1, 0],
       [0, 1, 0, 1, 0, 1]]

img = np.zeros(shape=(3000, 1500), dtype=int)


print(op.dilate(img, np.array(se, dtype=int)))