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


#ADD_SONG_FUNC
def add_song():
    song = filedialog.askopenfilename(title="Wybierz plik", filetypes=(("mp3 Files", "*.mp3"),))

    #dict = {"song": "os.path.basename(song)"}

    #song_name = os.path.basename(song)
    song_list.insert(END, song)

    #python add file to dict or add path to dict and getfilename

#ADD_MANY_SONGS
def add_songs():
    songs = filedialog.askopenfilenames(title="Wybierz pliki", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song_list.insert(END, song)

#PLAY_SONG
def play():
    song_to_play = song_list.get(ACTIVE)

    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0)

    play_time()

    #update slider
    #slider_position = int(song_length)
    #music_slider.config(to=slider_position, value=0)

#STOP_SONG
def stop():
    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    song_status.config(text='')

global paused
paused = False

#PAUSE_SONG
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#PLAY_NEXT_SONG
def next_song():
    current_song = song_list.curselection()
    next_one = current_song[0]+1
    song = song_list.get(next_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #MOVE_ACTIVE_BAR
    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one, last=None)

#PLAY_PREVIOUS_SONG
def previous_song():
    current_song = song_list.curselection()
    previous_one = current_song[0]-1
    song = song_list.get(previous_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #MOVE_ACTIVE_BAR
    song_list.selection_clear(0, END)
    song_list.activate(previous_one)
    song_list.selection_set(previous_one, last=None)

#SONG_TIME
def play_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    clock_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    slider_label.config(text=f'Slider: {int(music_slider.get())} and Song Pos: {int(current_time)}')

    current_song = song_list.curselection()
    song = song_list.get(current_song)
    load_song = MP3(song)

    global song_length
    song_length = load_song.info.length
    clock_time_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    song_status.config(text=f'Upłynęło: {clock_time}  z  {clock_time_length}  ')
    #update slider position to song position
    music_slider.config(value=current_time)

    slider_position = int(song_length)
    current_time +=1
    music_slider.config(to=slider_position, value=int(current_time))

    #updating time every 1000ms
    song_status.after(1000, play_time)

#DELETE_SONG
def del_song():
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()

#DELETE_SONGS
def del_songs():
    song_list.delete(0, END)
    pygame.mixer.music.stop()

def slide(x):
    #slider_label.config(text=f'{int(music_slider.get())} of {int(song_length)}')
    song_to_play = song_list.get(ACTIVE)

    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0, start=int(music_slider.get()))


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

#STATUS_BAR
song_status = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
song_status.pack(fill=X, side=BOTTOM, ipady=2)

#SLIDER
music_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
music_slider.pack(pady=40)

slider_label = Label(root, text="0")
slider_label.pack(pady=10)


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

