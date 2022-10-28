#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 22:39
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : WFO.py
# @Statement : Water Flow Optimizer
# @Reference : Luo K. Water flow optimizer: a nature-inspired evolutionary algorithm for global optimization[J]. IEEE Transactions on Cybernetics, 2021.
import random
import copy
import math
import matplotlib.pyplot as plt


def obj(x):
    """
    The objective function of pressure vessel design
    :param x:
    :return:
    """
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    x4 = x[3]
    g1 = -x1 + 0.0193 * x3
    g2 = -x2 + 0.00954 * x3
    g3 = -math.pi * x3 ** 2 - 4 * math.pi * x3 ** 3 / 3 + 1296000
    g4 = x4 - 240
    if g1 <= 0 and g2 <= 0 and g3 <= 0 and g4 <= 0:
        return 0.6224 * x1 * x3 * x4 + 1.7781 * x2 * x3 ** 2 + 3.1661 * x1 ** 2 * x4 + 19.84 * x1 ** 2 * x3
    else:
        return 1e10


def random_select(max_num, num):
    """
    Randomly select number in range [0, max_num - 1] except num
    :param max_num:
    :param num:
    :return:
    """
    new_num = random.randint(0, max_num - 1)
    while new_num == num:
        new_num = random.randint(0, max_num - 1)
    return new_num


def main(pop, iter, pl, pe, lbound, ubound):
    """
    The main function of the WFO
    :param pop: the number of water particles
    :param iter: the number of iterations
    :param pl: laminar probability
    :param pe: eddying probability
    :param lbound: the lower bound (list)
    :param ubound: the upper bound (list)
    :return:
    """
    # Step 1. Initialization
    dim = len(lbound)  # dimension
    score = []  # the objective value of particles
    position = []  # the position of particles
    for i in range(pop):
        temp_position = [random.uniform(lbound[j], ubound[j]) for j in range(dim)]
        position.append(temp_position)
        score.append(obj(temp_position))
    best_score = min(score)  # the best-so-far score
    best_position = position[score.index(best_score)]  # the position of best_score
    iter_best = []  # the global best value of each iteration
    con_iter = 0  # the iteration number of convergence

    # Step 2. The main loop
    for t in range(iter):
        possible_pos = []
        possible_score = []
        if random.random() < pl:
            # laminar operation
            temp_pos = random.choice(position)
            dis = [best_position[j] - temp_pos[j] for j in range(dim)]
            for i in range(pop):
                temp_num = random.random()
                new_pos = copy.deepcopy(position[i])
                for j in range(dim):
                    new_num = new_pos[j] + temp_num * dis[j]
                    if lbound[j] <= new_num <= ubound[j]:
                        new_pos[j] = new_num
                possible_pos.append(new_pos)
                possible_score.append(obj(new_pos))
        else:
            # turbulent operation
            for i in range(pop):
                temp_pos = copy.deepcopy(position[i])
                selected_index = random_select(pop, i)
                selected_position = position[selected_index]
                dim1 = random.randint(0, dim - 1)
                if random.random() < pe:
                    # eddying
                    rho = abs(temp_pos[dim1] - selected_position[dim1])
                    theta = random.uniform(-math.pi, math.pi)
                    new_pos = temp_pos[dim1] + rho * theta * math.cos(theta)
                    if lbound[dim1] <= new_pos <= ubound[dim1]:
                        temp_pos[dim1] = new_pos
                    possible_pos.append(temp_pos)
                    possible_score.append(obj(temp_pos))
                else:
                    # over-layer moving
                    dim2 = random_select(dim, dim1)
                    temp_pos[dim1] = (ubound[dim1] - lbound[dim1]) * (selected_position[dim2] - lbound[dim2]) / (ubound[dim2] - lbound[dim2]) + lbound[dim1]
                    possible_pos.append(temp_pos)
                    possible_score.append(obj(temp_pos))

        # Evolving and updating
        for i in range(pop):
            if possible_score[i] < score[i]:
                position[i] = copy.deepcopy(possible_pos[i])
                score[i] = possible_score[i]
                if possible_score[i] < best_score:
                    best_position = copy.deepcopy(possible_pos[i])
                    best_score = possible_score[i]
                    con_iter = t
        iter_best.append(best_score)

    # Step 3. Sort the results
    x = [i for i in range(iter)]
    plt.figure()
    plt.plot(x, iter_best, linewidth=2, color='blue')
    plt.xlabel('Iteration number')
    plt.ylabel('Global optimal value')
    plt.title('Convergence curve')
    plt.show()
    return {'best solution': best_position, 'best score': best_score, 'convergence iteration': con_iter}


if __name__ == '__main__':
    # Parameter settings
    pop = 50
    iter = 3000
    pl = 0.3
    pe = 0.7
    lbound = [0, 0, 10, 10]
    ubound = [100, 100, 100, 100]
    print(main(pop, iter, pl, pe, lbound, ubound))
