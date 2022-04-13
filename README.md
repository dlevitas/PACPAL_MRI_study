Documentation for the PACMAN game:

- 1). The source code for this game experiment has been heavily modifed from from https://itsourcecode.com/free-projects/python-projects/pacman-in-python-code/

- 2). To run experiment, execute the main.py file. All other .py files are called from there.

- 3). Game layout (i.e. environment):
	- a). Grid is 18x24 spaces (each space being 36x36 pixels)
    - b). Player always begins in one of the four grid corners
    - c). Ghosts always begin in one of the 4-way intersections
    - d). There are 10 grid maps, all of which contain 155 (out of 432) moveable spaces
    - e). A grid map is randomly selected at the onset of each trial
    - f). The numbers in the grid are: (0 = non-moveable space, 1 = horizontal movement, 2 = vertical movement, 3 = 2-way intersection, 4 = 3-way intersection, 5 = 4-way intersection)

- 4). The config.py file contains experiment and pygame variables that are called throughout the game.

- 5). All timing information is handled by the pygame.time.get_ticks() function, which uses milliseconds. Thus, the experiment game uses milliseconds for timing, but you can set experiment variables in minutes or seconds, which will be converted to milliseconds.

- 6). Direction movement keys can be found in the config.py file and modifed as you see fit.

- 7). To familiarize participants with the game play, a practice session occurs during the anat/T1w acquisition (~ 8 min), which occurs right before the actual data collection. Practice log files are denoted by "run-0" and can be ignored during pre-processing & analyses.

- 8). When player "loses" trial (i.e. caught by ghosts or run out of health), they incurr a cost of $0.10 to their cumulative bonus.

- 9). Although each trial contains multiple dots, only one is visible to the player at a time. 

- 10). There are two salience periods: safe (ghosts turn green) and threat (ghosts turn red).

- 11). During threat period, ghosts aim to chase player. During safe period, ghosts aim to get closer to the dot that is visible to the player.

- 12). Game specs:
	- a). python version 3.8
	- b). pygame version 2.0.2
	- c). anaconda version 2020.07
	- d). numpy version 1.19.5
	- e). pandas version 0.24.2
	- f). scipy version 1.7.1
	- g). natsort version 8.1.0
