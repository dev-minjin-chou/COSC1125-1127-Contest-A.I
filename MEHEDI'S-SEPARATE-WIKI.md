**Introduction
 Pacman capture the flag contest is a different types game of the regular pacman games. It have two agent which is offensive and defensive.Offense agents are responsible to enter opponent's base and eat dots.Numbers of dots eaten would be counted to score when the offensive agent returns to its own base safely. Similarly, opponent's pacman would do the same.On the other hand Defensive agent is responsible of 'protecting' its own base and obstruct opponent's pacman from entering and eating its dots.The team with the most score eaten dots wins!

**Techniques:**
For the Pacman-Final-contest i was working Monte-Carlo search technique for both Offensive and Defensive agent.i use Monte Carlo technique to  finding the best possible moves from all the available moves. Various heuristic functions are applied for getting all the possible moves.I am using deep copy function to analysis the game state while calculating.I have also used multiple function to calculate the value of each state. 

**Offensive**
For the offensive agent i used Monte Carlo techniques for finding the best possible moves.one problem is that the current design cannot handle reverse moves so algorithm breaks if reverse moves happens.In the case where a dots is eaten,it is assigning a negative points and ignore the ghost surrounding it. Once a agent see a ghost in the enemy base it will immediately try to return to its base by eating one dots. If the agents does not see any ghost in the enemy region it it heads towards the dots eats it and then eats the maximum food possible.

**Defensive**
The ghost agent continues watching the center point until it sees an enemy pacman in it's conspicuous reach. The agent will find the closest path to the pacman by using the open heuristic procedures, try to execute and a while later return back to center base once kill.
