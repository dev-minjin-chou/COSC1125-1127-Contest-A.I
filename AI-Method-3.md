# Monte Carlo Technique (MCT)

## Governing Strategy Tree  

### Application
We are using Monte Carlo Technique as our final approach. This technique works relatively well out of all the other approaches we have implemented. We are using the deepcopy function to further analyse the game state while computing each possible action and state of the successor nodes and calculate the probabilities based on each state. We have also created multiple action functions that calls in this Monte Carlo function to further evaluate and calculate the values of each state so that our Pacman agents are better in predicting and evaluating which action to take. 
### Trade-offs  
#### *Advantages*  
- Allows us to further predict/'oversee' the actions of the opponents team, hence is able to avoid some of the most costly paths.
- Able to sense opponent behind 'walls' and further distance away unlike the expectimax agents.
- Able to differentiate better actions to take in crucial times such as eating power capsules when ghost is nearby rather than picking up nearby foods.

#### *Disadvantages*
- Occasionally predicts the wrong movement/actions of opponents and takesthe wrong action, resulting in its death due to bad prediction.
- Occasionally gets confused at what actions its supposed to take hence moving back and forth in the process, wasting time and movements.