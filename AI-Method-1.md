# Expectimax and Heuristics
## Governing Strategy Tree  

### Application  
Uses expectimax agents for offensive. Calculates each states utility values based on expectations and returns the max value of it, not particularly smart. Implemented together with an evaluation function to further refine the characteristics of pacman. 

### Trade-offs  

#### *Advantages*  
- Better than minimax for competitions against other people, especially for those that don't perform as well as the top staff teams, as they'll inevitably make some sub-optimal decisions that expectimax can take advantage of
- With a good features and weights function it works quite well in terms of an agent's behaviour. 

#### *Disadvantages*
- Requires completely manual tuning based on results and observations made from previous performance
- Expensive computations as there can't be any pruning done to the trees, needs to be carefully managed to avoid going over the turn time limit
- Using this technique is our agent was unable to sense the opponent's agents if they are behind walls.