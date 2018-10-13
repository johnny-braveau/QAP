#! /usr/bin/env python3

"""
This module defines the Basis class for classes
containing one solution algorithm.
"""
import pulp

class Model(object):
    """
    """
    def __init__(self, n, d, i, r=False, a=[]):
        """
        n = instance size
        d = distance matrix
        i = intensity matrix
        r = relax variables
        a = fixed edges
        """
        self._n = n
        self._d = d
        self._i = i
        self._r = r
        self._a = a

    """

    Standard Linearizations including constraints for already fixed edges
    """
    def adam_johnson(self):
        """
        """
        qap = pulp.LpProblem('QAP', pulp.LpMinimize)
        if self._r:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                     range(self._n)),
                                         cat=pulp.LpContinuous, lowBound=0)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpBinary, lowBound=0)

        y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                             range(self._n), range(self._n), range(self._n)),
        cat=pulp.LpContinuous, lowBound=0)

        c_ijkl = [[[[0 for i in range(self._n)] for j in range(self._n)] for k in range(self._n)] for l in range(self._n)]

        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        c_ijkl[i][j][k][l] = float(self._d[i][k]) * float(self._i[j][l])

        qap += (pulp.lpSum(y_ijkl[i][j][k][l] * c_ijkl[i][j][k][l]
                    for i in range(self._n) for j in range(self._n) 
                    for k in range(self._n) for l in range(self._n) if j != l and i != k),
        'objective function')

        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][k] for k in range(self._n)) == 1,
                    'row: {}'.format(i))
                
        for k in range(self._n):
            qap += (pulp.lpSum(x_ij[i][k] for i in range(self._n)) == 1,
                    'column: {}'.format(k))

        for j in range(self._n):
            for k in range(self._n):
                for l in range(self._n):
                    if j != l:
                        qap += (pulp.lpSum(y_ijkl[i][j][k][l] for i in range(self._n) if i != k)  == x_ij[k][l],
                                    'lin 1 {} {} {}'.format(j, k, l))

        for i in range(self._n):
            for k in range(self._n):
                for l in range(self._n):
                    if i != k:
                        qap += (pulp.lpSum(y_ijkl[i][j][k][l] for j in range(self._n) if j != l)  == x_ij[k][l],
                                    'lin 2 {} {} {}'.format(i, k, l))

        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        if i < k and j != l:
                            qap += (y_ijkl[i][j][k][l] == y_ijkl[k][l][i][j],
                                        'lin 3 {} {} {} {}'.format(i, j, k, l))

        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap

    def aimms(self):
        """
        """
        if self._r:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                range(self._n)),
            cat=pulp.LpContinuous, lowBound=0, upBound=1)
            y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                    range(self._n), range(self._n), range(self._n)),
            cat=pulp.LpContinuous, lowBound=0, upBound=1)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpBinary, lowBound=0, upBound=1)
            y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                    range(self._n), range(self._n), range(self._n)),
            cat=pulp.LpBinary, lowBound=0, upBound=1)

        qap = pulp.LpProblem('QAP', pulp.LpMinimize)

        qap += (pulp.lpSum(y_ijkl[i][j][k][l] * float(self._d[i][j]) * float(self._i[k][l])
                for i in range(self._n) for j in range(self._n) if i != j
                for k in range(self._n) for l in range(self._n) if k != l),
            'objective function')


        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for j in range(self._n)) == 1,
                    'row {}'.format(i))
            

        for j in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for i in range(self._n)) == 1,
                    'column {}'.format(j))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        if (i != j and l != k):
                            qap += (y_ijkl[i][j][k][l] <= x_ij[i][k],
                            'lin {} {} {} {}'.format(i, j, k, l))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        if (i != j and l != k):
                            qap += (y_ijkl[i][j][k][l] >= x_ij[i][k] + x_ij[j][l] - 1,
                                        'lin 2 {} {} {} {}'.format(i, j, k, l))

        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap

    def fireze_yadegar(self):
        """
        """
        if self._r:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                             range(self._n)),
            cat=pulp.LpContinuous, lowBound=0)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                range(self._n)),
            cat=pulp.LpBinary, lowBound=0)
        
        y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                range(self._n), range(self._n), range(self._n)),
        cat=pulp.LpContinuous, lowBound=0, upBound=1)

        qap = pulp.LpProblem('QAP', pulp.LpMinimize)

        qap += (pulp.lpSum(y_ijkl[i][j][k][l] * float(self._d[i][j]) * float(self._i[k][l])
                   for i in range(self._n) for j in range(self._n) if i != j
                   for k in range(self._n) for l in range(self._n) if k != l),
            'objective function')
    
        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for j in range(self._n)) == 1,
                 'row {}'.format(i))
        

        for j in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for i in range(self._n)) == 1,
                 'column: {}'.format(j))


        for j in range(self._n):
            for k in range(self._n):
                for l in range(self._n):
                    qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for i in range(self._n))) == x_ij[j][l],
                    'lin 1 {} {} {}'.format(j, k, l))


        for i in range(self._n):
            for k in range(self._n):
                for l in range(self._n):
                    qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for j in range(self._n))) == x_ij[i][k],
                    'lin 2 {} {} {}'.format(i, k, l))


        for i in range(self._n):
            for j in range(self._n):
                for l in range(self._n):
                    qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for k in range(self._n))) == x_ij[j][l],
                    'lin 3 {} {} {}'.format(i, j, l))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for l in range(self._n))) == x_ij[i][k],
                    'lin 4 {} {} {}'.format(i, j, k))



        for i in range(self._n):
            for k in range(self._n):
                qap += (y_ijkl[i][i][k][k] == x_ij[i][k],
                'lin 5 {} {}'.format(i, k))

        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap
    
    def kaufman_broeckx(self):
        """
        """

        if self._r:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                range(self._n)),
            cat=pulp.LpContinuous, lowBound=0)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpBinary, lowBound=0, upBound=1)
        
        y_ik = pulp.LpVariable.dicts('y_%s_%s', (range(self._n),
                                                range(self._n)),
        cat=pulp.LpContinuous, lowBound=0)

        d_ik = [[0 for i in range(self._n)] for k in range(self._n)] 

        for i in range(self._n):
            for k in range(self._n):
                d_ik[i][k] = (pulp.lpSum(
                    float(self._d[i][j]) * float(self._i[k][l])
                    for j in range(self._n)
                    for l in range(self._n)))



        qap = pulp.LpProblem('QAP', pulp.LpMinimize)


        qap += (pulp.lpSum(y_ik[i][k]
                   for i in range(self._n) for k in range(self._n)),
                'objective function')
    

        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][k] for k in range(self._n)) == 1,
                 'row: {}'.format(i))
        

        for k in range(self._n):
            qap += (pulp.lpSum(x_ij[i][k] for i in range(self._n)) == 1,
                 'column: {}'.format(k))


        for i in range(self._n):
            for k in range(self._n):
                    qap += ((d_ik[i][k] * x_ij[i][k]) + pulp.lpSum(float(self._d[i][j]) * float(self._i[k][l]) * x_ij[j][l]
                                for j in range(self._n)
                                for l in range(self._n)) - y_ik[i][k] <= d_ik[i][k],
                                'dik_constant {} {}'.format(i, k))

        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap

    def lawler(self):
        """
        Solve QAP ILP linearized with Lawler (1963)
        """

        if self._r: 
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpContinuous, lowBound=0)
            
            y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                    range(self._n), range(self._n), range(self._n)),
            cat=pulp.LpContinuous)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpBinary, lowBound=0)
            
            y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                    range(self._n), range(self._n), range(self._n)),
            cat=pulp.LpBinary)

        c_ijkl = [[[[0 for i in range(self._n)] for j in range(self._n)] for k in range(self._n)] for l in range(self._n)]

        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        c_ijkl[i][j][k][l] = float(self._d[i][j]) * float(self._i[k][l])



        qap = pulp.LpProblem('QAP', pulp.LpMinimize)

        qap += (pulp.lpSum(y_ijkl[i][j][k][l] * float(c_ijkl[i][j][k][l])
                    for i in range(self._n) for j in range(self._n)
                    for k in range(self._n) for l in range(self._n)),
        'objective function')
    
        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for j in range(self._n)) == 1,
                    'row: {}'.format(i))
            
        for j in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for i in range(self._n)) == 1,
                    'column: {}'.format(j))

        qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for i in range(self._n) for j in range(self._n)
                                    for k in range(self._n) for l in range(self._n) ))
                                    == ((self._n)**2), 'lin 1')
        
        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        qap += (x_ij[i][k] + x_ij[j][l] - 2 * y_ijkl[i][j][k][l] >= 0,
                        'lin 2 {} {} {} {}'.format(i, j, k, l))

        
        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap

    def padberg(self):
        """
        
        """
        if self._r:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                range(self._n)),
            cat=pulp.LpContinuous, lowBound=0)
        else:
            x_ij = pulp.LpVariable.dicts('x_%s_%s', (range(self._n),
                                                    range(self._n)),
            cat=pulp.LpBinary, lowBound=0)
        
        y_ijkl = pulp.LpVariable.dicts('y_%s_%s_%s_%s', (range(self._n),
                                                range(self._n), range(self._n), range(self._n)),
        cat=pulp.LpContinuous, lowBound=0)

        q_ijkl = [[[[0 for i in range(self._n)] for j in range(self._n)] for k in range(self._n)] for l in range(self._n)] 

        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    for l in range(self._n):
                        q_ijkl[i][j][k][l] = float(self._d[i][j]) * float(self._i[k][l]) + float(self._d[j][i]) * float(self._i[l][k])

        qap = pulp.LpProblem('QAP', pulp.LpMinimize)

        qap += (pulp.lpSum(y_ijkl[i][j][k][l] * q_ijkl[i][j][k][l]
                        for i in range(self._n) for j in range(self._n) if i < j
                        for k in range(self._n) for l in range(self._n) if k != l),
                        'objective function')
    
        for i in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for j in range(self._n)) == 1,
                    'row: {}'.format(i))
            

        for j in range(self._n):
            qap += (pulp.lpSum(x_ij[i][j] for i in range(self._n)) == 1,
                    'column: {}'.format(j))


        for j in range(self._n):
            for k in range(self._n):
                for l in range(self._n):
                    n = self._n - 1
                    if (k != l and j <= n - 1) or (l < k and j == n):
                        qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for i in range(j))) +
                                (pulp.lpSum(y_ijkl[j][i][l][k] for i in range(j+1, self._n))) == x_ij[j][l],
                        'lin 1 {} {} {}'.format(j, k, l))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    n = self._n - 1
                    if ((i <= n - 3 and i < j and j <=  n - 1) 
                        or (k <= n - 1 and i == n - 2 and j == n - 1)):
                        qap += ((pulp.lpSum(y_ijkl[i][j][k][l] for l in range(k))) +
                                (pulp.lpSum(y_ijkl[i][j][k][l] for l in range(k+1, self._n))) == x_ij[i][k],
                        'lin 2 {} {} {}'.format(j, k, i))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n):
                    n = self._n - 1
                    if (k <= n - 1 and i <= n - 3 and i < j and j <= n - 1):
                        qap += ((pulp.lpSum(y_ijkl[i][j][l][k] for l in range(k))) +
                                (pulp.lpSum(y_ijkl[i][j][l][k] for l in range(k + 1, self._n))) == x_ij[j][k],
                        'lin 3 {} {} {}'.format(j, k, i))


        for i in range(self._n):
            for j in range(self._n):
                for k in range(self._n): 
                    for l in range(self._n):
                        n = self._n - 1
                        if(i < j and j <= n and k != l):
                            qap += y_ijkl[i][j][k][l] >= 0


        if len(self._a) > 0:
            self.__set_ones(qap, x_ij)

        return qap
    

    """
    Additional constraints for already placed pairs
    """
    def __set_ones(self, qap, x_ij):
        """
        set already chosen xij to 1
        """
        for element in self._a:
            qap += (x_ij[int(element[0])][int(element[1])] == 1,
                    'additional ones {} {}'.format(int(element[0]), int(element[1])))