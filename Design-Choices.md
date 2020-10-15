# Design Choices
We started our agents as a single offensive agent and a single defensive agent similar to baselineTeam’s. This however did not prove efficient based on the contest feedback, and we found that both staff_team_medium and staff_team_top use two offensive agents concurrently, proving that our single defensive agent does not have the capability to defend our side of the grid.

We then switched our offensive agent to have both attack and defensive capabilities, which would help if two opponent agents were to attack. However this soon produces another issue as both agents would chase after a single opposing agent and leave the opponent’s other agent unsupervised.

We changed our approach and had two offensive agents that are capable of attacking and defending at the same time, but at the ‘top’ and ‘bottom’ part of the grid for the preliminary contest, this however didn’t work correctly as our agents would tend to get stuck in a loop and would chase enemies on our end of the grid but never actually eat them, always keeping 1 cell between them.
We are currently switching back to a single offensive and defensive agent with a smarter evaluation function.

## General Comments

_General comments about the project goes here_

## Comments per topic

## Offense
For offense we have tried multiple AI techniques for this agent. 

## Defense
