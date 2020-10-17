# Method 2: Q-learning

Your notes about this part of the project, including acknowledgement, comments, strengths and limitations, etc. You do not need to explain the algorithm, tell us how you used it and how you applied it in your team.

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
- An advantage of approximate q-learning in particular, is that while q-learning learns the value of unique states through many iterations and experiences of being in that unique state, approximate q-learning can takes the elements of a state, compare it to a heuristic, and judge its value based on it's experience using that particular heuristic, rather than its experience being in that unique state

#### *Disadvantages*
- Difficult to train well using regular q-learning in a long competition, as the layouts used aren't always the same, and teams are continually changing and improving their strategies which requires more learning
- Diversity of competition opponents means that some policies that q-learning might form against particular opponents may not work as well against others

[Back to top](#table-of-contents)

### Future improvements  

[Back to top](#table-of-contents)
