import numpy as np
from matplotlib import pyplot as plt


X = np.array([400, 450, 900, 390, 550])
vector_range = 100
T_scale_factor = 1

# TODO: Write the code as explained in the instructions Done!
# raise NotImplemented()  # TODO: remove!


def probabilities_vector(X, T, T_scale_factor):

    x_pow_t_dic = {}
    x_pow_t_sum_dic = {}
    for x in X:
        for t in T:
            x_pow_t = np.power(np.divide(x, T_scale_factor), np.divide(-1, t))
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


def main():
    T = np.linspace(0.01, 5, vector_range)
    p_vectors = probabilities_vector(X, T, T_scale_factor)

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


if __name__ == '__main__':
    main()


