#### What is this game?

The game is in the very early stage of the development and there is not much to play with. That said, I am getting close to the first pre-alpha release – please see ROADMAP.md for more info.


#### OK, so what will this game be like in the future?

I aim to create a small scale tactical game, in the veins of the Into The Breach. Just a handful of units on a small map, short missions, no micromanagement.


#### What is the goal of the project?

The goal is to learn something new. I will try to use design patterns, tinker with both inheritance and composition, discipline myself to document the code well using the commonly used formatting. Simply, the goal is to learn, to develop new, better practices and maybe get rid of some bad habits.


#### How does it look like?

For the prototyping, I use graphics from game-icons.net (appropiate license notices are included in this repository). At some point, I would like to overhaul the graphics and use a custom-made pixel sprites. 

![player-movement](https://github.com/VedVid/untitled-strategy-game/blob/development/images/1.png)
![player-attack](https://github.com/VedVid/untitled-strategy-game/blob/development/images/2.png)
![gif](https://github.com/VedVid/untitled-strategy-game/blob/development/images/3.gif)


#### How to play?

You can download this repository, ensure that the requirements are met, and run `main.py`. When the game is mature enough, binary releases will be uploaded.  

Game is mostly playable by mouse:
* left mouse button on player character: select unit, switch from "move" command to "attack" command
* left mouse button while in movement mode: move unit to the tile under the cursor
* left mouse button while in attack mode: target tile under the cursor
* left mouse button during animation: speed up the animation
* right mouse button: "go back", so switch from "attack" command to "move" command, deselected unit
* space key: end your turn.

You can also run the tests by `python -m pytest`.


#### I don't see a license in the repository, is that an oversight?

While most of my work is released under open source licenses, that's not the case here. This project is only source-available. 

