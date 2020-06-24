# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:40:23 2020

@author: Patrick
"""

#GAME STATE FUNCTIONS
import pygame
from helpers import get_image,save_diff,dborder_state_definer,wborder_state_definer,uborder_state_definer,get_vocab,get_gender_vocab,get_plural_vocab
import random
import numpy as np
from os import getcwd
from pygame.locals import *
import pandas
import csv
import xlrd
from datetime import datetime
pygame.init()
main = getcwd()
with open(main + '\\states\\screen_dims.txt','r') as f:
    data = f.readlines()
    screen_w,screen_h = tuple(data[0].split(','))
    screen_w = int(screen_w)
    screen_h = int(screen_h)
    
word_list = get_vocab()  #[{eng:,german:,type:N/A/V/M,diff:E/M/H}]
gender_word_list = get_gender_vocab()
plural_word_list = get_plural_vocab()

letters                 = pygame.sprite.Group()
arrows                  = pygame.sprite.Group()
options1_arrows         = pygame.sprite.Group()
options2_arrows         = pygame.sprite.Group()
clouds                  = pygame.sprite.Group()
option_arrows           = pygame.sprite.Group()
option_difficult_arrows = pygame.sprite.Group()
option_word_arrows      = pygame.sprite.Group()
border_arrow            = pygame.sprite.Group()
player_arrow            = pygame.sprite.Group()
player_border_arrow     = pygame.sprite.Group()
word_balloons           = pygame.sprite.Group()
life_balloons           = pygame.sprite.Group()
gender_balloons         = pygame.sprite.Group()
plural_balloons         = pygame.sprite.Group()

class Genders(pygame.sprite.Sprite):
    font = pygame.font.SysFont('comicsansms', 30)
    
    def __init__(self,dict_entry):
        pygame.sprite.Sprite.__init__(self, gender_balloons)
        self.dict_entry = dict_entry
        self.german_str = dict_entry['GermanNoun'][0]
        self.gender_str = dict_entry['Gender'][0]

        self.width = len(self.german_str)
        self.height = random.randint(50,100)
        self.balloon_image, self.balloon_rect = get_image(main+'\\sprites\\airballoon1.png',self.width*30,self.height,reload=True) 
        self.balloon_image = self.balloon_image.convert()
        self.balloon_image.set_colorkey((255,255,255))
        self.balloon_rect.centery = int(7*screen_h/10)
        self.balloon_rect.centerx = random.randint(0+self.width*20,screen_w-self.width*20)
        
        self.word_display, self.word_display_rect = get_image(main+'\\sprites\\airballoon2.png',int(self.width*30),40,reload=True)
        self.word_display = self.word_display.convert()
        self.word_display.set_colorkey((255,255,255))
        self.word_display_rect.centery = self.balloon_rect.centery+self.balloon_rect.height
        self.word_display_rect.centerx = self.balloon_rect.centerx
        
        self.word_block = Words.font.render(self.german_str, True, (1,1,1))
        self.word_rect  = self.word_block.get_rect()
        self.word_rect.centery = self.word_display_rect.centery-5
        self.word_rect.centerx = self.balloon_rect.centerx-10
        
        self.answer_block = Words.font.render(self.gender_str,True,(1,1,1))
        self.answer_rect  = self.answer_block.get_rect()

        self.i = 0
        
    def move(self):
        if self.i%2 == 0:
            self.balloon_rect.centery      -= np.ceil(screen_h/400)
            self.word_rect.centery         -= np.ceil(screen_h/400)
            self.word_display_rect.centery -= np.ceil(screen_h/400)
        self.i += 1
    
    def border_check(self):
        if self.word_display_rect.centery <= 5: return False,False
        else: return True,True
        

class Plurals(pygame.sprite.Sprite):
    font = pygame.font.SysFont('comicsansms', 30)
    
    def __init__(self,dict_entry):
        pygame.sprite.Sprite.__init__(self, plural_balloons)
        self.dict_entry = dict_entry
        self.german_str = dict_entry['GermanNoun'][0]
        self.plural_str = dict_entry['Plural'][0]
        
        self.width = len(self.german_str)
        self.height = random.randint(50,100)
        self.balloon_image, self.balloon_rect = get_image(main+'\\sprites\\airballoon1.png',self.width*30,self.height,reload=True) 
        self.balloon_image = self.balloon_image.convert()
        self.balloon_image.set_colorkey((255,255,255))
        self.balloon_rect.centery = int(7*screen_h/10)
        self.balloon_rect.centerx = random.randint(0+self.width*20,screen_w-self.width*20)
        
        self.word_display, self.word_display_rect = get_image(main+'\\sprites\\airballoon2.png',int(self.width*30),40,reload=True)
        self.word_display = self.word_display.convert()
        self.word_display.set_colorkey((255,255,255))
        self.word_display_rect.centery = self.balloon_rect.centery+self.balloon_rect.height
        self.word_display_rect.centerx = self.balloon_rect.centerx
        
        self.word_block = Words.font.render(self.german_str, True, (1,1,1))
        self.word_rect  = self.word_block.get_rect()
        self.word_rect.centery = self.word_display_rect.centery-5
        self.word_rect.centerx = self.balloon_rect.centerx+15
        
        self.answer_block = Words.font.render(self.plural_str,True,(1,1,1))
        self.answer_rect  = self.answer_block.get_rect()

        self.i = 0
        
    def move(self):
        if self.i%2 == 0:
            self.balloon_rect.centery      -= np.ceil(screen_h/400)
            self.word_rect.centery         -= np.ceil(screen_h/400)
            self.word_display_rect.centery -= np.ceil(screen_h/400)
        self.i += 1
    
    def border_check(self):
        if self.word_display_rect.centery <= 5: return False,False
        else: return True,True
        
class Words(pygame.sprite.Sprite):
    font = pygame.font.SysFont('comicsansms', 27)
    
    def __init__(self,dict_entry):
        pygame.sprite.Sprite.__init__(self, word_balloons)
        self.dict_entry = dict_entry
        self.type = dict_entry['Type'][0]
        self.difficulty = dict_entry['Difficulty'][0]
        self.english_str = dict_entry['English']
        self.german_str = dict_entry['German'][0]
        
        self.width = len(self.german_str)
        self.height = random.randint(50,100)
        
        self.jrand = random.randint(0,2)
        if self.jrand == 0:
            self.word_display, self.word_display_rect = get_image(main+'\\sprites\\pixel_balloon1.png',int(self.width*24),120,reload=True)
        elif self.jrand == 1:
            self.word_display, self.word_display_rect = get_image(main+'\\sprites\\pixel_balloon2.png',int(self.width*24),120,reload=True)
        elif self.jrand == 2:
            self.word_display, self.word_display_rect = get_image(main+'\\sprites\\pixel_balloon3.png',int(self.width*24),120,reload=True)
        self.word_display = self.word_display.convert()
        self.word_display.set_colorkey((255,255,255))
        self.word_display_rect.centery = int(6*screen_h/10)+self.word_display_rect.height
        self.word_display_rect.centerx = random.randint(0+self.width*20,screen_w-self.width*20)
        
        self.word_block = Words.font.render(self.german_str, True, (1,1,1))
        self.word_rect  = self.word_block.get_rect()
        self.word_rect.centery = self.word_display_rect.centery-18
        self.word_rect.centerx = self.word_display_rect.centerx
        
        self.answer_block = Words.font.render(self.english_str[0],True,(1,1,1))
        self.answer_rect  = self.answer_block.get_rect()

        self.i = 0
        
    def move(self):
        if self.i%2 == 0:
            self.word_rect.centery         -= np.ceil(screen_h/400)
            self.word_display_rect.centery -= np.ceil(screen_h/400)
        self.i += 1
    
    def border_check(self):
        if self.word_display_rect.centery <= 5: return False,False
        else: return True,True
        

class Letters(pygame.sprite.Sprite):
    time = np.arange(0, 63, 0.05)
    pattern = 10*np.sin(time)
    
    def __init__(self,path,xsize,ysize,xpos,ypos):
        pygame.sprite.Sprite.__init__(self, letters)
        self.i = int(random.randint(0,len(Letters.time)))
        self.path = path
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.path = main + self.path
        self.image,self.rect = get_image(self.path,self.xsize,self.ysize)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos        
    
    def move(self):
        try:
            self.dy = Letters.pattern[int(np.ceil(self.i))]
            self.i += 0.4
            # self.ypos += np.ceil(self.dy/1) 
            self.rect.centery = self.ypos - int(np.ceil(self.dy/1))
        except IndexError:
            self.i=0

class Lives(pygame.sprite.Sprite):
    def __init__(self,path,xsize,ysize,xpos,ypos):
        pygame.sprite.Sprite.__init__(self, life_balloons)
        self.path = path
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.path = main + self.path
        self.image,self.rect = get_image(self.path,self.xsize,self.ysize)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos    
        
    def die(self):
        self.kill()

class Arrows(pygame.sprite.Sprite):
    def __init__(self,path,xsize,ysize,xpos,ypos):
        pygame.sprite.Sprite.__init__(self, arrows)
        self.path = path
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.path = main + self.path
        self.image,self.rect = get_image(self.path,self.xsize,self.ysize)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos     
        
        
class Clouds(pygame.sprite.Sprite):
    def __init__(self,path,xsize,ysize,xpos,ypos):
        pygame.sprite.Sprite.__init__(self, clouds)
        self.path = path
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.path = main + self.path
        self.image,self.rect = get_image(self.path,self.xsize,self.ysize)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos       
        self.i = 1
        self.dx = random.randint(1,3)
    
    def move(self):
        if self.i % 5 == 0:
            self.xpos += self.dx
            self.rect.centerx += self.dx
        self.i += 1
        
        if self.rect.x >= screen_w:
            self.xpos,self.rect.x = -self.xsize,-self.xsize
            new_pos = random.randint(self.ysize,screen_h-self.ysize)
            self.ypos,self.rect.centery = new_pos,new_pos
            self.dx = random.randint(1,3)
            
class OptionArrows(pygame.sprite.Sprite):
    def __init__(self,group,path,xsize,ysize,xpos,ypos):
        self.group = group
        if self.group == 'main_options':
            pygame.sprite.Sprite.__init__(self, option_arrows)
        elif self.group == 'difficulty_options':
            pygame.sprite.Sprite.__init__(self, option_difficult_arrows)
        elif self.group == 'words':
            pygame.sprite.Sprite.__init__(self, option_word_arrows)
        elif self.group == 'border':
            pygame.sprite.Sprite.__init__(self,border_arrow)
        elif self.group == 'player_arrow':
            pygame.sprite.Sprite.__init__(self,player_arrow)
        elif self.group == 'player_border_arrow':
            pygame.sprite.Sprite.__init__(self,player_border_arrow)
        self.path = path
        self.xsize = xsize
        self.ysize = ysize
        self.xpos = xpos
        self.ypos = ypos
        self.path = main + self.path
        self.image,self.rect = get_image(self.path,self.xsize,self.ysize)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect.centerx = self.xpos
        self.rect.centery = self.ypos
        

def title_screen(state,screen):
    pygame.init()
    screen_w,screen_h = screen.get_size()
    
    #Get Sprites
    title_background, title_background_rect = get_image(main+'\\sprites\\title_background.png',screen_w,screen_h)
    title_background.convert()
    title_background.set_colorkey((255,255,255))
    
    play_arrow = Arrows('\\sprites\\play_arrow.png',int(screen_w/3),int(screen_h/5),      int(screen_w/3),int(65*screen_h/100))
    options_arrow = Arrows('\\sprites\\options_arrow.png',int(screen_w/3),int(screen_h/5),int(screen_w/3),int(80*screen_h/100))

    b = Letters('\\sprites\\B_balloon1.png',int(screen_w/6),int(screen_h/6),  int(10*screen_w/100), int(25*screen_h/100))
    a1 = Letters('\\sprites\\A_balloon1.png',int(screen_w/6),int(screen_h/6),int(24*screen_w/100), int(25*screen_h/100))
    l1 = Letters('\\sprites\\L_balloon1.png',int(screen_w/6),int(screen_h/6),int(38*screen_w/100), int(25*screen_h/100))
    l2 = Letters('\\sprites\\L_balloon2.png',int(screen_w/6),int(screen_h/6),int(50*screen_w/100),int(25*screen_h/100))
    o1 = Letters('\\sprites\\O_balloon1.png',int(screen_w/6),int(screen_h/6),int(62*screen_w/100),int(25*screen_h/100))
    o2 = Letters('\\sprites\\O_balloon2.png',int(screen_w/6),int(screen_h/6),int(75*screen_w/100),int(25*screen_h/100))
    n1 = Letters('\\sprites\\N1.png',int(screen_w/6),int(screen_h/6),int(81*screen_w/100),int(25*screen_h/100))
    
    p = Letters('\\sprites\\P.png',int(screen_w/6),int(screen_h/6),  int(12*screen_w/100), int(45*screen_h/100))
    l3 = Letters('\\sprites\\L_balloon3.png',int(screen_w/6),int(screen_h/6),int(24*screen_w/100), int(45*screen_h/100))
    a2 = Letters('\\sprites\\A_balloon2.png',int(screen_w/6),int(screen_h/6),int(36*screen_w/100), int(45*screen_h/100))
    t = Letters('\\sprites\\T.png',int(screen_w/6),int(screen_h/6),  int(48*screen_w/100),int(45*screen_h/100))
    o3 = Letters('\\sprites\\O_balloon3.png',int(screen_w/6),int(screen_h/6),int(60*screen_w/100),int(45*screen_h/100))
    o4 = Letters('\\sprites\\O_balloon4.png',int(screen_w/6),int(screen_h/6),int(72*screen_w/100),int(45*screen_h/100))
    n2 = Letters('\\sprites\\N2.png',int(screen_w/6),int(screen_h/6),int(84*screen_w/100),int(45*screen_h/100))
    
    cloud1 = Clouds('\\sprites\\cloud1.png',int(screen_w/3),int(screen_h/6),int(64*screen_w/100),int(25*screen_h/100))
    cloud2 = Clouds('\\sprites\\cloud2.png',int(screen_w/4),int(screen_h/5),int(44*screen_w/100),int(50*screen_h/100))
    
    
    while state['title'] == 1:
        #Blits
        screen.fill((1,1,1))
        screen.blit(title_background,title_background_rect)
        clouds.draw(screen)
        letters.draw(screen)
        arrows.draw(screen)
        pygame.display.flip()
        
        for sprite in letters:
            sprite.move()
        # for cloud in clouds:
        #     cloud.move()
        #Events    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_arrow.rect.collidepoint(pos):
                    state['title']   = 0
                    state['game1']   = 1
                    state['options'] = 0
                elif options_arrow.rect.collidepoint(pos):
                    state['title']   = 0
                    state['game1']   = 0
                    state['options'] = 1
            elif event.type == pygame.QUIT:
                state['running'] = 0
                pygame.quit()
                return state
        
    return state


def options(state,screen):
    screen_w,screen_h = screen.get_size()
    
        #Get Sprites
    title_background, title_background_rect = get_image(main+'\\sprites\\title_background.png',screen_w,screen_h)
    title_background.convert()
    title_background.set_colorkey((255,255,255))
    
    cloud1 = Clouds('\\sprites\\cloud1.png',int(screen_w/3),int(screen_h/6),int(64*screen_w/100),int(25*screen_h/100))
    cloud2 = Clouds('\\sprites\\cloud2.png',int(screen_w/4),int(screen_h/5),int(44*screen_w/100),int(50*screen_h/100))
    
    # user_arrow = OptionArrows('main_options','\\sprites\\user_arrow.png',                int(screen_w/3),int(screen_h/6),  int(15*screen_w/100), int(25*screen_h/100))
    difficulty_arrow = OptionArrows('main_options','\\sprites\\difficulty_arrow.png',    int(screen_w/3.5),int(screen_h/5),  int(20*screen_w/100), int(30*screen_h/100))
    choose_words_arrow = OptionArrows('main_options','\\sprites\\choose_words_arrow.png',int(screen_w/3.5),int(screen_h/5),  int(20*screen_w/100), int(45*screen_h/100))
    user_arrow = OptionArrows('main_options','\\sprites\\user_arrow.png',                int(screen_w/3.5),int(screen_h/5),  int(20*screen_w/100), int(60*screen_h/100))
    back_arrow = OptionArrows('main_options','\\sprites\\back_arrow.png',                int(screen_w/3.5),int(screen_h/5),  int(20*screen_w/100), int(75*screen_h/100))

    easy_arrow = OptionArrows('difficulty_options','\\sprites\\easy_arrow.png',     int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(20*screen_h/100))
    medium_arrow = OptionArrows('difficulty_options','\\sprites\\medium_arrow.png', int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(40*screen_h/100))
    hard_arrow = OptionArrows('difficulty_options','\\sprites\\hard_arrow.png',     int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(60*screen_h/100))
    
    verbs_arrow = OptionArrows('words','\\sprites\\verbs_arrow.png',            int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(10*screen_h/100))
    adjectives_arrow = OptionArrows('words','\\sprites\\adjectives_arrow.png',  int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(25*screen_h/100))
    nouns_arrow = OptionArrows('words','\\sprites\\nouns_arrow.png',            int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(40*screen_h/100))
    plurals_arrow = OptionArrows('words','\\sprites\\plurals_arrow.png',        int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(55*screen_h/100))
    genders_arrow = OptionArrows('words','\\sprites\\genders_arrow.png',        int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(70*screen_h/100))
    mixed_arrow = OptionArrows('words','\\sprites\\mixed_arrow.png',            int(screen_w/3),int(screen_h/6),  int(55*screen_w/100), int(85*screen_h/100))

    player1_arrow = OptionArrows('player_arrow','\\sprites\\player1.png', int(screen_w/3),int(screen_h/2),  int(45*screen_w/100), int(50*screen_h/100))
    player2_arrow = OptionArrows('player_arrow','\\sprites\\player2.png', int(screen_w/3),int(screen_h/2),  int(75*screen_w/100), int(50*screen_h/100))
    
    player1_border_arrow = OptionArrows('player_border_arrow','\\sprites\\player1_selected.png', int(screen_w/3),int(screen_h/2),  int(45*screen_w/100), int(50*screen_h/100))
    player2_border_arrow = OptionArrows('player_border_arrow','\\sprites\\player2_selected.png', int(screen_w/3),int(screen_h/2),  int(75*screen_w/100), int(50*screen_h/100))

    select_arrow = OptionArrows('border_arrow','\\sprites\\arrow_border.png',int(screen_w/3),int(screen_h/6),  int(65*screen_w/100), int(60*screen_h/100))
    
    dborder_state = {'E':0,'M':0,'H':0}
    wborder_state = {'V':0,'A':0,'N':0,'P':0,'G':0,'M':0}
    uborder_state = {'player1':0,'player2':0}
    btn_state = {'Words':0,'Difficulty':0,'User':0,'Back':0}
    
    dselect = False
    wselect = False
    uselect = False
    
    while state['options'] == 1:
        #Blits
        screen.fill((1,1,1))
        screen.blit(title_background,title_background_rect)
        clouds.draw(screen)
        option_arrows.draw(screen)
        
        with open(main + '\\states\\difficulty.txt','r') as f:
            d = f.readlines()
        dborder_state = dict.fromkeys(dborder_state,0)
        dborder_state[d[0]] = 1
        
        with open(main + '\\states\\word_choice.txt','r') as f:
            w = f.readlines()
        wborder_state = dict.fromkeys(wborder_state,0)
        wborder_state[w[0]] = 1
        
        with open(main + '\\states\\user.txt','r') as f:
            u = f.readlines()
        uborder_state = dict.fromkeys(uborder_state,0)
        uborder_state[u[0]] = 1

        
        ##User Select
        if btn_state['User'] == 1:
            player_arrow.draw(screen)
            if uborder_state['player1'] == 1:
                player1_border_arrow.rect.centerx = player1_arrow.rect.centerx
                player1_border_arrow.rect.centery = player1_arrow.rect.centery
                screen.blit(player1_border_arrow.image,player1_border_arrow.rect)
            elif uborder_state['player2'] == 1:
                player2_border_arrow.rect.centerx = player2_arrow.rect.centerx
                player2_border_arrow.rect.centery = player2_arrow.rect.centery
                screen.blit(player2_border_arrow.image,player2_border_arrow.rect)
                
        ##SHOW CSV WORD CHOICES##
        if btn_state['Words'] == 1:
            option_word_arrows.draw(screen)
            if wborder_state['V'] == 1:
                select_arrow.rect.centerx = verbs_arrow.rect.centerx
                select_arrow.rect.centery = verbs_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif wborder_state['A'] == 1:
                select_arrow.rect.centerx = adjectives_arrow.rect.centerx
                select_arrow.rect.centery = adjectives_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif wborder_state['N'] == 1:
                select_arrow.rect.centerx = nouns_arrow.rect.centerx
                select_arrow.rect.centery = nouns_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)
            elif wborder_state['P'] == 1:
                select_arrow.rect.centerx = plurals_arrow.rect.centerx
                select_arrow.rect.centery = plurals_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif wborder_state['G'] == 1:
                select_arrow.rect.centerx = genders_arrow.rect.centerx
                select_arrow.rect.centery = genders_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif wborder_state['M'] == 1:
                select_arrow.rect.centerx = mixed_arrow.rect.centerx
                select_arrow.rect.centery = mixed_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect) 
                       
        
        ##SHOW DIFFICULTY OPTIONS##
        if btn_state['Difficulty'] == 1:
            option_difficult_arrows.draw(screen)
            if dborder_state['E'] == 1:
                select_arrow.rect.centerx = easy_arrow.rect.centerx
                select_arrow.rect.centery = easy_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif dborder_state['M'] == 1:
                select_arrow.rect.centerx = medium_arrow.rect.centerx
                select_arrow.rect.centery = medium_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)   
            elif dborder_state['H'] == 1:
                select_arrow.rect.centerx = hard_arrow.rect.centerx
                select_arrow.rect.centery = hard_arrow.rect.centery
                screen.blit(select_arrow.image,select_arrow.rect)  
        

        
        pygame.display.flip()
        
        #Events    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                ##Create option collisions##
                if btn_state['User'] == 1:
                    if user_arrow.rect.collidepoint(pos):
                        uselect = False
                        btn_state['User'] = 0
                        break
                    for sprite in player_arrow:
                        if sprite.rect.collidepoint(pos):
                            uborder_state = uborder_state_definer(uborder_state,sprite)
                if btn_state['Difficulty'] == 1:
                    if difficulty_arrow.rect.collidepoint(pos):
                        dselect = False
                        btn_state['Difficulty'] = 0
                        break
                    for sprite in option_difficult_arrows:
                        if sprite.rect.collidepoint(pos):
                            dborder_state = dborder_state_definer(dborder_state,sprite)
                if btn_state['Words'] == 1:
                    if choose_words_arrow.rect.collidepoint(pos):
                        wselect = False
                        btn_state['Words'] = 0
                        break
                    for sprite in option_word_arrows:
                        if sprite.rect.collidepoint(pos):
                            wborder_state = wborder_state_definer(wborder_state,sprite)
                        ##BACK BUTTON##

                ##Option State Definitions##
            
                if user_arrow.rect.collidepoint(pos):
                    uselect = True
                    btn_state = dict.fromkeys(btn_state, 0)
                    btn_state['User'] = 1                    
                elif choose_words_arrow.rect.collidepoint(pos):
                    wselect = True
                    btn_state = dict.fromkeys(btn_state, 0)
                    btn_state['Words'] = 1
                elif difficulty_arrow.rect.collidepoint(pos):
                    dselect = True
                    btn_state = dict.fromkeys(btn_state, 0)
                    btn_state['Difficulty'] = 1
                elif back_arrow.rect.collidepoint(pos):
                    btn_state = dict.fromkeys(btn_state, 0)
                    btn_state['Back'] = 1
                    if btn_state['Back'] == 1:
                        state['title'] = 1
                        state['options'] = 0
                        return state
            elif event.type == pygame.QUIT:
                state['running'] = 0
                pygame.quit()
                return state
    return state

def game1(state,screen): 
    screen_w,screen_h = screen.get_size()
    
    ##Get correct game states:
    ##Proper word selection:
    active_word_list = []
    with open(main+'\\states\\word_choice.txt','r') as f:
        word_choice = f.readlines()[0]
    with open(main+'\\states\\difficulty.txt','r') as f:
        diff_choice = f.readlines()[0]

    if word_choice == 'G':
        active_word_list = gender_word_list
    elif word_choice == 'P':
        active_word_list = plural_word_list
    else:
        for entry in word_list:
            if entry['Type'] == [word_choice] and entry['Difficulty'] == [diff_choice]:
                active_word_list.append(entry)
    
    
    random.shuffle(active_word_list)
        ##Generator for nouns,adjs,verbs,mixed##
    def gen_word_balloon():
        for i in active_word_list:
            yield Words(i)
    
    def gen_gender_balloon():
        for i in active_word_list:
            yield Genders(i)
            
    def gen_plural_balloon():
        for i in active_word_list:
            yield Plurals(i)
    
    if word_choice == 'G':
        generated_word = gen_gender_balloon()
    elif word_choice == 'P':
        generated_word = gen_plural_balloon()
    else:
        generated_word = gen_word_balloon()
    
    
    #Get Sprites
    sky,sky_rect = get_image(main+'\\sprites\\sky.png',screen_w,screen_h)
    sky.convert()
    sky.set_colorkey((255,255,255))
    
    inputbox,inputbox_rect = get_image(main+'\\sprites\\inputbox.png',
                         int(screen_w/2.25),
                         int(screen_h/5))
    inputbox.convert()
    inputbox.set_colorkey((255,255,255))
    inputbox_rect.left = int(screen_w/12)
    inputbox_rect.bottom = screen_h
    
    pause_button,pause_rect = get_image(main+'\\sprites\\pause.png',
                             int(screen_w/5),
                             int(screen_h/5))
    pause_button.convert()
    pause_button.set_colorkey((255,255,255))
    pause_rect.right = int(screen_w)
    pause_rect.bottom = screen_h
    
    life1 = Lives('\\sprites\\life1.png',int(1*screen_w/12),int(1*screen_w/12),int(7*screen_w/12),int(10*screen_h/12))
    life2 = Lives('\\sprites\\life2.png',int(1*screen_w/12),int(1*screen_w/12),int(8*screen_w/12),int(10*screen_h/12))    
    life3 = Lives('\\sprites\\life3.png',int(1*screen_w/12),int(1*screen_w/12),int(9*screen_w/12),int(10*screen_h/12))

    
    #Variables
    missed_words = []
    score=0
    font = pygame.font.SysFont('comicsansms', 45)
    lives = 3
    text=''
    gen_state = 1
    
    def paused(state,screen):
        screen_w,screen_h = screen.get_size()
        
        #Fadey screen   
        s = pygame.Surface((screen_w,screen_h))
        s.set_alpha(5)              
        s.fill((254,254,254))
        
        #Get sprites
        unpause_butt,unpause_rect = get_image(main+'\\sprites\\unpause.png')
        unpause_butt.convert()
        unpause_butt.set_colorkey((255,255,255))
        unpause_rect.centerx = int(screen_w/2)
        unpause_rect.centery = int(screen_h/2-(screen_h/5))
        
        return_title_butt,return_title_rect = get_image(main+'\\sprites\\return_to_title.png')
        return_title_butt.convert()
        return_title_butt.set_colorkey((255,255,255))
        return_title_rect.centerx = int(screen_w/2)
        return_title_rect.centery = int(screen_h/2+(screen_h/5))
    
        #Events
        paused = True
        while paused:
            ##Blits
            screen.blit(unpause_butt,unpause_rect)
            screen.blit(return_title_butt,return_title_rect)
            screen.blit(s, (0,0))
            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if unpause_rect.collidepoint(pos):
                        paused = False
                        state['title_screen'] = 0
                        state['game1']        = 1
                        return state
                    elif return_title_rect.collidepoint(pos):
                        paused=False
                        state['game1'] = 0
                        state['title'] = 1
                        return state
                if event.type == pygame.QUIT:
                    state['running'] = 0
                    state['game1']   = 0
                    state['title']   = 0
                    pygame.quit()
                    return state
        return state
    
    def gameover(state,screen,victory = False):
        if not victory:
            gameover_img, gameover_rect = get_image(main+'\\sprites\\gameover.png',screen_w,screen_h)
            screen.blit(gameover_img,gameover_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
        if victory:
            gamewon_img, gamewon_rect = get_image(main+'\\sprites\\youwin.png',screen_w,screen_h)
            screen.blit(gamewon_img,gamewon_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            
        #Read in options
        with open(main+'\\states\\user.txt','r') as f:
            user = f.readlines()[0]
    
        with open(main+'\\states\\difficulty.txt','r') as f:
            difficulty = f.readlines()[0]    
            
        with open(main+'\\states\word_choice.txt','r') as f:
            word_choice = f.readlines()[0] 
            
        #Save scores and potentially missed words
        with open(main+'\\' + user + '_scores\\' + difficulty + '_' + word_choice + '.csv','a') as f:
            writer = csv.writer(f, lineterminator = '\n')
            writer.writerow([datetime.date(datetime.now()),score])
        
        with open(main+'\\' + user + '_scores\\missed_words.csv','a') as f:
            writer = csv.writer(f, lineterminator = '\n')
            for i in missed_words:
                for k,v in i.items():
                    writer.writerow([datetime.date(datetime.now()),(k,v)])
            
        state['game1'] = 0
        state['title'] = 1
        return state
        
    def show_answer(screen,word_obj):
        #Fadey screen   
        s = pygame.Surface((screen_w,screen_h))
        s.set_alpha(5)              
        s.fill((254,254,254))
        
        #Get sprites
        answer_btn,answer_rect = get_image(main+'\\sprites\\show_answer.png',int(screen_w/1.4),int(screen_h/2))
        answer_btn.convert()
        answer_btn.set_colorkey((255,255,255))
        answer_rect.centerx = int(screen_w/2)
        answer_rect.centery = int(screen_h/2)
        word_obj.answer_rect.centerx = answer_rect.centerx
        word_obj.answer_rect.centery = answer_rect.centery
        
        ##Blits
        screen.blit(s, (0,0))
        screen.blit(answer_btn,answer_rect)
        screen.blit(word_obj.answer_block,word_obj.answer_rect)

        pygame.display.flip()
        pygame.time.wait(2000)
        
    
    
    ##Main Game Loop
    while state['game1'] == 1:
        
        ##Get generated word objects and calculate lives
        if gen_state == 1:
            word_obj = next(generated_word)
            gen_state += 1
            
        word_status = True
        alive = True
        word_obj.move()
        word_status,alive = word_obj.border_check()
        
        
        ##Eventually print these on screen as well
        if alive == False:
            lives -= 1
            if lives == 2: 
                life1.die()
                pygame.display.update()
                try:
                    print({word_obj.german_str:word_obj.english_str})
                    #Needs a try except to catch the gender/plural cases here
                    missed_words.append({word_obj.german_str:word_obj.english_str})
                except AttributeError:
                    try:
                        print({word_obj.german_str:word_obj.gender_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.gender_str})
                    except AttributeError:
                        print({word_obj.german_str:word_obj.plural_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.plural_str})
                show_answer(screen,word_obj)
            elif lives == 1: 
                life2.kill()
                try:
                    print({word_obj.german_str:word_obj.english_str})
                    #Needs a try except to catch the gender/plural cases here
                    missed_words.append({word_obj.german_str:word_obj.english_str})
                except AttributeError:
                    try:
                        print({word_obj.german_str:word_obj.gender_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.gender_str})
                    except AttributeError:
                        print({word_obj.german_str:word_obj.plural_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.plural_str})
                show_answer(screen,word_obj)
            elif lives == 0: 
                life3.kill()
                try:
                    print({word_obj.german_str:word_obj.english_str})
                    #Needs a try except to catch the gender/plural cases here
                    missed_words.append({word_obj.german_str:word_obj.english_str})
                except AttributeError:
                    try:
                        print({word_obj.german_str:word_obj.gender_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.gender_str})
                    except AttributeError:
                        print({word_obj.german_str:word_obj.plural_str})
                        #Needs a try except to catch the gender/plural cases here
                        missed_words.append({word_obj.german_str:word_obj.plural_str})
                show_answer(screen,word_obj)
                lives = 3
                state['game1'] = 0
                gameover(state,screen)
                
        if word_status == False:
            gen_state+=1
            try:
                word_obj = next(generated_word)
            except StopIteration:
                gameover(state,screen,victory=True)

            
            
        #Text input
        block = font.render(text, True, (1,1,1))
        block_rect = block.get_rect()
        block_rect.centerx = inputbox_rect.centerx
        block_rect.centery = inputbox_rect.centery
        
        #Blits
        screen.fill((255,255,255))
        screen.blit(sky,sky_rect)
        screen.blit(inputbox,inputbox_rect)
        screen.blit(pause_button,pause_rect)
        screen.blit(block,block_rect)
        screen.blit(word_obj.word_display,  word_obj.word_display_rect)
        screen.blit(word_obj.word_block,    word_obj.word_rect)
        life_balloons.draw(screen)
        pygame.display.flip()

        ##User Input
        #Events

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pause_rect.collidepoint(pos):
                    state = paused(state,screen)
            elif event.type == KEYDOWN:
                ##Check Answer Event##
                if event.key == K_RETURN:
                    text = text.upper().strip()
                    
                    ##Normal word translations Events##
                    if word_choice == 'N' or word_choice == 'A' or word_choice == 'V' or word_choice == 'M':
                        check_list = [eng.upper() for eng in word_obj.english_str]
                        for counter,eng in enumerate(check_list):
                            if eng.startswith('TO '): 
                                text = text.replace('TO ','')
                                check_list[counter] = eng.replace('TO ','')
                            elif eng.startswith('THE '): 
                                text = text.replace('THE ','') 
                                check_list[counter] = eng.replace('THE ','')
                        if text in check_list:
                            score+=1
                            try:
                                word_obj = next(generated_word)
                            except StopIteration:
                                gameover(state,screen,victory=True)
                            text = ''
                        else:
                            text = ''
                    
                    ##Gender word events##
                    if word_choice == 'G':
                        check_list = word_obj.gender_str.upper()
                        if text in [check_list]:
                            score+=1
                            try:
                                word_obj = next(generated_word)
                            except StopIteration:
                                gameover(state,screen,victory=True)
                            text = ''
                        else:
                            text = ''
                            
                    ##Plural word events##
                    if word_choice == 'P':
                        check_list = [word_obj.plural_str.upper()]
                        for counter,plural in enumerate(check_list):
                            if plural.startswith('DIE '): 
                                text = text.replace('DIE ','')
                                check_list[counter] = plural.replace('DIE ','')
                        if text in check_list:
                            score+=1
                            try:
                                word_obj = next(generated_word)
                            except StopIteration:
                                gameover(state,screen,victory=True)
                            text = ''
                        else:
                            text = ''
                            
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key != K_BACKSPACE or event.key != K_RETURN:
                    text += event.unicode
            if event.type == pygame.QUIT:
                state['running'] = 0
                state['game1'] = 0
                pygame.quit()
                return state
        
    return state



    
    

    
    
    