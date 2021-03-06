from framework import *
from deliveries import *

from matplotlib import pyplot as plt
import numpy as np
from typing import List, Union

# Load the map
roads = load_map_from_csv(Consts.get_data_file_path("tlv.csv"))

# Make `np.random` behave deterministic.
Consts.set_seed()

# --------------------------------------------------------------------
# -------------------------- Map Problem -----------------------------
# --------------------------------------------------------------------

def plot_distance_and_expanded_wrt_weight_figure(
        weights: Union[np.ndarray, List[float]],
        total_distance: Union[np.ndarray, List[float]],
        total_expanded: Union[np.ndarray, List[int]]):
    """
    Use `matplotlib` to generate a figure of the distance & #expanded-nodes
     w.r.t. the weight.
    """
    assert len(weights) == len(total_distance) == len(total_expanded)

    fig, ax1 = plt.subplots()

    # TODO: Plot the total distances with ax1. Use `ax1.plot(...)`.
    # TODO: Make this curve colored blue with solid line style.
    # See documentation here:
    # https://matplotlib.org/2.0.0/api/_as_gen/matplotlib.axes.Axes.plot.html
    # You can also search google for additional examples.
    #raise NotImplemented()
    ax1.plot(weights, total_distance,'b-')

    # ax1: Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('distance traveled', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_xlabel('weight')

    # Create another axis for the #expanded curve.
    ax2 = ax1.twinx()

    # TODO: Plot the total expanded with ax2. Use `ax2.plot(...)`.
    # TODO: ax2: Make the y-axis label, ticks and tick labels match the line color.
    # TODO: Make this curve colored red with solid line style.
    #raise NotImplemented()
    ax2.plot(weights, total_expanded, 'r-')
    ax2.set_ylabel('states expanded', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.show()


def run_astar_for_weights_in_range(heuristic_type: HeuristicFunctionType, problem: GraphProblem):
    # TODO:
    # 1. Create an array of 20 numbers equally spreaded in [0.5, 1]
    #    (including the edges). You can use `np.linspace()` for that.
    # 2. For each weight in that array run the A* algorithm, with the
    #    given `heuristic_type` over the map problem. For each such run,
    #    store the cost of the solution (res.final_search_node.cost)
    #    and the number of expanded states (res.nr_expanded_states).
    #    Store these in 2 lists (array for the costs and array for
    #    the #expanded.
    # Call the function `plot_distance_and_expanded_by_weight_figure()`
    #  with that data.
    #raise NotImplemented()  # TODO: remove!

    list_of_range = np.linspace(0.5, 1, 20)
    list_of_costs = []
    list_of_expanded = []
    for weight in list_of_range:
        astar = AStar(heuristic_type, weight)
        res = astar.solve_problem(problem)
        list_of_costs.append(res.final_search_node.cost)
        list_of_expanded.append(res.nr_expanded_states)

    plot_distance_and_expanded_wrt_weight_figure(list_of_range, list_of_costs, list_of_expanded)


def plot_costs_compare_graph(greedy_stochastic_costs, anytime_greedy_stochastic_costs, astar_costs, greedy_deterministic_costs):
    iterations = range(len(greedy_stochastic_costs))

    plt.plot(iterations, greedy_stochastic_costs, label="Greedy stochastic")
    plt.plot(iterations, anytime_greedy_stochastic_costs, label="Anytime greedy stochastic")
    plt.plot(iterations, astar_costs, label="astar")
    plt.plot(iterations, greedy_deterministic_costs, label="Greedy deterministic")

    plt.xlabel("Iteration")
    plt.ylabel("costs")
    plt.title("cost as a function of the iteration")
    plt.legend()
    plt.grid()
    plt.show()


def map_problem():
    print()
    print('Solve the map problem.')

    # Ex.8
    map_prob = MapProblem(roads, 54, 549)
    uc = UniformCost()
    res = uc.solve_problem(map_prob)
    print(res)

    # Ex.10
    # TODO: create an instance of `AStar` with the `NullHeuristic`, done!
    #       solve the same `map_prob` with it and print the results (as before).
    # Notice: AStar constructor receives the heuristic *type* (ex: `MyHeuristicClass`),
    #         and not an instance of the heuristic (eg: not `MyHeuristicClass()`).
    astar = AStar(NullHeuristic)
    res = astar.solve_problem(map_prob)
    print(res)

    # Ex.11
    # TODO: create an instance of `AStar` with the `AirDistHeuristic`, done!
    #       solve the same `map_prob` with it and print the results (as before).
    astar = AStar(AirDistHeuristic)
    res = astar.solve_problem(map_prob)
    print(res)

    # Ex.12
    # TODO: Done!
    # 1. Complete the implementation of the function
    #    `run_astar_for_weights_in_range()` (upper in this file).
    # 2. Complete the implementation of the function
    #    `plot_distance_and_expanded_by_weight_figure()`
    #    (upper in this file).
    # 3. Call here the function `run_astar_for_weights_in_range()`
    #     #    with `AirDistHeuristic` and `map_prob`.
    run_astar_for_weights_in_range(AirDistHeuristic, map_prob)


# --------------------------------------------------------------------
# ----------------------- Deliveries Problem -------------------------
# --------------------------------------------------------------------

def relaxed_deliveries_problem():

    print()
    print('Solve the relaxed deliveries problem.')

    big_delivery = DeliveriesProblemInput.load_from_file('big_delivery.in', roads)
    big_deliveries_prob = RelaxedDeliveriesProblem(big_delivery)

    # Ex.16
    # TODO: create an instance of `AStar` with the `MaxAirDistHeuristic`, done!
    #       solve the `big_deliveries_prob` with it and print the results (as before).

    astar = AStar(MaxAirDistHeuristic)
    res = astar.solve_problem(big_deliveries_prob)
    print(res)

    # Ex.17
    # TODO: create an instance of `AStar` with the `MSTAirDistHeuristic`, done!
    #       solve the `big_deliveries_prob` with it and print the results (as before).

    astar = AStar(MSTAirDistHeuristic)
    res = astar.solve_problem(big_deliveries_prob)
    print(res)

    # Ex.18
    # TODO: Call here the function `run_astar_for_weights_in_range()` done!
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.
    run_astar_for_weights_in_range(MSTAirDistHeuristic, big_deliveries_prob)

    # Ex.24
    # TODO:
    # 1. Run the stochastic greedy algorithm for 100 times.
    #    For each run, store the cost of the found solution.
    #    Store these costs in a list.

    k = 100
    greedy_stochastic_costs = []
    for _ in range(k):
        greedy_stochastic = GreedyStochastic(MSTAirDistHeuristic)
        res = greedy_stochastic.solve_problem(big_deliveries_prob)
        greedy_stochastic_costs.append(res.final_search_node.cost)

    # 2. The "Anytime Greedy Stochastic Algorithm" runs the greedy
    #    greedy stochastic for N times, and after each iteration
    #    stores the best solution found so far. It means that after
    #    iteration #i, the cost of the solution found by the anytime
    #    algorithm is the MINIMUM among the costs of the solutions
    #    found in iterations {1,...,i}. Calculate the costs of the
    #    anytime algorithm wrt the #iteration and store them in a list.

    anytime_greedy_stochastic_costs = [min(greedy_stochastic_costs[:index]) for index in range(1, k+1)]

    # 3. Calculate and store the cost of the solution received by
    #    the A* algorithm (with w=0.5).

    astar = AStar(MSTAirDistHeuristic, heuristic_weight=0.5)
    res = astar.solve_problem(big_deliveries_prob)
    astar_cost = res.final_search_node.cost

    # 4. Calculate and store the cost of the solution received by
    #    the deterministic greedy algorithm (A* with w=1).

    greedy_deterministic = AStar(MSTAirDistHeuristic, heuristic_weight=1)
    res = greedy_deterministic.solve_problem(big_deliveries_prob)
    greedy_deterministic_cost = res.final_search_node.cost

    # 5. Plot a figure with the costs (y-axis) wrt the #iteration
    #    (x-axis). Of course that the costs of A*, and deterministic
    #    greedy are not dependent with the iteration number, so
    #    these two should be represented by horizontal lines.
    plot_costs_compare_graph(greedy_stochastic_costs, anytime_greedy_stochastic_costs, [astar_cost]*k, [greedy_deterministic_cost]*k)


def strict_deliveries_problem():
    print()
    print('Solve the strict deliveries problem.')

    small_delivery = DeliveriesProblemInput.load_from_file('small_delivery.in', roads)
    small_deliveries_strict_problem = StrictDeliveriesProblem(
        small_delivery, roads, inner_problem_solver=AStar(AirDistHeuristic))

    # Ex.26
    # TODO: Call here the function `run_astar_for_weights_in_range()`
    #       with `MSTAirDistHeuristic` and `big_deliveries_prob`.
    run_astar_for_weights_in_range(MSTAirDistHeuristic, small_deliveries_strict_problem)

    # Ex.28
    # TODO: create an instance of `AStar` with the `RelaxedDeliveriesHeuristic`,
    #       solve the `small_deliveries_strict_problem` with it and print the results (as before).
    astar = AStar(RelaxedDeliveriesHeuristic)
    res = astar.solve_problem(small_deliveries_strict_problem)
    print(res)

def main():
    map_problem()
    relaxed_deliveries_problem()
    strict_deliveries_problem()


if __name__ == '__main__':
    main()
