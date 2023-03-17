### Code #####################################################################

import numpy as np
import random
import timeit

#Create the Ant Class
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_eaten = 0
    
    # Randomize each ants' action (up, down, left, right)
    def action(self):
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            self.y = min(self.y + 1, 99)
        elif direction == "down":
            self.y = max(self.y - 1, 0)
        elif direction == "left":
            self.x = max(self.x - 1, 0)
        elif direction == "right":
            self.x = min(self.x + 1, 99)
    
    # Consume the food
    def consume(self, food_loc):
        if (self.x, self.y) in food_loc:
            food_loc.remove((self.x, self.y)) 
            self.food_eaten += 1
# Create the Grid World for the Ants
class Simulation:
    def __init__(self, num_ants, num_food):
        self.num_ants = num_ants
        self.num_food = num_food
        self.food_loc = self._generate_food_locations()
        self.ants = self._generate_ants()
    
    # Spawn the food
    def _generate_food_locations(self):
        # Generate a set of random food locations that do not overlap
        food_loc = set()
        while len(food_loc) < self.num_food:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            food_loc.add((x, y))
        return food_loc

    #Spawn the ants... if ants spawn on food, consume it
    def _generate_ants(self):
        ants = []
        while len(ants) < self.num_ants:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            if (x, y) not in self.food_loc:
                ants.append(Ant(x, y))
            else:
                ant = Ant(x,y)
                self.food_loc.remove((x,y))
                ant.food_eaten +=1
                ants.append(ant)
        return ants
    
    # run the action of the ants in the Grid World
    def run(self, num_steps):
        for _ in range(num_steps):
            for ant in self.ants:
                ant.action()
                ant.consume(self.food_loc)

#build the simulation
def run_simulations(num_simulations, num_ants, num_food, num_steps):
    results = []
    for _ in range(num_simulations):
        sim = Simulation(num_ants, num_food)
        sim.run(num_steps)
        total_food_eaten = sum(ant.food_eaten for ant in sim.ants)
        results.append(total_food_eaten)
    return results

# Run 1000 simulations with 100 ants... each for 100 time steps

results = run_simulations(1000, 100, 10, 100)


# Calculate the mean and standard deviation of the total food eaten
mean = sum(results) / len(results)
std_dev = np.sqrt(sum((x - mean) ** 2 for x in results) / len(results))

print(f"Mean: {mean}, Standard Deviation: {std_dev}")


### Execution Time ############################################################
code_time = '''
import numpy as np
import random

#Create the Ant Class
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_eaten = 0
    
    # Randomize each ants' action (up, down, left, right)
    def action(self):
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            self.y = min(self.y + 1, 99)
        elif direction == "down":
            self.y = max(self.y - 1, 0)
        elif direction == "left":
            self.x = max(self.x - 1, 0)
        elif direction == "right":
            self.x = min(self.x + 1, 99)
    
    # Consume the food
    def consume(self, food_loc):
        if (self.x, self.y) in food_loc:
            food_loc.remove((self.x, self.y)) 
            self.food_eaten += 1
# Create the Grid World for the Ants
class Simulation:
    def __init__(self, num_ants, num_food):
        self.num_ants = num_ants
        self.num_food = num_food
        self.food_loc = self._generate_food_locations()
        self.ants = self._generate_ants()
    
    # Spawn the food
    def _generate_food_locations(self):
        # Generate a set of random food locations that do not overlap
        food_loc = set()
        while len(food_loc) < self.num_food:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            food_loc.add((x, y))
        return food_loc

    #Spawn the ants... if ants spawn on food, consume it
    def _generate_ants(self):
        ants = []
        while len(ants) < self.num_ants:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            if (x, y) not in self.food_loc:
                ants.append(Ant(x, y))
            else:
                ant = Ant(x,y)
                self.food_loc.remove((x,y))
                ant.food_eaten +=1
                ants.append(ant)
        return ants
    
    # run the action of the ants in the Grid World
    def run(self, num_steps):
        for _ in range(num_steps):
            for ant in self.ants:
                ant.action()
                ant.consume(self.food_loc)

#build the simulation
def run_simulations(num_simulations, num_ants, num_food, num_steps):
    results = []
    for _ in range(num_simulations):
        sim = Simulation(num_ants, num_food)
        sim.run(num_steps)
        total_food_eaten = sum(ant.food_eaten for ant in sim.ants)
        results.append(total_food_eaten)
    return results

# Run 1000 simulations with 100 ants... each for 100 time steps
results = run_simulations(1000, 100, 10, 100)

# Calculate the mean and standard deviation of the total food eaten
mean = sum(results) / len(results)
std_dev = np.sqrt(sum((x - mean) ** 2 for x in results) / len(results))

print(f"Mean: {mean}, Standard Deviation: {std_dev}")

'''
execution_time = timeit.timeit(code_time, number=1)
print(f"Execution time: {execution_time:.5f} seconds")


### UNIT TESTING ##############################################################
import unittest

class TestSimulation(unittest.TestCase):
    def test_init_no_ants_no_food(self):
        sim = Simulation(0, 0)
        self.assertEqual(sim.num_ants, 0)
        self.assertEqual(sim.num_food, 0)
        self.assertEqual(sim.food_loc, set())
        self.assertEqual(sim.ants, [])
        
    def test_init_one_ant_no_food(self):
        sim = Simulation(1, 0)
        self.assertEqual(sim.num_ants, 1)
        self.assertEqual(sim.num_food, 0)
        self.assertEqual(sim.food_loc, set())
        self.assertEqual(len(sim.ants), 1)
        
    def test_init_one_ant_one_food(self):
        sim = Simulation(1, 1)
        self.assertEqual(sim.num_ants, 1)
        self.assertEqual(sim.num_food, 1)
        self.assertEqual(len(sim.food_loc), 1)
        self.assertEqual(len(sim.ants), 1)
        self.assertEqual(sim.ants[0].food_eaten, 0)
        
    def test_init_two_ants_one_food(self):
        sim = Simulation(2, 1)
        self.assertEqual(sim.num_ants, 2)
        self.assertEqual(sim.num_food, 1)
        self.assertEqual(len(sim.food_loc), 1)
        self.assertEqual(len(sim.ants), 2)
        self.assertEqual(sim.ants[0].food_eaten + sim.ants[1].food_eaten, 0)

# Run the test cases
unittest.main()
### END ######################################################################


