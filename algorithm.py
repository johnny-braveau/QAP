#! /usr/bin/env python3

"""
This module defines the Basis class for classes
containing one solution algorithm.
"""
import sys
import time


class Algorithm(object):
    """
    Basis class for classes containing one solution algorithm.
    
    >>> algorithm = Algorithm()
    >>> print(algorithm)
    name: Algorithm
    time: None
    ov: None
    solution: None
    
    >>> algorithm = Algorithm()
    >>> print(algorithm.name)
    Algorithm

    >>> algorithm = Algorithm()
    >>> print(algorithm.time)
    None

    >>> algorithm = Algorithm()
    >>> print(algorithm.ov)
    None

    >>> algorithm = Algorithm()
    >>> print(algorithm.solution)
    None

    >>> from functionalities import Instance2D
    >>> instance = QAP("")
    >>> algorithm = Algorithm()
    >>> algorithm.solve(instance)
    Traceback (most recent call last):
      ...
    NotImplementedError
    """

    def __init__(self):
        """
        intitalize algorithm

        >>> algorithm = Algorithm()
        >>> print(algorithm)
        name: Algorithm
        time: None
        ov: None
        solution: None
        """

        self.__time = None
        self._ov = None
        self._solution = None
        self._best_known = None

    def __str__(self):
        """
        Returns the object information as a string.

        >>> algorithm = Algorithm()
        >>> print(algorithm)
        name: Algorithm
        time: None
        ov: None
        solution: None
        """
        s = ""
        s += "name: " + self.name + '\n'
        s += "time: " + str(self.time) + '\n'
        s += "ov: " + str(self.ov) + '\n'
        s += "solution: " + str(self.solution) + '\n'
        s += "best known ov " + str(self._best_known)
        return s

    @property
    def ov(self):
        """
        Getter to the variable ov (objective value).

        >>> algorithm = Algorithm()
        >>> print(algorithm.ov)
        None
        """
        return self._ov

    @ov.setter
    def ov(self, value):
        """
        Setter to the variable ov (objective value). Calling this getter causes an error.
        
        >>> algorithm = Algorithm()
        >>> algorithm.ov = 0
        Traceback (most recent call last):
          ...
        AssertionError: Not allowed to write to the private variable Algorithm.ov!
        """
        raise AssertionError("Not allowed to write to the private variable Algorithm.ov!")

    @property
    def solution(self):
        """
        Getter to the variable solution (list of the solution substructures (paths and cycles)).
        
        >>> algorithm = Algorithm()
        >>> print(algorithm.solution)
        None
        """

        return self._solution

    @solution.setter
    def solution(self, value):
        """
        Setter to the variable solution (list of the solution substructures (paths and cycles)). Calling this getter causes an error.

        >>> algorithm = Algorithm()
        >>> algorithm.solution = [[]]
        Traceback (most recent call last):
          ...
        AssertionError: Not allowed to write to the private variable Algorithm.solution!
        """
        raise AssertionError("Not allowed to write to the private variable Algorithm.solution!")

    @property
    def time(self):
        """
        Getter to the variable time (computation time).

        >>> algorithm = Algorithm()
        >>> print(algorithm.time)
        None
        """
        return self.__time

    @time.setter
    def time(self, value):
        """
        Setter to the variable time (computation time). Calling this getter causes an error.
        
        >>> algorithm = Algorithm()
        >>> algorithm.time = 0
        Traceback (most recent call last):
          ...
        AssertionError: Not allowed to write to the private variable Algorithm.time!
        """
        raise AssertionError("Not allowed to write to the private variable Algorithm.time!")

    @property
    def name(self):
        """
        Getter to the variable name (name of the class).
        
        >>> algorithm = Algorithm()
        >>> print(algorithm.name)
        Algorithm
        """
        return self.__class__.__name__

    @name.setter
    def name(self, value):
        """
        Setter to the variable name (name of the class). Calling this getter causes an error.
        
        >>> algorithm = Algorithm()
        >>> algorithm.name = ""
        Traceback (most recent call last):
          ...
        AssertionError: Not allowed to write to the private variable Algorithm.name!
        """
        raise AssertionError("Not allowed to write to the private variable Algorithm.name!")

    def algorithm(self, instance, model, cutoff, progress):
        """
        Solution algorithm. This method has to be implemented in
        all inherited classes and it has to set the variables
        __ov, __ov_list and __solution.
        Calling this method causes an error.

        Arguments:
        instance -- instance of QAP
        model -- linearization model used
        cutoff -- rounding border
        progress -- boolean value whether the pulp progress is shown
        """
        raise NotImplementedError

    def solve(self, instance, model, cutoff = 1.0, progress = False):
        """
        User interface method which has to be called if the
        solution should be computed. The method automatically
        measures the computational time required
        by the method algorithm.
        
        Arguments:
        instance -- instance of the QAP Lib
        instance -- instance of QAP
        model -- linearization model used
        cutoff -- rounding border
        progress -- boolean value whether the pulp progress is shown
        """
        start_time = time.time()
        self.algorithm(instance, model, cutoff, progress)
        end_time = time.time()
        assert instance.is_solution(self.solution)
        self._best_known = instance.get_solution()
        self.__time = end_time - start_time


def main():
    """
    The main program for test purposes only.

    >>> main()
    0
    """
    return 0

if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
    
    sys.exit(main())
