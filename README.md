# QAP

This is a simple python project so solve the quadatic assignment problem.
Different linearizations are implemented in lp_models.py.
Solve to optimality only possible with small instances.
Data is used from QAPlib: http://anjos.mgi.polymtl.ca/qaplib/

## example usage in python3
```
>>> from functionalities import *
>>> instance = QAP("qapdat/small/chr12a.dat")
>>> instance.instance_size()
>>> 12
>>> from optimum import Optimum
>>> alg = Optimum()
>>> alg.solve(instance)
>>> alg.solve(instance, 'kaufman_broeckx')
>>> alg.ov()
>>> alg.ov
>>> 9552.0
>>> alg.solution
>>> [[0.0, 6.0], [10.0, 7.0], [11.0, 3.0], [1.0, 4.0], [2.0, 11.0], [3.0, 1.0], [4.0, 0.0], [5.0, 2.0], [6.0, 8.0], [7.0, 10.0], [8.0, 9.0], [9.0, 5.0]]
```