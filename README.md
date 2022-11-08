### Water Flow Optimizer

##### Reference: Luo K. Water flow optimizer: a nature-inspired evolutionary algorithm for global optimization[J]. IEEE Transactions on Cybernetics, 2021.

| Variables         | Meaning                                                  |
| ----------------- | -------------------------------------------------------- |
| pop               | The number of water particles                            |
| iter              | The number of iterations                                 |
| pl                | The laminar probability                                  |
| pe                | The eddying probability                                  |
| dim               | The number of dimensions                                 |
| score             | List, the score of the i-th particle is score[i]         |
| position          | List, the position of the i-th particle is position[i]   |
| best_score        | The global best score                                    |
| best_location     | The position of the global best particle                 |
| possible_position | List, the possible movements of water particles          |
| possible_score    | List, the score of possible movements                    |
| iter_best         | List, the best-so-far score of each iteration            |
| con_iter          | The last iteration number when the best_score is updated |

#### Test problem: Pressure vessel design
![](https://github.com/Xavier-MaYiMing/Water-Flow-Optimizer/blob/main/Pressure%20vessel%20design.png)

$$
\begin{align}
&\text{min}\ f(x)=0.6224x_1x_3x_4+1.7781x_2x_3^2+3.1661x_1^2x_4+19.84x_1^2x_3,\\
&\text{s.t.} \\
&-x_1+0.0193x_3\leq0,\\
&-x_3+0.0095x_3\leq0,\\
&-\pi x_3^2x_4-\frac{4}{3}\pi x_3^3+1296000\leq0,\\
&x_4-240\leq0,\\
&0\leq x_1\leq99,\\
&0\leq x_2 \leq99,\\
&10\leq x_3 \leq 200,\\
&10\leq x_4 \leq 200.
\end{align}
$$


#### Example

```python
if __name__ == '__main__':
    # Parameter settings
    pop = 50
    iter = 3000
    pl = 0.3
    pe = 0.7
    lbound = [0, 0, 10, 10]
    ubound = [99, 99, 200, 200]
    print(main(pop, iter, pl, pe, lbound, ubound))
```

##### Output:

![](https://github.com/Xavier-MaYiMing/Water-Flow-Optimizer/blob/main/convergence%20curve.png)

![](https://github.com/Xavier-MaYiMing/Water-Flow-Optimizer/blob/main/enlarged%20view.png)



The upper figure is the convergence curve, and the lower figure is the enlarged view.  The WFO converges at its 1250-th iteration.

```python
{
    'best solution': [1.3005502034963052, 0.6428626394484327, 67.3860209065443, 10.000000000000005], 
    'best score': 8050.913534658795, 
    'convergence iteration': 1250
}

```

