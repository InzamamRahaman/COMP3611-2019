import numpy as np

# Sampling from a binomial distribution
sample = np.random.binomial(5, 0.5, 500)
print(sample)
print(np.mean(sample)) # should be 2.5 = n * p
print(np.std(sample))

def my_binomial(n, p):
    num_successes = 0
    # for each trail
    for i in range(n):
        # run trail
        x = np.random.random()
        # if trail is successful
        if x <= p:
            num_successes += 1
    return num_successes

def binomial(n, p, size=1):
    successes = []
    # for each experiment
    for i in range(size):
        successes.append(my_binomial(n, p))
    return successes

sample = binomial(5, 0.5, 10000)
print(sample)
print(np.mean(sample)) # should be 2.5 = n * p
print(np.std(sample)) # should n * p * (1 - p)

# poisson distribution
sample = np.random.poisson(5, 1000)
print(sample)
print(np.mean(sample)) # mean should be 5
print(np.std(sample))

# normal distribution
sample = np.random.normal(125, np.sqrt(30), 1000)
print(sample)
print(np.mean(sample))
print(np.std(sample))

# exponentail
sample = np.random.exponential(5, 1000)
print(sample)
print(np.mean(sample))
print(np.std(sample))

# multinomial
print('Dice rolls')
numbers = [1, 2, 3, 4, 5, 6]
probs = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
sample = np.random.choice(numbers, size=1000,
                          p=probs)
print(sample)
print(np.mean(sample))
print(np.std(sample))





