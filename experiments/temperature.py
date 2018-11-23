import numpy as np
from matplotlib import pyplot as plt


X = np.array([400, 450, 900, 390, 550])
vector_range = 100

# TODO: Write the code as explained in the instructions
# raise NotImplemented()  # TODO: remove!


def probabilities_vector(X, T):

    x_pow_t_dic = {}
    x_pow_t_sum_dic = {}
    for x in X:
        for t in T:
            x_pow_t = np.power(x, np.divide(-1, t))
            x_pow_t_dic[(x, t)] = x_pow_t
            if t not in x_pow_t_sum_dic:
                x_pow_t_sum_dic[t] = x_pow_t
            else:
                x_pow_t_sum_dic[t] += x_pow_t

    vectors_dic = {}
    for x in X:
        probability_vector = []
        for t in T:
            probability_vector.append(np.divide(x_pow_t_dic[(x, t)], x_pow_t_sum_dic[t]))
        vectors_dic[x] = probability_vector
    return vectors_dic


T = np.linspace(0.01, 5, vector_range)
p_vectors = probabilities_vector(X, T)

for i, x in enumerate(X):
    P = p_vectors[x]
    plt.plot(T, P, label=str(x))

plt.xlabel("T")
plt.ylabel("P")
plt.title("Probability as a function of the temperature")
plt.legend()
plt.grid()
plt.show()
exit()
