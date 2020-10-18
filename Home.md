# RMIT COSC1125/1127 AI Pacman Contest Project
## Introduction
Pacman capture the flag contest is relatively different from the regular pacman games. Starting off with two teams competing with one another, each teams have two agents that can either be offensive or defensive. Offense agents are responsible to enter opponent's territory and 'steal' food pellets. Each food pellets eaten would be turned to score when the offensive agent returns to its own side of the grid. Similarly opponent's pacman would do the same. This is where the role of defensive agent comes in. Defensive agent is responsible of 'protecting' its own side of the grid's food pellets and prevents opponent's pacman from entering and 'stealing' its foods. Rules are relatively basic, and the rules of classic pacman still stands such as a pacman is able to eat opponent's ghost if power capsules have been consumed. The team with the most score 'food pellets stolen' wins!

## List of pages
1. [Home and Introduction]()
2. [Design Choices (Offense/Defense)](Design-Choices)

    2.1 [Expectimax and Heuristics](AI-Method-1)

    2.2 [Q-learning](AI-Method-2)

    2.3 [Monte Carlo Tree Search](AI-Method-3)
3. [Evolution and Experiments](Evolution)
4. [Conclusions and Reflections](Conclusions-and-Reflections)

## Team Members

List here the full name, email, and student number for each member of the team:

* Minjin Chou - s3641315@student.rmit.edu.au - 3641315
* Chatchapat Dechathaweewat - s3679216@student.rmit.edu.au - 3679216
* William David Ireland - s3719036@student.rmit.edu.au - 3719036


## Useful links - Wiki features

This wiki uses the [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) syntax. 

1. The [MarkDown Demo tutorial](https://guides.github.com/features/mastering-markdown/) shows how various elements are rendered.
2. This 5min video shows how to use markdown for creating [issues](https://www.youtube.com/watch?v=TKJ4RdhyB5Y).
3. The [GitHub documentation](https://docs.gitlab.com/ee/user/project/wiki/) has more information about using a wiki.
4. This video shows how can you use [Project boards and issues](https://www.youtube.com/watch?v=nI5VdsVl0FM&list=PLYMgErMHWi1PRMTsHXote19b7f9F-JjmT&index=2&t=1s) to integrate agile methodologies for working in your team.
5. Documentation on [wikis](https://docs.github.com/en/github/building-a-strong-community/documenting-your-project-with-wikis) by github.

The wiki itself is actually a git repository, which means you can clone it, edit it locally/offline, add images or any other file type, and push it back to us. It will be live immediately.

Go ahead and try:

```
$ git clone https://github.com/RMIT-COSC1127-1125-AI/YOUR-REPO-NAME.wiki.git
```

or if you have the ssh registered in GitHub (to avoid entering the password every time), simply:

```
$ git clone git@github.com:RMIT-COSC1127-1125-AI/YOUR-REPO-NAME.wiki.git
```


Wiki pages are normal files, with the `.md` extension. You can edit them locally, as well as creating new ones.

## Syntax highlighting


Here's an example of some Python code:

```python

def wiki_rocks(text):
    formatter = lambda t: "funky"+t
    return formatter(text)
```