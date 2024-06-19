import pickle
from deap import base, creator, tools
import random


def evaluation_function(individual):
    """
    评估一个individual是否适合用来深度探测
    @param individual:
    @return:
    """
    num_selected = sum(individual)  # 计算被选择的特征数量
    if num_selected < 1 or num_selected > 5:  # 如果特征数量不在1到5之间
        return -float("inf"),  # 设置适应度为负无穷大

    # 根据individual矩阵，来计算是否出现server的概率
    probabilities = []
    product_dict = dict()

    for line_data in load_array:
        if line_data[0] not in product_dict.keys():
            product_dict[line_data[0]] = len(product_dict)

            new_row = []
            new_row.append(line_data[0])
            hasServer = False
            for i in range(1, len(line_data)):
                if individual[i - 1]:
                    hasServer = hasServer or line_data[i]['hasServer']

            dict_temp = {}
            if hasServer:
                dict_temp.update({"hasServer": 1, "sum": 1})
            else:
                dict_temp.update({"hasServer": 0, "sum": 1})

            new_row.append(dict_temp)
            probabilities.append(new_row)

        else:
            hasServer = False
            for i in range(1, len(line_data)):
                if individual[i - 1]:
                    hasServer = hasServer or line_data[i]['hasServer']

            if hasServer:
                probabilities[product_dict[line_data[0]]][1]['hasServer'] += 1
                probabilities[product_dict[line_data[0]]][1]['sum'] += 1
            else:
                probabilities[product_dict[line_data[0]]][1]['sum'] += 1

    total_probability = 1
    for _ in probabilities:
        _pro = _[1]['hasServer'] / _[1]['sum'] * 100
        # 这里有可能出现零概率
        if _pro == 0:
            _pro = 1
        total_probability = total_probability * _pro

    return total_probability,


# 读取处理过的数据
with open('./process_pip/select_probe_temp/array_3d.pkl', "rb") as file:
    load_array = pickle.load(file)

# 探测请求的特征概率
probabilities = []

# 你的问题参数
# num_containers = 30  # web容器数量
num_probes = 296  # 探测载荷数量

# 创建一个名为FitnessMax的适应度类，继承自deap库的base.Fitness类，weights参数表示我们是在做最大化问题
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# 创建一个名为Individual的个体类，继承自list类，设置其fitness属性为前面定义的FitnessMax类
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator: define how each attribute (probe selection) is generated
toolbox.register("attr_bool", random.randint, 0, 1)


def init_individual(ind_class):
    individual = [0] * num_probes
    selected_probes = random.sample(range(num_probes), random.randint(1, 5))
    for i in selected_probes:
        individual[i] = 1
    return ind_class(individual)


toolbox.register("individual", init_individual, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operator registration: define the genetic operators to be used
toolbox.register("evaluate", evaluation_function)  # 评估每个个体的适应度
toolbox.register("mate", tools.cxTwoPoint)  # 交叉操作
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)  # 变异操作，indpb是每个属性变异的概率
toolbox.register("select", tools.selTournament, tournsize=3)  # 选择操作，tournsize是每次比赛的参赛者数量

# 设置遗传算法的参数
population_size = 200
num_generations = 50
crossover_probability = 0.8
mutation_probability = 0.2

# 创建初始种群
pop = toolbox.population(n=population_size)

# 进行遗传算法的迭代
for gen in range(num_generations):

    print("正在迭代第 " + str(gen+1) + " 轮")

    # 选择下一代的个体
    offspring = toolbox.select(pop, len(pop))

    # 克隆选中的个体，防止后续操作影响原来的个体
    offspring = list(map(toolbox.clone, offspring))

    # 应用交叉操作
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < crossover_probability:
            toolbox.mate(child1, child2)

    # 应用变异操作
    for mutant in offspring:
        if random.random() < mutation_probability:
            toolbox.mutate(mutant)

    # 评估新一代的个体
    fitnesses = map(toolbox.evaluate, offspring)
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    # 新一代个体替代旧的种群
    pop[:] = offspring

# 导入需要的库
import matplotlib.pyplot as plt

# 在遗传算法结束后
best_individual = tools.selBest(pop, 1)[0]  # 选择最优个体

# 输出最优个体的特征选择和对应的适应度
print("Best individual is: %s\nwith fitness: %s" % (best_individual, best_individual.fitness))
for i in range(len(best_individual)):
    if best_individual[i] == 1:
        print(i + 1)

# 创建一个图像展示最优个体的特征选择
plt.figure(figsize=(10, 5))
plt.bar(range(len(best_individual)), best_individual)
plt.xlabel('Feature Index')
plt.ylabel('Selected or Not')
plt.title('Best Individual')
plt.show()


