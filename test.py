#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 17:09:41 2021

@author: dlevitas
"""
import os
import sys
import time
import pygame
import importlib
# from config import seed
import config

data_dir = os.getcwd()

# print("Enter subject ID:")
# s = input()

# print("Enter run ID:")
# r = input()

# subID = s
# runID = r

# print(subID, runID)



# def update_seed(seed):
#     # importlib.reload(config)
#     import config

#     file = open("{}/config.py".format(data_dir), "w")
#     file.write("seed = {}".format(config.seed + seed))
#     file.close()

#     exec(open("{}/config.py".format(data_dir)).read(), globals())


#     return config.seed


# for i in range(10):
#     print(update_seed(i))




# for i in range(10):
#     seed += 1

#     start = time.time()

#     file = open("{}/config.py".format(data_dir), "w")
#     file.write("seed = {}".format(seed))
#     file.close()

#     end = time.time()

#     print("The elapsed time to generate seed {} was {}".format(seed, (end-start)))

#     # file = open("{}/config.py".format(data_dir), "r")
#     # print(file.read())
#     # print(seed)

# start = time.time()
# pygame.time.delay(3000)
# end = time.time()
# print("The elapsed time was {}".format(end-start))

# subID = 'ms@'
# runID = '02'


# if not subID.isalnum():
#     raise ValueError("The subID contains non-alphanumeric character(s). Please re-enter subID")

# try:
#     if not int(runID):
#         raise ValueError("The runID is not an integer value. Please re-enter runID")
# except:
#     raise ValueError("The runID is not an integer value. Please re-enter runID")


def test():
    a = False
    b = False

    return True, False

a,b = test()
print(a,b)


