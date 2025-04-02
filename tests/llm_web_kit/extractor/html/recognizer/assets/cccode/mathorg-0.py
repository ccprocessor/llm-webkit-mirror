import numpy as np
import matplotlib.pyplot as plt


f = np.poly1d([1, 0, 0, -1])
df = np.polyder(f)

def iterate(z):
    i = 0
    while abs(f(z)) > 0.0001:
        with np.errstate(all='ignore'):
            w = z - f(z)/df(z)
            i += np.exp(-1/abs(w-z))
            z = w
    return i

y, x = np.ogrid[1:-1:600j, -1:1:600j]
z = x + y*1j
img = np.frompyfunc(iterate, 1, 1)(z).astype(np.float)
fig = plt.figure(figsize=(4, 4), dpi=100)
ax = fig.add_axes([0, 0, 1, 1], aspect=1)
ax.axis('off')
ax.imshow(img, cmap='hot')
fig.savefig('newton.png')
复制代码