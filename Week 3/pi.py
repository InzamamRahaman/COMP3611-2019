
import numpy as np

def in_circle(x, y):
    return x * x + y * y <= 1.0

def compute_pi(nruns=500000):
    count = 0.0
    xs = np.random.uniform(-1,1,nruns)
    ys = np.random.uniform(-1,1,nruns)
    for x, y in zip(xs, ys):
        if in_circle(x, y):
            count += 1.0
    ratio = count / nruns
    return ratio * 4

print(compute_pi())



