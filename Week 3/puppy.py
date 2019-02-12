import numpy as np

def sample_letter():
    letters = ['P', 'U', 'Y', 'LOL']
    probs = [0.05, 0.5, 0.05, 0.40]
    letter = np.random.choice(letters,
                              size=1,
                              p=probs)
    return letter[0]

def sample_dog_type():
    dogs = ['big', 'med', 'tiny']
    probs = [0.4, 0.3, 0.3]
    dog = np.random.choice(dogs, size=1, p=probs)
    dog = dog[0]
    return dog


def sample_num_weeks_food_lasts(dog_type):
    rates = {
        'big': ([1, 2, 3], [0.5, 0.3, 0.2]),
        'med': ([1, 2, 3], [0.25, 0.5, 0.25]),
        'tiny': ([1, 2, 3], [0.2, 0.3, 0.5])
    }
    weeks = rates[dog_type][0]
    probs = rates[dog_type][1]
    week = np.random.choice(weeks, size=1, p=probs)
    week = week[0]
    return week

def won(counts):
    if counts['P'] >= 3 and counts['U'] >= 1 and counts['Y'] >= 1:
        return True
    return False


def simulate_customer():
    counts = {
        'P': 0,
        'U': 0,
        'Y': 0,
        'LOL': 0
    }
    dog = sample_dog_type()
    weeks = 0
    num_bags = 0
    week_last = 0
    while not won(counts):
        letter = sample_letter()
        counts[letter] += 1
        num_bags += 1
        week_last = sample_num_weeks_food_lasts(dog)
        weeks += week_last
    weeks -= week_last
    return num_bags, weeks

def simulate(nruns=1000):
    customers = []
    weeks = []
    for i in range(nruns):
        num_bags, num_weeks = simulate_customer()
        customers.append(num_bags)
        weeks.append(num_weeks)
    customers = np.array(customers)
    weeks = np.array(weeks)
    return customers, weeks

sample_num_bags, sample_weeks = simulate(5000)
print(np.mean(sample_num_bags))
print(np.mean(sample_weeks))
print(sum(sample_weeks <= 25))
print(np.mean(sample_num_bags[sample_weeks <= 25]))