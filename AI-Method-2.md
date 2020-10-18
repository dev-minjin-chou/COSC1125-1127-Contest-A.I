# Q-learning

## Governing Strategy Tree 

### Application  
Attempted to use this technique as the base agent instead of reflexCaptureAgent, but ultimately was never used in a competition. Took advantage of the computeQValuesAction to further evaluate a better legal action based on Q-values. Improved chooseAction function by implementing calculations of q-values. 

### Trade-offs 

#### *Advantages*  
- Doesn't require as much manual tuning as other methods, as the policies are formed from experience
- An advantage of approximate Q-learning in particular, is that while Q-learning learns the value of unique states through many iterations and experiences of being in that unique state, approximate Q-learning can takes the elements of a state, compare it to a heuristic, and judge its value based on its experience using that particular heuristic, rather than its experience being in that unique state
  - This is especially useful for Pacman, as there's too many states for Q-learning to reasonably learn all of their values. However, approximate Q-learning is able to generalise states and their values, and apply similar values to states with similar outcomes, but with varying compositions

#### *Disadvantages*
- Difficult to train well using regular Q-learning in a long Pacman competition, as the layouts used aren't always the same, and teams are continually changing and improving their strategies which requires more learning
- Diversity of competition opponents means that some policies that Q-learning might form against particular opponents may not work as well against others