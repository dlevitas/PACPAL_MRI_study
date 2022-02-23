#import shlex
import pygame
import random
#import platform
from config import *
import numpy as np
#import subprocess as subp


##Determine Monitor Resolution:
#if platform.system() == "Windows":
#    from win32api import GetSystemMetrics
#    w_pix, h_pix = GetSystemMetrics(0), GetSystemMetrics(1)
#elif platform.system() == "Darwin":
#    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
#    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout)
#    if '@' in output:
#        w_pix, h_pix = [int(x.strip(" ")) for x in output.split(':')[-1].split("@")[0].split(' x ')]
#    elif 'Retina' in output:
#        w_pix, h_pix = [int(x) for x in output.split(":")[-1].split("Retina")[0:1][0].split(' x ')]
#    elif 'QHD/WQHD - Wide Quad High Definition' in output:
#        w_pix, h_pix = [int(x) for x in output.split(":")[-1].split("(QHD/WQHD - Wide Quad High Definition)")[0:1][0].split(' x ')]
#elif platform.system() == "Linux":
#    output = subp.check_output("xdpyinfo  | grep -oP 'dimensions:\s+\K\S+'", shell=True).decode("utf-8")
#    w_pix = int(output.split("x")[0])
#    h_pix = int(output.split("x")[-1].split("\n")[0])
#    
#
#print(w_pix, h_pix)
#
#aspect_ratio = w_pix / h_pix
#
#screen_width = round(w_pix / aspect_ratio)
#screen_height = round(h_pix / aspect_ratio)

#pic_pixels = 36
#
#grid_shape = (round(screen_height/pic_pixels), round(screen_width/pic_pixels))
#
#grid = np.zeros(grid_shape)
#
#for x, col in enumerate(grid):
#    for y, y_value in enumerate(col):
#        if x == 0 or x == grid.shape[0]-1:
#            pass
#        elif y == 0 or y == grid.shape[1]-1 :
#            pass
#        else:
#            if (x, y) in [(1, 1), (grid.shape[0]-2, 1), (1, grid.shape[1]-2), (grid.shape[0]-2, grid.shape[1]-2)]:
#                grid[x, y] = 3
#            else:
#                upVal, downVal, leftVal, rightVal = [grid[x-1, y], grid[x+1, y], grid[x, y-1], grid[x, y+1]]
                
                
            
def enviroment_setup(rand_num):
    """Determines which grid is used for the trial as well as the player, ghosts,
    and dots locations. Since there are a variety of options to choose from, this
    information is randomized when a new trial is initialized."""
    
    # generate random seed
    random.seed(rand_num)

    grid_options = []

    gridA = {"grid":   ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0),
                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,4,1,1,1,4,0,0,2,0),
                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0),
                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0),
                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)),
             "id": "A",
             "player_start_pos": [(36, 36), (36, 576), (792, 36), (792, 576)],
             "slime_start_pos": [(288, 216), (540, 216), (288, 396), (540, 396)]
             }
