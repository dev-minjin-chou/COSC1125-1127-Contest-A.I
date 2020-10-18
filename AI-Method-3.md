# Monte Carlo Technique (MCT)

## Governing Strategy Tree  

### Application
We are using monte carlo technique as our final approach. This technique works relatively well out of all the other approaches we have implemented. We are using the deepcopy function to further analyse the game state of our pacman while computing each possible actions and state of the successor nodes and calculates the probabilities based on each states. We have also created multiple action functions that calls in this montecarlo function to further evaluate and calculate the values of each state so that our pacman are better in predicting and evaluating which action to take. 
### Trade-offs  
-Trade-offs of this technique is even though it is smart and is able to sense opponent quite far away unlike our first expectimax approach, this technique is not effective at times as occasionally it will 'predict' the wrong actions of the opponent and brought itself the inevitable end. 
#### *Advantages*  
-Allows us to further predict/'oversee' the actions of the opponents team, hence is able to avoid some of the most costly paths.

#### *Disadvantages*
-Occasionally predicts the wrong movement/actions of opponents and took the wrong action, causes itself to die in the process due to bad prediction.