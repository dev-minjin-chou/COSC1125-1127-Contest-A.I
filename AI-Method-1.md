# Expectimax and Heuristics
## Governing Strategy Tree  

### Application  

### Trade-offs  
The trade-offs in using this technique is our agent are unable to sense the opponent's agent if they are behind walls. However with a better evaluation function it works quite well in terms of agent's behaviour.

#### *Advantages*  
- Better than minimax for competitions against other people, especially for those that don't perform as well as the top staff teams, as they'll inevitably make some sub-optimal decisions that expectimax can take advantage of 

#### *Disadvantages*
- Requires completely manual tuning based on results and observations made from previous performance
- Expensive computations as there can't be any pruning done to the trees, needs to be carefully managed to avoid going over the turn time limit