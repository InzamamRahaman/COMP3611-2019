import numpy as np 

def f(x):
    return 2 * x + 1

def g(x):
    return x ** x ** x 

def h(x, y):
    return x ** 2 + y ** 2

def simple_integral(f, a, b, n_samples=50000):
    areas = []
    for i in range(n_samples):
        x = np.random.uniform(a, b)
        area = (b - a) * f(x)
        areas.append(area)
    return np.mean(areas)

def double_integral(f, a, b, c, d, n_samples=50000):
    areas = []
    for i in range(n_samples):
        x = np.random.uniform(a, b)
        y = np.random.uniform(c, d)
        area = (b - a) * (d  - c) * f(x, y)
        areas.append(area)
    return np.mean(areas)

def integral(n_samples, f, *args):
    volumes = []
    bounds = list(args)
    n = len(bounds) // 2
    for i in range(n_samples):
        coords = []
        for j in range(0,n+2,2):
            coords.append(np.random.uniform(bounds[j], bounds[j + 1]))
        volume = f(*coords)
        volumes.append(volume)
    return np.mean(volumes)

def a_func(x, y, z):
    return x**2 + y**3 + z**4


print(simple_integral(g, 0, 2))
print(double_integral(h, 0, 2, 1, 3))
print(integral(100000, a_func, 0, 1, 2, 3, 4, 5))

