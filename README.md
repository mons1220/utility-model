# Utility-based preferential attachment model

Utility-based preferential attachment model is an evolving network model in which preference is based on utility within second degree of separation.

The utility of node $i$ at a specific time step $t$ is as follows. 
$$u_i^{[2]} (t)=k_i^{[1]} (t)(b_{1}-c)+k_i^{[2]} (t) b_{2}$$ 
$k_i^{[1]}$: Number of direct links  
$k_i^{[2]}$: Number of indirect links (second degree of separation)  
$b_{1}, b_{2}$: Benefit coefficient from nodes with direct / indirect connection  
$c$: Cost coefficient from nodes with direct connection  

For convenience, we use coef_k1 ($=b_{1}-c$), coef_k2 ($=b_{2}$)

## Instructions
Coded in Python3.

You can initialize Utility-based preferential attachment model by next code:
```python
from utility_model import UM

G = UM(m=1, coef_k1=1, coef_k2=0, seed=5)  # BA model
```
m (int): Number of edges added at each step  
coef_k1 (int): Utility coefficient for direct connection  
coef_k2 (int): Utility coefficient for indirect connection (only positive numbers are considered. Otherwise the target pool will almost disappear.)  
seed (int): Number of seed nodes (ring network)  

You can add new nodes by next code:
```python
G.add_nodes(N=100000)
```
N (int): Number of nodes added to the network  

See example.py for a detailed example.

## Reference
The model code is based on the work of Max Falkenberg.
https://github.com/MaxFalkenberg/k2model
