Documentation for the PACMAN game:

- 1). Source code: https://itsourcecode.com/free-projects/python-projects/pacman-in-python-code/

- 2). The source code has been heavily adapted for fMRI experiment.

- 3). To run experiment, execute the main.py file. All other .py files are called from there to help build the game.

- 4). Regarding game layout (i.e. environment):
	- a). Grid is 18x24 spaces (each space being 36x36 pixels)
    - b). Player will always begin in one of the four grid corners
    - c). Slimes will always begin in one of the 4-way intersections
    - d). There will always be 155/432 moveable spaces
    - e). The numbers in the grid are: (0 = non-moveable space, 1 = horizontal movement, 2 = vertical movement, 3 = 2-way intersection, 4 = 3-way intersection, 5 = 4-way intersection)

- 5). The config.py file contains pygame variables that are called throughout the game

- 6). Aditional variables can be found in main.py under "experiment variables"

- 7). All timing information is handled by the pygame.time.get_ticks() function, which uses milliseconds. Thus, the experiment game uses milliseconds for timing, but you can set experiment variables in minutes or minutes, which will be converted.

- 8). Direction movement keys can be found in the config.py file and modifed as you see fit.

- 9). To efficiently familiarize participants with the game play, a practice session occurs during the anat/T1w acquisition (~ 6 min), which comes right before the actual data collection. Practice log files are denoted by "run-0" and can be ignored during pre-processing & analyses.

- 10). When player "loses" trial (i.e. caught by ghosts or run out of health), they incurr a cost of $0.03 to their bonus.

- 11). Specs are:
	- a). python version 3.7
	- b). pygame version 2.0.2
	- c). anaconda version 2019.03
	- d). numpy version 1.19.5
	- e). pandas version 0.24.2
	- f). scipy version 1.7.1
