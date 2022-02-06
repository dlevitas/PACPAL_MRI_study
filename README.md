Documentation for the PACMAN game:

1). Source code: https://itsourcecode.com/free-projects/python-projects/pacman-in-python-code/

2). The source code has been heavily adapted for fMRI experiment

3). To run experiment, execute the main.py file. All other .py files are called from there to help build the game.

4) Regarding game layout (i.e. environment):
	a). Grid is 18x24 spaces (each space being 32x32 pixels)
    b). Player will always begin in one of the four grid corners
    c). Slimes will always begin in one of the 4-way intersections
    d). There will always be 155/432 moveable spaces
    e). The numbers in the grid are: (0 = non-moveable space, 1 = horizontal movement, 2 = vertical movement, 3 = 2-way intersection, 4 = 3-way intersection, 5 = 4-way intersection)

5). The config.py file contains pygame variables (i.e. unchangeable) that are called throughout the game

6). Changeable variables can be found in main.py under "experiment variables"

7). All timing information is handled by the pygame.time.get_ticks() function, which uses milliseconds. Thus, the experiment game uses milliseconds for timing, but you can set experiment variables in minutes or minutes, which will be converted.

8). If player dies < 3 seconds into the the salience period (safe, threat), the following trial will keep the same period. The reason for this is that the player didn't have much time to interact in the new period before the trial ended. 