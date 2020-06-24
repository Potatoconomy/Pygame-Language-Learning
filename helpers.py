# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:23:22 2020

@author: Patrick
"""

#HELPERS
import xlrd
import sys
import os
import pygame
pygame.init()
main = os.getcwd()


_image_library = {}
def get_image(path,transformx=None,transformy=None,reload=None):
    global _image_library            
    try:
        image,image_rect = _image_library.get(path)
    except TypeError:
        image,image_rect = None,None
    if image == None or reload == True:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        if (transformx,transformy) != (None,None):
            image = pygame.transform.scale(image,(transformx,transformy))
        image_rect = image.get_rect()
        image.set_colorkey((255,255,255))
        _image_library[path] = (image,image_rect)

    return image,image_rect
    
 

def get_vocab():
    d = []
    fname = main + '\\vocab\\germanvocab.xlsx'
    xl_workbook = xlrd.open_workbook(fname)
    
    # grab the first sheet by index 
    # (sheets are zero-indexed)
    xl_sheet = xl_workbook.sheet_by_index(0)
    
    #iterating through rows and columns
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows, 0th is title
        col=0
        row_info = {'English':None,'German':None,'Type':None,'Difficulty':None}
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            if col_idx == 0:  row_info['German']     = cell_obj.value
            if col_idx == 1:  row_info['English']    = cell_obj.value 
            if col_idx == 2:  row_info['Type']       = cell_obj.value
            if col_idx == 3:  row_info['Difficulty'] = cell_obj.value
        
        #Fix entry syntax
        row_info = {k.strip(): v.strip() for k, v in row_info.items()}
        row_info = {k: v.split(',') for k, v in row_info.items()}
        row_info = {k.strip(): [v[i].strip() for i in range(len(v))] for k, v in row_info.items()}
        d.append(row_info)
    return d


def get_gender_vocab():
    d = []
    fname = main + '\\vocab\\germangenders.xlsx'
    xl_workbook = xlrd.open_workbook(fname)
    
    # grab the first sheet by index 
    # (sheets are zero-indexed)
    xl_sheet = xl_workbook.sheet_by_index(0)
    
    #iterating through rows and columns
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows, 0th is title
        col=0
        row_info = {'GermanNoun':None,'Gender':None}
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            if col_idx == 0:  row_info['GermanNoun']     = cell_obj.value
            if col_idx == 1:  row_info['Gender']    = cell_obj.value         
        #Fix entry syntax
        row_info = {k.strip(): v.strip() for k, v in row_info.items()}
        row_info = {k: v.split(',') for k, v in row_info.items()}
        row_info = {k.strip(): [v[i].strip() for i in range(len(v))] for k, v in row_info.items()}
        d.append(row_info)
    return d


def get_plural_vocab():
    d = []
    fname = main + '\\vocab\\germanplurals.xlsx'
    xl_workbook = xlrd.open_workbook(fname)
    
    # grab the first sheet by index 
    # (sheets are zero-indexed)
    xl_sheet = xl_workbook.sheet_by_index(0)
    
    #iterating through rows and columns
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(1, xl_sheet.nrows):    # Iterate through rows, 0th is title
        col=0
        row_info = {'GermanNoun':None,'Plural':None}
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            if col_idx == 0:  row_info['GermanNoun']     = cell_obj.value
            if col_idx == 1:  row_info['Plural']    = cell_obj.value         
        #Fix entry syntax
        row_info = {k.strip(): v.strip() for k, v in row_info.items()}
        row_info = {k: v.split(',') for k, v in row_info.items()}
        row_info = {k.strip(): [v[i].strip() for i in range(len(v))] for k, v in row_info.items()}
        d.append(row_info)
    return d

def save_diff(diff):
    with open(main + '\\states\\difficulty.txt','w') as f:
        for k,v in diff.items():
            if v:
                f.write(k)

def save_word_choice(choice):
    with open(main + '\\states\\word_choice.txt','w') as f:
        for k,v in choice.items():
            if v:
                f.write(k)

def save_player(choice):
    with open(main + '\\states\\user.txt','w') as f:
        for k,v in choice.items():
            if v:
                f.write(k)
                
                
def dborder_state_definer(border_state,sprite):
    border_state = dict.fromkeys(border_state, 0)
    if sprite.path   ==  main+'\\sprites\\easy_arrow.png':      border_state['E']    = 1
    elif sprite.path ==  main+'\\sprites\\medium_arrow.png':    border_state['M']     = 1
    elif sprite.path ==  main+'\\sprites\\hard_arrow.png':      border_state['H']    = 1
    save_diff(border_state)
    return border_state

def wborder_state_definer(border_state,sprite):
    border_state = dict.fromkeys(border_state, 0)
    if sprite.path ==  main+'\\sprites\\verbs_arrow.png':       border_state['V']   = 1
    elif sprite.path ==  main+'\\sprites\\adjectives_arrow.png':border_state['A']    = 1
    elif sprite.path ==  main+'\\sprites\\nouns_arrow.png':     border_state['N']   = 1
    elif sprite.path ==  main+'\\sprites\\plurals_arrow.png':   border_state['P'] = 1
    elif sprite.path ==  main+'\\sprites\\genders_arrow.png':   border_state['G'] = 1
    elif sprite.path ==  main+'\\sprites\\mixed_arrow.png':     border_state['M']   = 1
    save_word_choice(border_state)
    return border_state

def uborder_state_definer(border_state,sprite):
    border_state = dict.fromkeys(border_state, 0)
    if sprite.path   == main+'\\sprites\\player1.png': border_state['player1'] = 1
    elif sprite.path == main+'\\sprites\\player2.png': border_state['player2'] = 1
    save_player(border_state)
    return border_state
    