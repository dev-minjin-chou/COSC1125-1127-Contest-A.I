# Evolution of the approach

## First Agent Team - Heuristic Offensive and Defensive Agents
----
#### Strategy summary
The first team composition we tried out were 2 heuristic agents that used expectimax adversarial search. One agent was tasked with travelling to the opponent's end of the board and collecting food, the other was tasked with standing guard at the border of our end of the board, and chasing down enemy agents that made it past the border.

### Demo

*1. Both agents chasing after the same opponent*

![(27/09) Chasing Enemy](images/27-09_chase_enemy.gif)

*2. Both agents stuck in the same loop*

![(27/09) Stuck in loop](images/27-09_loop.gif) 

*3. Offense agent giving power pellets little value*

![(27/09) Misusing Power Pellets](images/27-09_power.gif)

#### Competition: Daily (27/09 3:19am)
#### Results: Position - 38/53 | No staff teams beaten

![(27-09) Leaderboard](images/27-09_leaderboard.png)

#### Results summary
We only managed to beat staff_team_basic once, and every other staff team match was lost. We were 2 places beneath staff_team_basic on the leaderboard, so ultimately there needed to be a lot more work done to make the agents perform better.

| Pros | Cons |
|-----------------|:-------------|
| First body part | Second cell  |
| Second line     | foo          |
----
## Second Agent Team - Heuristic Offensive Agents
----
#### Strategy summary
We learnt through some testing and observing other teams that having multiple offensive agents was a good choice. We took our original offensive agent and tweaked it further so that it would patrol different regions of the board to cover the most distance.

### Demo

*1. Ghosts keeping their distance from Pacman*

![(prelim) Ghosts keeping distance from pacman](images/prelim_ghost.gif)

*2. Ghosts trap Pacman, but are stuck and refuse to eat him*

![(prelim) Ghosts trap pacman](images/prelim_stuck.gif)

#### Competition: Preliminary
#### Results: Position - 59/69 | No staff teams beaten

![Demo 1](images/prelim_leaderboard.png)

#### Results summary
We were beaten by every staff team, except for one match with staff_team_top, although that was most likely random luck. As the agents would rarely ever eat any opponents, but would still chase them around the board, we would lose a large majority of matches as long as the opponents managed to get at least 1 pellet.


| Pros | Cons |
|-----------------|:-------------|
| First body part | Second cell  |
| Second line     | foo          |
