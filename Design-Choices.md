# Design Choices
We started our agents as a single offensive agent and a single defensive agent similar to baselineTeam’s. This however did not prove efficient based on the contest feedback, and we found that both staff_team_medium and staff_team_top use two offensive agents concurrently, proving that our single defensive agent may not have the capability to defend our side of the grid.

We then switched our offensive agent to have both attack and defensive capabilities, which would help if two opponent agents were to attack. However this soon produces another issue as both agents would chase after a single opposing agent and leave the opponent’s other agent unsupervised.

We changed our approach and had two offensive agents that are capable of attacking and defending at the same time, but at the ‘top’ and ‘bottom’ part of the grid for the preliminary contest, this however didn’t work correctly as our agents would tend to get stuck in a loop and would chase enemies on our end of the grid but never actually eat them, always keeping 1 cell between them.

We attempted to use a Q-learning agent as the base agent rather than a reflex agent, so that it could compare legal actions using Q-values. However, because the desired features and their weights were already refined enough, Q-learning was taking steps in the wrong direction. We attempted to make an approximate Q-learning agent, but there wasn't enough time to complete work on that agent.

After trying to achieve good results by improving the expectimax agents further and not getting much of anything out of it, we decided to pivot to a new strategy using Monte Carlo Tree Search, which gave us exceedingly great results compared to our previous attempts. We decided to use these agents as our final submission after improving their capabilities.

## General Comments


## Comments per topic

## Offense
For offense we have tried multiple AI techniques for this agent.
## Defense
