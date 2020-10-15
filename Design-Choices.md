# Design Choices

We started our agents as a single offensive agent and a single defensive agent such as that of baselineTeam’s. This however did not prove efficient based on the contest feedback as coming up against staff team medium where two offensive agents concurrently attacked us soon proved that our single defensive agent does not have the capability to defend our grid. We have then switched our offensive agent to both attack and defend and so it would help if two opponent pacman were to attack both agents capable of defending, however this soon produces another issue as both agents would chase after a single opponent and leave the other opponent’s pacman unsupervised. We have then switched to the approach of having two offensive agent that is capable of attacking and defending at the same time at ‘top’ and ‘bottom’ part of the grid for the preliminary contest, this however is not efficient as we thought as occasionally both agent would attack concurrently and would usually result in a lost of scores due to lack of supervision of the opponent’s team. We are currently switching back to a single offensive and defensive agent with a smarter evaluation function. 


## General Comments

_General comments about the project goes here_

## Comments per topic

## Offense
For offense we have tried multiple AI techniques for this agent. 

## Defense
