"""
module solving QAP to optimum without any relaxations but using linearized models
"""

from algorithm import Algorithm
from lp_models import Model
from functionalities import get_sorted_x_vars, place_units
import pulp

class Optimum(Algorithm):
    """
    solve QAP without relaxation to the optimum
    only for small problems
    """

    def __init__(self):
        """
        initialize optimum algorithm
        """
        super().__init__()

    def algorithm(self, instance, model, cutoff=1.0, progress=False):
        """
        solve QAP without relaxation to the optimum
        """

        m = Model(instance.instance_size(), instance.distance(), instance.intensity(), False, [])
        result = getattr(m, model)()
        result.solve()
        self._ov = result.objective.value()
        x_vars = get_sorted_x_vars(result)
        self._solution = place_units(x_vars, 1)
