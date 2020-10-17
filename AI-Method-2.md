# Q-learning
# Table of Contents
- [Governing Strategy Tree](#governing-strategy-tree)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Future improvements](#future-improvements)

## Governing Strategy Tree 

### Application  

[Back to top](#table-of-contents)

### Trade-offs  

#### *Advantages*  
- Doesn't require as much manual tuning as other methods, as the policies are formed from experience
- An advantage of approximate q-learning in particular, is that while q-learning learns the value of unique states through many iterations and experiences of being in that unique state, approximate q-learning can takes the elements of a state, compare it to a heuristic, and judge its value based on its experience using that particular heuristic, rather than its experience being in that unique state
  - This is especially useful for Pacman, as there's too many states for q-learning to reasonably learn all of their values. However, approximate q-learning is able to generalise states and their values, and apply similar values to states with similar outcomes, but with varying compositions

#### *Disadvantages*
- Difficult to train well using regular q-learning in a long Pacman competition, as the layouts used aren't always the same, and teams are continually changing and improving their strategies which requires more learning
- Diversity of competition opponents means that some policies that q-learning might form against particular opponents may not work as well against others

[Back to top](#table-of-contents)

### Future improvements  

[Back to top](#table-of-contents)
