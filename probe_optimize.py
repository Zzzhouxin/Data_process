import pickle

with open('./process_pip/select_probe_temp/probability_matrix.pkl', "rb") as file:
    probability_matrix = pickle.load(file)

import numpy as np
from scipy.optimize import minimize


def objective_function(x, p):
    p = np.array(p, dtype=float)  # 将特征概率转换为NumPy数组
    return -np.sum(x * p)  # 计算加权和


def constraint_function(x):
    return np.sum(x) - 5


def optimize_probe_selection(p, num_requests):
    x0 = np.zeros(num_requests)

    constraints = [{'type': 'ineq', 'fun': constraint_function}]

    problem = minimize(objective_function, x0, args=(p,), method='SLSQP', constraints=constraints)

    optimal_selection = problem.x

    return optimal_selection


# 探测请求的特征概率
probabilities = []
for i in range(1, len(probability_matrix[0])):
    probabilities.append((float(probability_matrix[0][i]['hasServer_probability'].strip('%'))))

# 优化选择
optimal_selection = optimize_probe_selection(probabilities, len(probabilities))

# 输出最优选择的探测请求
for i, selection in enumerate(optimal_selection):
    print(selection)
    if selection == 1:
        print(f"选择探测请求 {i + 1}")
