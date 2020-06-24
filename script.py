# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:22:01 2020

@author: Patrick
"""

import pygame
import sys
from pygame.locals import *
import os

# os.chdir('set path if not working')
import helpers
import states
#%%
#Idea for later:
#Make the points you gain in this skill, grant you internet accessto sites like youtube/facebook/reddit

#%%
#Globals
main = os.getcwd()
black = (0, 0, 0)
white = (255, 255, 255)
with open(main+'\\states\\screen_dims.txt','r') as f:
    data = f.readlines()
    screen_w,screen_h = tuple(data[0].split(','))
    screen_w = int(screen_w)
    screen_h = int(screen_h)

pygame.init()

def loop():
    pygame.init()
    state = {'running':1,'title':1,'game1':0,'options':0}
    #Init and screen
    screen = pygame.display.set_mode((screen_w,screen_h))
    screen.fill(black)
    pygame.display.flip()
    while state['running']==1:
        if state['running']==0:  pygame.quit()
        if state['title']==1:    state = states.title_screen(state,screen)
        if state['options']==1:  state = states.options(state,screen)
        if state['game1']==1:    state = states.game1(state,screen)


            
loop()


##TODO:##
#IMplement data tracking from the main menu:  plt plyplotting that shit
        