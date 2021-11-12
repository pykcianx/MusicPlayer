import os
from tkinter import *
from tkinter import filedialog
import pygame
import os
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('AudioPlayer')
root.iconbitmap('mp3player\\mp3.ico')
root.geometry('470x600')
root.resizable(width=0, height=0)

pygame.mixer.init()


def add_song():
    song = filedialog.askopenfilename(title="Wybierz plik", filetypes=(("mp3 Files", "*.mp3"),("wav Files", "*.wav")))
    song_list.insert(END, song)

def add_songs():
    songs = filedialog.askopenfilenames(title="Wybierz pliki", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song_list.insert(END, song)

def play():
    global stopped
    stopped = False

    music_slider.config(value=0)

    song_to_play = song_list.get(ACTIVE)

    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0)

    play_time()

    current_volume = pygame.mixer.music.get_volume()
    volume_label.config(text=current_volume * 100)



global stopped
stopped = False
def stop():
    song_status.config(text='')
    music_slider.config(value=0)

    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    song_status.config(text='')

    global stopped
    stopped = True



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
    song_status.config(text='')
    music_slider.config(value=0)

    current_song = song_list.curselection()
    next_one = current_song[0]+1
    song = song_list.get(next_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one, last=None)

def previous_song():
    song_status.config(text='')
    music_slider.config(value=0)

    current_song = song_list.curselection()
    previous_one = current_song[0]-1
    song = song_list.get(previous_one)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    song_list.selection_clear(0, END)
    song_list.activate(previous_one)
    song_list.selection_set(previous_one, last=None)

def play_time():
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() / 1000
    clock_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    song = song_list.get(ACTIVE)
    load_song = MP3(song)

    global song_length
    song_length = load_song.info.length
    clock_time_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time +=1
    if int(music_slider.get()) == int(song_length):
        song_status.config(text=f'Upłynęło: {clock_time_length}')
        next_song()

    elif paused:
        pass

    elif int(music_slider.get()) == int(current_time):
        slider_position = int(song_length)
        music_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        music_slider.config(to=slider_position, value=int(music_slider.get()))
        clock_time = time.strftime('%H:%M:%S', time.gmtime(int(music_slider.get())))
        song_status.config(text=f'Upłynęło: {clock_time}  z  {clock_time_length}  ')
        next_time = int(music_slider.get()) + 1
        music_slider.config(value=next_time)


    song_status.after(1000, play_time)

def del_song():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()

def del_songs():
    stop()
    song_list.delete(0, END)
    pygame.mixer.music.stop()

def slide(x):
    song_to_play = song_list.get(ACTIVE)

    pygame.mixer.music.load(song_to_play)
    pygame.mixer.music.play(loops=0, start=int(music_slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    volume_label.config(text=current_volume * 100)



master_frame = Frame(root)
master_frame.pack(pady=20)

#SONG_LIST
song_list = Listbox(master_frame, bg="black", fg="green", width=60, height=25, selectbackground="#e56353", selectforeground="white", background="#313131", foreground="white")
song_list.grid(row=0, column=0)

#CONTROL BTNS
#BTN_IMAGES
back_btn_img = PhotoImage(file="mp3player\\back.png")
forward_btn_img = PhotoImage(file="mp3player\\forward.png")
play_btn_img = PhotoImage(file="mp3player\\play.png")
pause_btn_img = PhotoImage(file="mp3player\\pause.png")
stop_btn_img = PhotoImage(file="mp3player\\stop.png")

#BTN_FRAME
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0)

volume_frame = LabelFrame(master_frame, text="Głośność")
volume_frame.grid(row=0, column=1, padx=10)

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
song_status.pack(fill=X, side=BOTTOM, ipady=0)

#SLIDERS
music_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
music_slider.grid(row=3, column=0, pady=20)

volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

volume_label = Label(volume_frame, text="0")
volume_label.pack(pady=10)

#MENU
my_menu = Menu(root)
root.config(menu=my_menu)

#ADD_SONGS_MENU
add_song_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label="Plik", menu=add_song_menu)
add_song_menu.add_command(label="Dodaj plik audio", command=add_song)
#ADD_MANY_SONGS
add_song_menu.add_command(label="Dodaj wiele plików audio", command=add_songs)
add_song_menu.add_command(label = "_________________________________")
add_song_menu.add_command(label = "Zamknij program", command = root.destroy)
#DELETE_SONG_MENU
remove_song_menu = Menu(my_menu, tearoff = False)
my_menu.add_cascade(label="Edycja", menu=remove_song_menu)
remove_song_menu.add_command(label="Usuń piosenkę", command=del_song)
remove_song_menu.add_command(label="Usuń wszystkie piosenki", command=del_songs)


root.mainloop()

