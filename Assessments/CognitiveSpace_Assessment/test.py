import time
import random
import numpy as np

class GridWorld:
    def __init__(self, size, num_food, num_ants):
        self.size = size
        self.num_food = num_food
        self.food = self.create_food()
        self.num_ants = num_ants
        self.ants = self.create_ants()
    
    def create_food(self):
        food = []
        for _ in range(self.num_food):
            x, y = self.random_coordinates()
            food.append(Food(x, y))
        return food
    
    def create_ants(self):
        ants = []
        for _ in range(self.num_ants):
            x, y = self.random_coordinates()
            ants.append(Ant(x, y, self))
        return ants
    
    def random_coordinates(self):
        return random.randint(0, self.size-1), random.randint(0, self.size-1)
    
    def simulate(self, num_steps):
        for step in range(num_steps):
            for ant in self.ants:
                ant.move()
    
    def get_total_food_eaten(self):
        return sum([ant.food_eaten for ant in self.ants])

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ant:
    def __init__(self, x, y, grid_world):
        self.x = x
        self.y = y
        self.grid_world = grid_world
        self.food_eaten = 0
    
    def move(self):
        direction = random.randint(0, 3)
        if direction == 0:
            self.x += 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x -= 1
        else:
            self.y -= 1
        self.x = max(0, self.x)
        self.x = min(self.grid_world.size-1, self.x)
        self.y = max(0, self.y)
        self.y = min(self.grid_world.size-1, self.y)
        self.eat_food()
    
    def eat_food(self):
        for food in self.grid_world.food:
            if food.x == self.x and food.y == self.y:
                self.grid_world.food.remove(food)
                self.food_eaten += 1

# Run the simulations
num_simulations = 1000
num_steps = 100
size = 100
num_food = 10
num_ants = 100

food_eaten = []
start_time = time.perf_counter()
for i in range(num_simulations):
    grid_world = GridWorld(size, num_food, num_ants)
    grid_world.simulate(num_steps)
    food_eaten.append(grid_world.get_total_food_eaten())
end_time = time.perf_counter()

# Calculate the mean and standard deviation of the total food eaten
mean = np.mean(food_eaten)
std = np.std(food_eaten)

print(f"Mean food eaten: {mean}")
print(f"Standard deviation of food eaten: {std}")

# Calculate the time elapsed
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")


#######################################

import numpy as np
import random
import time

class GridWorld:
    def __init__(self, size, num_food, num_ants):
        self.size = size
        self.num_food = num_food
        self.food = self.create_food()
        self.num_ants = num_ants
        self.ants = self.create_ants()
    
    def create_food(self):
        food = []
        for _ in range(self.num_food):
            x, y = self.random_coordinates()
            food.append(Food(x, y))
        return food
    
    def create_ants(self):
        ants = {}
        for _ in range(self.num_ants):
            x, y = self.random_coordinates()
            ant = Ant(x, y, self)
            ants[(x, y)] = ant
        return ants
    
    def random_coordinates(self):
        return random.randint(0, self.size-1), random.randint(0, self.size-1)
    
    def simulate(self, num_simulations, num_steps):
        results = []
        for i in range(num_simulations):
            self.reset()
            for step in range(num_steps):
                for coord, ant in self.ants.items():
                    ant.move()
            total_food_eaten = self.get_total_food_eaten()
            results.append(total_food_eaten)
        mean = np.mean(results)
        std = np.std(results)
        return mean, std
    
    def reset(self):
        self.food = self.create_food()
        self.ants = self.create_ants()
    
    def get_total_food_eaten(self):
        return sum([ant.food_eaten for ant in self.ants.values()])

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ant:
    def __init__(self, x, y, grid_world):
        self.x = x
        self.y = y
        self.grid_world = grid_world
        self.food_eaten = 0
    
    def move(self):
        direction = random.randint(0, 3)
        if direction == 0:
            self.x += 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x -= 1
        else:
            self.y -= 1
        self.x = max(0, self.x)
        self.x = min(self.grid_world.size-1, self.x)
        self.y = max(0, self.y)
        self.y = min(self.grid_world.size-1, self.y)
        self.eat_food()
    def eat_food(self):
        for food in self.grid_world.food:
            if food.x == self.x and food.y == self.y:
                self.grid_world.food.remove(food)
                self.food_eaten += 1
                break

# Run 1000 simulations with 100 ants, each for 100 time steps
grid_world = GridWorld(100, 10, 100)
start_time = time.perf_counter()
mean, std = grid_world.simulate(1000, 100)
end_time = time.perf_counter()

# Calculate elapsed time
elapsed_time = end_time - start_time

print(f"Mean: {mean}, Standard Deviation: {std}")
print(f"Elapsed time: {elapsed_time:.2f} seconds")

import numpy as np
import random
import time

class GridWorld:
    def __init__(self, size, num_food, num_ants):
        self.size = size
        self.num_food = num_food
        self.food = self.create_food()
        self.num_ants = num_ants
        self.ants = self.create_ants()
    
    def create_food(self):
        food = set()
        food_locations = random.sample(range(self.size * self.size), self.num_food)
        for location in food_locations:
            x, y = location % self.size, location // self.size
            food.add((x, y))
        return food
    
    def create_ants(self):
        ants = {}
        ant_locations = random.sample(range(self.size * self.size), self.num_ants)
        for location in ant_locations:
            x, y = location % self.size, location // self.size
            ant = Ant(x, y, self)
            ants[(x, y)] = ant
        return ants
    
    def simulate(self, num_simulations, num_steps):
        results = []
        for i in range(num_simulations):
            self.reset()
            for step in range(num_steps):
                for coord, ant in self.ants.items():
                    ant.move()
            total_food_eaten = self.get_total_food_eaten()
            results.append(total_food_eaten)
        mean = np.mean(results)
        std = np.std(results)
        return mean, std
    
    def reset(self):
        self.food = self.create_food()
        self.ants = self.create_ants()
    
    def get_total_food_eaten(self):
        return sum([ant.food_eaten for ant in self.ants.values()])
class Ant:
    def __init__(self, x, y, grid_world):
        self.x = x
        self.y = y
        self.grid_world = grid_world
        self.food_eaten = 0
    
    def move(self):
        direction = random.randint(0, 3)
        if direction == 0:
            self.x += 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x -= 1
        else:
            self.y -= 1
        self.x = max(0, self.x)
        self.x = min(self.grid_world.size-1, self.x)
        self.y = max(0, self.y)
        self.y = min(self.grid_world.size-1, self.y)
        self.eat_food()
    
    def eat_food(self):
        if (self.x, self.y) in self.grid_world.food:
            self.grid_world.food.remove((self.x, self.y))
            self.food_eaten += 1

# Run 1000 simulations with 100 ants, each for 100 time steps
grid_world = GridWorld(100, 10, 100)
start_time = time.perf_counter()
mean, std = grid_world.simulate(1000, 100)
end_time = time.perf_counter()

# Calculate elapsed time
elapsed_time = end_time - start_time

print(f"Mean: {mean}, Standard Deviation: {std}")
print(f"Elapsed time: {elapsed_time:.2f} seconds")