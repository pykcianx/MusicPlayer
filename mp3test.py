import os
from tkinter import *
from tkinter import filedialog
import pygame
import os
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('mp3app')
root.iconbitmap('mp3player\\mp3.ico')
root.geometry('500x450')

pygame.mixer.init()

file_dict = {}

def add_song():
    song = filedialog.askopenfilename(title="Wybierz plik", filetypes=(("mp3 Files", "*.mp3"),))
    for key in file_dict:
        file_dict['key'].append(song)

    song_list.insert(END, file_dict.keys)


def add_songs():
    songs = filedialog.askopenfilenames(title="Wybierz pliki", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song_list.insert(END, song)

def play():
    song_to_play = song_list.get(ACTIVE)

    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0)


def stop():
    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)


global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    current_song = song_list.curselection()
    next_one = current_song[0]+1
    song = song_list.get(next_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one, last=None)

def previous_song():
    current_song = song_list.curselection()
    previous_one = current_song[0]-1
    song = song_list.get(previous_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    song_list.selection_clear(0, END)
    song_list.activate(previous_one)
    song_list.selection_set(previous_one, last=None)


def del_song():
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()

def del_songs():
    song_list.delete(0, END)
    pygame.mixer.music.stop()



#SONG_LIST
song_list = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_list.pack(pady=20)

#CONTROL BTNS
#BTN_IMAGES
back_btn_img = PhotoImage(file="mp3player\\backward_btn.png")
forward_btn_img = PhotoImage(file="mp3player\\forward_btn.png")
play_btn_img = PhotoImage(file="mp3player\\play_btn.png")
pause_btn_img = PhotoImage(file="mp3player\\pause_btn.png")
stop_btn_img = PhotoImage(file="mp3player\\stop_btn.png")
#BTN_FRAME
controls_frame = Frame(root)
controls_frame.pack()
#BUTTONS
back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command = previous_song)
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command = next_song)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command = lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)
#BTN_LOCATION
back_btn.grid(row=0, column=0, padx=5)
forward_btn.grid(row=0, column=1, padx=5)
play_btn.grid(row=0, column=2, padx=5)
pause_btn.grid(row=0, column=3, padx=5)
stop_btn.grid(row=0, column=4, padx=5)


#MENU
my_menu = Menu(root)
root.config(menu=my_menu)

#ADD_SONGS_MENU
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Plik", menu=add_song_menu)
add_song_menu.add_command(label="Dodaj plik audio", command=add_song)
#ADD_MANY_SONGS
add_song_menu.add_command(label="Dodaj wiele plików audio", command=add_songs)
#DELETE_SONG_MENU
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Edycja", menu=remove_song_menu)
remove_song_menu.add_command(label="Usuń piosenkę", command=del_song)
remove_song_menu.add_command(label="Usuń wszystkie piosenki", command=del_songs)


root.mainloop()

