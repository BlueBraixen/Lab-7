#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 16:06:54 2023

@author: NP
"""
import pgzrun
import pygame
import pgzero
import random
from pgzero.builtins import Actor
from random import randint
import math
import pgzero.clock

#Constants
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y) 
FONT_COLOR = (0, 0, 0)
EGG_TARGET = 150
HERO_START = (200, 200) 
HERO2_START = (200, 400) 
ATTACK_DISTANCE = 200 
DRAGON_WAKE_TIME = 2 
EGG_HIDE_TIME = 2 
MOVE_DISTANCE = 5

#Variables
lives = 15
eggs_collected = 0
game_over = False
game_complete = False
reset_required = False

#Dragon with one egg

easy_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 100)), 
    "eggs": Actor("one-egg", pos=(400, 100)), 
    "egg_count": 1,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 10,
    "sleep_counter": 0,
    "wake_counter": 0
}
#Dragon with two eggs
medium_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 300)), 
    "eggs": Actor("two-eggs", pos=(400, 300)), 
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 7,
    "sleep_counter": 0,
    "wake_counter": 0
}
#Dragon with three eggs
hard_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    "eggs": Actor("three-eggs", pos=(400, 500)),
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 4,
    "sleep_counter": 0,
    "wake_counter": 0
}
# Sets up initial positions
lairs = [easy_lair, medium_lair, hard_lair] 
hero = Actor("hero", pos=HERO_START)
hero2 = Actor("hero2", pos=HERO2_START)


#Sets up characters and elements
def draw():
    global lairs, eggs_collected, lives, game_complete 
    screen.clear()
    screen.blit("dungeon", (0, 0))
    if game_over:
        screen.draw.text("GAME OVER!", fontsize=60, center=CENTER, color=FONT_COLOR) 
    elif game_complete:
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR) 
    else:
        hero.draw()
        hero2.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)

#Adds new eggs 
def draw_lairs(lairs_to_draw): 
    for lair in lairs_to_draw:
        lair["dragon"].draw()
        if lair["egg_hidden"] is False:
            lair["eggs"].draw()
def draw_counters(eggs_collected, lives): 
    screen.blit("egg-count", (0, HEIGHT - 30)) 
    screen.draw.text(str(eggs_collected),
                     fontsize=40,
                     pos=(30, HEIGHT - 30),
                     color=FONT_COLOR)
    screen.blit("life-count", (80, HEIGHT - 30)) 
    screen.draw.text(str(lives),
                     fontsize=40,
                     pos=(110, HEIGHT - 30),
                     color=FONT_COLOR)
    screen.draw.text(str(lives), fontsize=40,
                     pos=(110, HEIGHT - 30),
                     color=FONT_COLOR)

#Moves characters and sees if they get hit.
def update():
    if keyboard.right:
        hero.x += MOVE_DISTANCE 
        if hero.x > WIDTH:
            hero.x = WIDTH 
    elif keyboard.left:
        hero.x -= MOVE_DISTANCE 
        if hero.x < 0:
            hero.x = 0
    elif keyboard.down:
        hero.y += MOVE_DISTANCE
        if hero.y > HEIGHT:
            hero.y = HEIGHT
    elif keyboard.up:
        hero.y -= MOVE_DISTANCE 
        if hero.y < 0:
            hero.y = 0
    if keyboard.d:
        hero2.x += MOVE_DISTANCE 
        if hero2.x > WIDTH:
            hero2.x = WIDTH 
    elif keyboard.a:
        hero2.x -= MOVE_DISTANCE 
        if hero2.x < 0:
            hero2.x = 0
    elif keyboard.s:
        hero2.y += MOVE_DISTANCE
        if hero2.y > HEIGHT:
            hero2.y = HEIGHT
    elif keyboard.w:
        hero2.y -= MOVE_DISTANCE 
        if hero2.y < 0:
            hero.y = 0
    check_for_collisions()
    
    #Allows Dragons to wake up
def update_lairs():
    global lairs, hero, hero2, lives 
    for lair in lairs:
        if lair["dragon"].image == "dragon-asleep":
            update_sleeping_dragon(lair)
        elif lair["dragon"].image == "dragon-awake": 
            update_waking_dragon(lair)
        update_egg(lair)
        
        #Checks time
clock.schedule_interval(update_lairs, 1)

#Determines if dragon should wake up
def update_sleeping_dragon(lair):
    if lair["sleep_counter"] >= lair["sleep_length"]:
        if random.choice([True, False]):
            lair["dragon"].image = "dragon-awake"
            lair["sleep_counter"] = 0
    else:
        lair["sleep_counter"] += 1
        
        #Determines if dragon should go to sleep
def update_waking_dragon(lair):
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:
        if random.choice([True, False]):
            lair["dragon"].image = "dragon-asleep"
            lair["wake_counter"] = 0
    else:
        lair["wake_counter"] += 1
#Places Egg
def update_egg(lair):
    if lair["egg_hidden"] is True:
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:
            lair["egg_hidden"] = False
            lair["egg_hide_counter"] = 0 
        else:
            lair["egg_hide_counter"] += 1
#Determines if player gets eggs
def check_for_collisions():
    global lairs, eggs_collected, lives, reset_required, game_complete 
    for lair in lairs:
        if lair["egg_hidden"] is False: check_for_egg_collision(lair)
        if lair["dragon"].image == "dragon-awake" and reset_required is False: 
            check_for_dragon_collision(lair)
            #Determines if player gets hit
def check_for_dragon_collision(lair):
    x_distance = hero.x - lair["dragon"].x 
    y_distance = hero.y - lair["dragon"].y 
    distance = math.hypot(x_distance, y_distance) 
    if distance < ATTACK_DISTANCE:
        handle_dragon_collision1()
    x_distance2 = hero2.x - lair["dragon"].x 
    y_distance2 = hero.y - lair["dragon"].y 
    distance2 = math.hypot(x_distance2, y_distance2) 
    if distance2 < ATTACK_DISTANCE:
        handle_dragon_collision2()
        
#Moves Character 1 back
def handle_dragon_collision1():
    global reset_required
    reset_required = True
    animate(hero, pos=HERO_START, on_finished=subtract_life)
    
#Moves Character 2 back
def handle_dragon_collision2():
    global reset_required
    reset_required = True

    animate(hero2, pos=HERO2_START, on_finished=subtract_life)

#Counts eggs
    
def check_for_egg_collision(lair): 
    global eggs_collected, game_complete 
    if hero.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True 
        eggs_collected += lair["egg_count"] 
    if hero2.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True 
        eggs_collected += lair["egg_count"] 
        if eggs_collected >= EGG_TARGET:
            game_complete = True
#Drains life counter
def subtract_life():
    global lives, reset_required, game_over 
    lives -= 1
    if lives == 0:
        game_over = True
    reset_required = False
    
    
pgzrun.go()