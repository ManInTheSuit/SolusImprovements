#!/usr/bin/python3

# This script toggles UI appearance between day and night mode

import subprocess,os
from neovim import attach

HOME = '/home/supcom'
# Day themes
GTK_DAY = "Plata-Lumine-Compact"
NVIM_DAY = 'one'
KITTY_DAY = 'One Half Light'
ICONS_DAY = 'Papirus-Light'
CURSOR_DAY = 'volantes_light_cursors'

# Night themes
GTK_NIGHT = 'Gruvbox-Material-Dark'
NVIM_NIGHT = 'gruvbox-material'
KITTY_NIGHT = 'Gruvbox Dark'
ICONS_NIGHT = 'Papirus-Dark'
CURSOR_NIGHT = 'volantes_dark_cursors'


def toggle_gtk(day_mode):
    if day_mode:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','gtk-theme',f'"{GTK_NIGHT}"'])
    else:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','gtk-theme',f'"{GTK_DAY}"'])

def toggle_nvim(day_mode):
    lines=[]
    with open(f'{HOME}/.config/nvim/ui.vim', "r", encoding='utf-8') as file:
        lines = file.readlines()

    for i in range(0,len(lines)):
        if 'set background' in lines[i]:
            if day_mode:
                lines[i] = 'set background=dark\n'
            else:
                lines[i] = 'set background=light\n'

        if 'colorscheme' in lines[i]:
            if day_mode:
                lines[i] = f'colorscheme {NVIM_NIGHT}\n'
            else:
                lines[i] = f'colorscheme {NVIM_DAY}\n'

    with open(f'{HOME}/.config/nvim/ui.vim', "w", encoding='utf-8') as file:
        for line in lines:
           file.write(line)

    instances = []

    # get the content of /tmp
    directory_content = os.listdir('/tmp')
    for directory in directory_content:
        # check if it contains directories starting with nvim
        if directory.startswith('nvim'):
            # check if the nvim directories contains a socket
            dc = os.listdir('/tmp/' + directory)
            if '0' in dc:
                instances.append('/tmp/' + directory + '/0') 

    for instance in instances:
        # connect over the socker
        nvim = attach('socket', path=instance)

        # execute the reload command
        nvim.command(f'source {HOME}/.config/nvim/init.vim')

def toggle_kitty(day_mode):
    if day_mode:
        subprocess.run(['kitty','+kitten','themes','--reload-in=all',f'{KITTY_NIGHT}'])
    else:
        subprocess.run(['kitty','+kitten','themes','--reload-in=all',f'{KITTY_DAY}'])

def toggle_icons(day_mode):
    if day_mode:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','icon-theme',f'"{ICONS_NIGHT}"'])
    else:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','icon-theme',f'"{ICONS_DAY}"'])

def toggle_cursor(day_mode):
    if day_mode:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','cursor-theme',f'"{CURSOR_NIGHT}"'])
    else:
        subprocess.run(['gsettings','set','org.gnome.desktop.interface','cursor-theme',f'"{CURSOR_DAY}"'])


if __name__=="__main__":
    """ 
    Stuff to toggle:
        GTK system-wide theme
        Neovim theme
        Kitty theme 
        Icon theme
        Cursor theme
    """
    curr_gtk_theme = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], stdout=subprocess.PIPE).stdout.decode('UTF-8').replace("'","").strip()
    
    day_mode = (curr_gtk_theme==GTK_DAY)
    
    toggle_gtk(day_mode)
    toggle_nvim(day_mode)
    toggle_kitty(day_mode)
    toggle_icons(day_mode)
    toggle_cursor(day_mode)

