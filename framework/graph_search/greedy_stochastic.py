from .graph_problem_interface import *
from .best_first_search import BestFirstSearch
from typing import Optional
from experiments.temperature import probabilities_vector
import numpy as np


class GreedyStochastic(BestFirstSearch):
    def __init__(self, heuristic_function_type: HeuristicFunctionType,
                 T_init: float = 1.0, N: int = 5, T_scale_factor: float = 0.95):
        # GreedyStochastic is a graph search algorithm. Hence, we use close set.
        super(GreedyStochastic, self).__init__(use_close=True)
        self.heuristic_function_type = heuristic_function_type
        self.T = T_init
        self.N = N
        self.T_scale_factor = T_scale_factor
        self.solver_name = 'GreedyStochastic (h={heuristic_name})'.format(
            heuristic_name=heuristic_function_type.heuristic_name)

    def _init_solver(self, problem: GraphProblem):
        super(GreedyStochastic, self)._init_solver(problem)
        self.heuristic_function = self.heuristic_function_type(problem)

    def _open_successor_node(self, problem: GraphProblem, successor_node: SearchNode):
        """
        TODO: implement this method! Done!
        """
        if self.open.has_state(successor_node.state):
            already_found_node_with_same_state = self.open.get_node_by_state(successor_node.state)
            if already_found_node_with_same_state.cost > successor_node.cost:
                self.open.extract_node(already_found_node_with_same_state)
                self.open.push_node(successor_node)

        elif self.close.has_state(successor_node.state):
            already_found_node_with_same_state = self.close.get_node_by_state(successor_node.state)
            if already_found_node_with_same_state.cost > successor_node.cost:
                self.close.remove_node(already_found_node_with_same_state)
                self.open.push_node(successor_node)

        else:
            self.open.push_node(successor_node)

    def _calc_node_expanding_priority(self, search_node: SearchNode) -> float:
        """
        TODO: implement this method! Done!
        Remember: `GreedyStochastic` is greedy.
        """
        # meaning: return only heuristic value.
        h = self.heuristic_function.estimate(search_node.state)
        return h

    def _extract_next_search_node_to_expand(self) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         using the stochastic method to choose out of the N
         best items from open.
        TODO: implement this method! Done!
        Use `np.random.choice(...)` whenever you need to randomly choose
         an item from an array of items given a probabilities array `p`.
        You can read the documentation of `np.random.choice(...)` and
         see usage examples by searching it in Google.
        Notice: You might want to pop min(N, len(open) items from the
                `open` priority queue, and then choose an item out
                of these popped items. The other items have to be
                pushed again into that queue.
        """
        node_to_expand = None

        if self.open.is_empty():
            return node_to_expand

        effective_N = min(self.N, len(self.open))
        best_N_nodes = [self.open.pop_next_node() for _ in range(effective_N)]
        X = [node.expanding_priority for node in best_N_nodes]
        T = [self.T]

        self.T *= self.T_scale_factor

        if len(X) == 1:
            node_to_expand = best_N_nodes[0]
        else: # there is more than one node to choose from.
            if best_N_nodes[0].expanding_priority == 0:
                node_to_expand = best_N_nodes[0] # this patch is for solve zero divide RunTimeError.
            else:
                p_vector = probabilities_vector(X, T)
                index = np.random.choice(range(effective_N), p=[p_vector[node.expanding_priority][0] for node in best_N_nodes])
                node_to_expand = best_N_nodes.pop(index)
            for node in best_N_nodes:
                self.open.push_node(node)
        self.close.add_node(node_to_expand)

        return node_to_expand
