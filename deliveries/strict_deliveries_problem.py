from framework.graph_search import *
from framework.ways import *
from .map_problem import MapProblem
from .deliveries_problem_input import DeliveriesProblemInput
from .relaxed_deliveries_problem import RelaxedDeliveriesState, RelaxedDeliveriesProblem

from typing import Set, FrozenSet, Optional, Iterator, Tuple, Union


class StrictDeliveriesState(RelaxedDeliveriesState):
    """
    An instance of this class represents a state of the strict
     deliveries problem.
    This state is basically similar to the state of the relaxed
     problem. Hence, this class inherits from `RelaxedDeliveriesState`.

    TODO:
        If you believe you need to modify the state for the strict
         problem in some sense, please go ahead and do so.
    """
    def __init__(self, current_location: Junction,
                 dropped_so_far: Union[Set[Junction], FrozenSet[Junction]],
                 fuel: float):
        super(StrictDeliveriesState, self).__init__(current_location, dropped_so_far, fuel) # TODO


class StrictDeliveriesProblem(RelaxedDeliveriesProblem):
    """
    An instance of this class represents a strict deliveries problem.
    """

    name = 'StrictDeliveries'

    def __init__(self, problem_input: DeliveriesProblemInput, roads: Roads,
                 inner_problem_solver: GraphProblemSolver, use_cache: bool = True):
        super(StrictDeliveriesProblem, self).__init__(problem_input)
        self.initial_state = StrictDeliveriesState(
            problem_input.start_point, frozenset(), problem_input.gas_tank_init_fuel)
        self.inner_problem_solver = inner_problem_solver
        self.roads = roads
        self.use_cache = use_cache
        self._init_cache()

    def _init_cache(self):
        self._cache = {}
        self.nr_cache_hits = 0
        self.nr_cache_misses = 0

    def _insert_to_cache(self, key, val):
        if self.use_cache:
            self._cache[key] = val

    def _get_from_cache(self, key):
        if not self.use_cache:
            return None
        if key in self._cache:
            self.nr_cache_hits += 1
        else:
            self.nr_cache_misses += 1
        return self._cache.get(key)

    def expand_state_with_costs(self, state_to_expand: GraphProblemState) -> Iterator[Tuple[GraphProblemState, float]]:
        """
        TODO: implement this method!
        This method represents the `Succ: S -> P(S)` function of the strict deliveries problem.
        The `Succ` function is defined by the problem operators as shown in class.
        The relaxed problem operators are defined in the assignment instructions.
        It receives a state and iterates over the successor states.
        Notice that this is an *Iterator*. Hence it should be implemented using the `yield` keyword.
        For each successor, a pair of the successor state and the operator cost is yielded.
        """
        assert isinstance(state_to_expand, StrictDeliveriesState)
        curr_junction = state_to_expand.current_location
        possible_waiting_orders = self.drop_points - state_to_expand.dropped_so_far
        start_junction_id = curr_junction.index
        for succ_junction in self.possible_stop_points:
            target_junction_id = succ_junction.index
            key = (start_junction_id, target_junction_id)
            val = self._get_from_cache(key)
            if val is None: # not in cache.
                map_prob = MapProblem(self.roads, start_junction_id, target_junction_id)
                res = self.inner_problem_solver.solve_problem(map_prob)
                operator_cost = res.final_search_node.cost
                self._insert_to_cache(key, operator_cost)
            else:
                operator_cost = val
            remain_fuel = state_to_expand.fuel - operator_cost
            if remain_fuel < 0 or succ_junction in state_to_expand.dropped_so_far:
                continue
            if succ_junction in possible_waiting_orders:
                succ_state = StrictDeliveriesState(succ_junction,
                                                    state_to_expand.dropped_so_far | frozenset([succ_junction]),
                                                    remain_fuel)
            else:  # gas Station
                succ_state = StrictDeliveriesState(succ_junction, state_to_expand.dropped_so_far,
                                                    self.gas_tank_capacity)
            yield succ_state, operator_cost
        # raise NotImplemented()  # TODO: remove!

    def is_goal(self, state: GraphProblemState) -> bool:
        """
        This method receives a state and returns whether this state is a goal.
        TODO: implement this method!
        """
        assert isinstance(state, StrictDeliveriesState)
        return state.dropped_so_far == self.drop_points  # we dropped all the deliveries! yay!
        # raise NotImplemented()  # TODO: remove!