#    gridA = {"grid":   ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0),
#                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,4,1,1,4,1,1,1,5,1,1,1,1,1,1,5,1,1,1,4,1,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,4,1,1,1,4,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,2,0,0,2,0,0,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,3,1,1,4,1,1,1,4,1,1,1,1,1,1,4,1,1,1,4,1,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
#                        (0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0),
#                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)),
#             "id": "A",
#             "player_start_pos": [(36, 36), (36, 576), (792, 36), (792, 576)],
#             "slime_start_pos": [(288, 216), (540, 216), (288, 396), (540, 396)]
#             }    

    gridB = {"grid":   ((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                        (0,3,1,1,1,3,0,0,0,0,3,1,1,1,1,1,1,4,1,1,1,1,3,0),
                        (0,2,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,2,0),
                        (0,2,0,0,0,4,1,1,1,1,4,0,0,0,0,0,0,2,0,0,0,0,2,0),
                        (0,2,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,2,0),
                        (0,4,1,1,1,4,1,1,1,1,5,1,1,1,4,1,1,4,1,1,1,1,4,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0),
                        (0,4,1,1,1,1,1,4,1,1,5,1,1,1,4,1,1,1,4,1,1,1,3,0),
                        (0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0),
                        (0,2,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0),
                        (0,4,1,1,1,1,1,3,0,0,4,1,1,1,1,1,1,1,5,1,1,1,3,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,2,0),
                        (0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,2,0),
                        (0,3,1,1,1,1,1,1,1,1,4,1,1,1,1,1,1,1,4,1,1,1,3,0),
                        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)),
             "id": "B",
             "player_start_pos": [(36, 36), (36, 576), (792, 36), (792, 576)],
             "slime_start_pos": [(360, 180), (360, 360), (648, 468)]
            }
    

    # combine grid options
    grid_options.append([gridA, gridB])
    grid_options = [x for y in grid_options for x in y] # flatten list of dics

    # randomly select a grid option
    grid_data = random.choice(grid_options)

    # grid
    grid = grid_data["grid"]

    # grid ID
    grid_id = grid_data["id"]

    # randomly select player start position
    player_start_pos = random.choice(grid_data["player_start_pos"])

    # randomly select slimes start positions
    slime1_start_pos = random.choice(grid_data["slime_start_pos"])
    slime2_start_pos = random.choice([x for x in grid_data["slime_start_pos"] if x != slime1_start_pos])
    slimes_start_pos = [slime1_start_pos, slime2_start_pos]

    # get all intersections (2-way, 3-way, 4-way) and horizontal and vertical
    horizontal = []
    vertical = []
    intersection_2way = []
    intersection_3way = []
    intersection_4way = []

    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                pos_type = "horizontal"
                upVal, downVal, leftVal, rightVal = 0, 0, 1, 1
                legal_directions = ["left", "right"]
                horizontal.append(((j*36, i*36), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

            elif item == 2:
                pos_type = "vertical"
                upVal, downVal, leftVal, rightVal = 2, 2, 0, 0
                legal_directions = ["up", "down"]
                vertical.append(((j*36, i*36), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

            elif item in [3, 4, 5]:
                legal_directions = []
                upVal = grid[i-1][j]
                downVal = grid[i+1][j]
                leftVal = grid[i][j-1]
                rightVal = grid[i][j+1]

                if upVal != 0:
                    legal_directions.append("up")
                if downVal != 0:
                    legal_directions.append("down")
                if leftVal != 0:
                    legal_directions.append("left")
                if rightVal != 0:
                    legal_directions.append("right")

                if item == 3:
                    pos_type = "2way"
                    intersection_2way.append(((j*36, i*36), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))
                elif item == 4:
                    pos_type = "3way"
                    intersection_3way.append(((j*36, i*36), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))
                elif item == 5:
                    pos_type = "4way"
                    intersection_4way.append(((j*36, i*36), [upVal, downVal, leftVal, rightVal], legal_directions, pos_type))

    dots_pos = [x[0] for x in intersection_2way+intersection_3way+intersection_4way if x[0] != player_start_pos]
    dots_pos = random.sample(dots_pos, 15)

    return grid, player_start_pos, slimes_start_pos, dots_pos, grid_id, horizontal, vertical, intersection_2way, intersection_3way, intersection_4way


def draw_enviroment(screen, grid):
    """Creates the grid."""
    
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36+36, i*36], 3) # line drawn left
                pygame.draw.line(screen, BLUE , [j*36, i*36+36], [j*36+36, i*36+36], 3) # line drawn right
            elif item == 2:
                pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36, i*36+36], 3) # line drawn up
                pygame.draw.line(screen, BLUE , [j*36+36, i*36], [j*36+36, i*36+36], 3) # line drawn down
            elif item in [3, 4]:
                upVal = grid[i-1][j]
                downVal = grid[i+1][j]
                leftVal = grid[i][j-1]
                rightVal = grid[i][j+1]

                # 2-way intersection
                if [upVal, downVal, leftVal, rightVal] == [0, 2, 0, 1]: # down<-->right
                    pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36+36, i*36], 3)
                    pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36, i*36+36], 3)
                elif [upVal, downVal, leftVal, rightVal] == [2, 0, 0, 1]: # up<-->right
                    pygame.draw.line(screen, BLUE , [j*36, i*36+36], [j*36+36, i*36+36], 3)
                    pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36, i*36+36], 3)
                elif [upVal, downVal, leftVal, rightVal] == [0, 2, 1, 0]: # down<-->left
                    pygame.draw.line(screen, BLUE , [j*36, i*36], [j*36+36, i*36], 3)
                    pygame.draw.line(screen,BLUE ,[j*36+36,i*36],[j*36+36,i*36+36],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,0,1,0]: # up<-->left
                    pygame.draw.line(screen,BLUE ,[j*36,i*36+36],[j*36+36,i*36+36],3)
                    pygame.draw.line(screen,BLUE ,[j*36+36,i*36],[j*36+36,i*36+36],3)

                # 3-way intersection
                elif [upVal,downVal,leftVal,rightVal] == [2,2,0,1]: # up<-->down<-->right
                    pygame.draw.line(screen,BLUE ,[j*36,i*36],[j*36,i*36+36],3)
                elif [upVal,downVal,leftVal,rightVal] == [0,2,1,1]: # down<-->left<-->right
                    pygame.draw.line(screen,BLUE ,[j*36,i*36],[j*36+36,i*36],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,2,1,0]: # up<-->down<-->left
                    pygame.draw.line(screen,BLUE ,[j*36+36,i*36],[j*36+36,i*36+36],3)
                elif [upVal,downVal,leftVal,rightVal] == [2,0,1,1]: # up<-->left<-->right
                    pygame.draw.line(screen,BLUE ,[j*36,i*36+36],[j*36+36,i*36+36], 3)
                else:
                    pass
