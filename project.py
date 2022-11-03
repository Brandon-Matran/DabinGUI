from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from buttons import dates
import pygame
import webbrowser
from os import listdir
import customtkinter
from PIL import Image, ImageTk

#Create our main window
root = Tk()
root.title('Dabin Fan Page')
#Create a window that fits entire screen and is resizeable

root.geometry("1451x749")
root['background']='#E3E3D7'
root.resizable(True, True)


#Icon
root.iconbitmap('./images/sun.ico')

background = PhotoImage(file="images/DabinPiano.png")
bg_label = Label(root, image=background)
bg_label.place(x=0, y=0)

#Pick a theme
style = Style()
style.theme_use('clam')
style.configure("Treeview",
    background='#E3E3D7',
    foreground='black',
    fieldbackground='#E3E3D7'
)
event_label = Label(root, text='Tour Dates', font=("Arial Black", 18, "bold"), background='#E3E3D7')
event_label.pack(anchor=NW, padx= 100)
events = Treeview(root)

#Define our columns
events['columns'] = ('Month', 'Date', 'Location')

#Format column
events.column("#0", width=0, stretch=NO)
events.column("Month",anchor=W, width=80)
events.column("Date", anchor=CENTER, width=80)
events.column("Location", anchor=E, width=150)

#Headings
events.heading("#0", text="Label", anchor=W)
events.heading("Month", text="Month", anchor=CENTER)
events.heading("Date", text="Day", anchor=CENTER)
events.heading("Location", text="Location", anchor=CENTER)

# #Data
# events.insert(parent="",index='end', iid=0, text="", values=("Test"))
events.insert(parent="",index='end', iid=0, text="", values=(dates[0]))
events.insert(parent="",index='end', iid=1, text="", values=(dates[1]))
events.insert(parent="",index='end', iid=2, text="", values=(dates[2]))
events.insert(parent="",index='end', iid=3, text="", values=(dates[3]))
events.pack(anchor=NW)

# print(insert_into_playlist)
pygame.mixer.init()

# get list of files
playlist = listdir('./Music')
active_playlist = playlist
shuffled_playlist = []

# Get number of files
file_range = len(playlist) - 1

# Settings variables used to control play logic
music_option = True
shuffle_music = False
indexed_track = 0
display_track = indexed_track + 1
is_stopped = True
is_paused = False
is_started = False
repeat_track = False
repeat_all = False


# Updates the display values of the current track number and name
def update_display():
    global display_track
    display_track = playlist.index(active_playlist.__getitem__(indexed_track)) + 1
    # track_num_display.config(text=f"Track: {display_track}")
    track_name_display.config(text=f"Now Playing:\n{active_playlist.__getitem__(indexed_track)}")


# Logic to run music
def start_music():
    global indexed_track, is_started, is_stopped, active_playlist

    # Determine if random or normal play
    if shuffle_music:
        active_playlist = shuffled_playlist
    else:
        active_playlist = playlist

    # If music is not already playing, it has not been stopped or paused then grabs next song in queue
    while not pygame.mixer.music.get_busy() and not is_stopped and not is_paused and not is_started:
        pygame.mixer.music.load(f"./Music/{active_playlist.__getitem__(indexed_track)}")
        pygame.mixer.music.play()
        is_started = True
    # While music is playing check every 100 milliseconds if music track has finished playing and re-trigger music.
    if pygame.mixer.music.get_busy():
        window.after(100, start_music)
    else:
        # Repeat logic
        if not is_stopped and not is_paused:
            # If not repeating then at last track trigger stop
            if not repeat_all and not repeat_track and indexed_track == file_range:
                stop_music()

            # Repeat one logic reduce index call by 1 prior to adding 1 so always stay on same track
            elif repeat_track:
                indexed_track -= 1

            # Else it is repeating all
            indexed_track += 1
            is_started = False

            # Checks to make sure track is not skipped past last song or into negative.
            if indexed_track < 0 or indexed_track > file_range:
                indexed_track = 0

            # Update the display with current track info
            update_display()

            # Repeat music
            start_music()


# Gets the current status of the music player
def music_status():
    music_yes = pygame.mixer.music.get_busy()
    return music_yes


# Stop the music from playing. If already stopped then it resets repeat status and the playlist
def stop_music():
    global is_stopped, is_started, indexed_track, repeat_all, repeat_track
    if is_stopped:
        indexed_track = 0
        repeat_all = False
        repeat_track = False
        update_display()
    pygame.mixer.music.stop()
    is_stopped = True
    is_started = False
    start_music()


# Skip to next track
def next_track():
    global indexed_track, is_started
    # If music is playing stop it and move it to the next track and start again
    music_playing = music_status()
    if music_playing:
        pygame.mixer.music.stop()
        if indexed_track == file_range:
            indexed_track = 0
            is_started = False
        start_music()

    # If music is not playing move to next track and if on last track move to first
    else:
        if indexed_track != file_range:
            indexed_track += 1
        else:
            indexed_track = 0
    update_display()


# Skip to last track
def prev_track():
    global indexed_track, is_started
    # If music is playing stop it move to prior track or if on first track move to last track.
    music_playing = music_status()
    if music_playing:
        if display_track == 1:
            indexed_track = file_range
            is_started = False
        else:
            indexed_track -= 2
        pygame.mixer.music.stop()
        start_music()

    # If music is not playing skip back one, if on first track move to last track
    else:
        if indexed_track != 0:
            indexed_track -= 1
        else:
            indexed_track = file_range
    update_display()


# Play or pause logic
def play_track():
    global is_paused, is_stopped
    music_playing = music_status()
    # If music is playing then pause it and mark the paused flag as True
    if music_playing:
        is_paused = True
        pygame.mixer.music.pause()

    # Else it was paused so unpause and mark paused flag as False
    else:
        is_paused = False
        pygame.mixer.music.unpause()

    # Mark stopped as False and start music
    is_stopped = False
    start_music()



# Control buttons
start_pause = Frame(root)
start_pause.pack(side=BOTTOM)
previous_button = Button(start_pause,text="⏮ Back", command=prev_track)
previous_button.pack(side=LEFT)
stop_button = Button(start_pause, text="⏹ Stop", command=stop_music)
stop_button.pack(side=LEFT)
start_button = Button(start_pause, text="⏯ Play", command=play_track)
start_button.pack(side=LEFT)
next_button = Button(start_pause, text="⏭ Next", command=next_track)
next_button.pack(side=LEFT)
# repeat_button = Button(start_pause, text="🔄", command=repeat_loop)
# repeat_button.pack(side=LEFT)

# Displayed information

# track_num_display = Label(text=f"Track: {display_track}")
track_name_display = Label(text=f"Now Playing:\n{active_playlist.__getitem__(indexed_track)}")
# track_num_display.pack(side=BOTTOM)
track_name_display.pack(side=BOTTOM)


start_pause = Frame(root)
start_pause.pack(side=BOTTOM)

def openNewWindow():
    #Toplevel object which creates a new window
    newWindow = Toplevel()
    #Create a title for the new window
    newWindow.title("Tour Dates")
    #Size of geometry
    newWindow.geometry("500x500")
    newWindow['background']='#d1d5e7'
    T = Text(newWindow, height=50, width=52, font="Arial", background='#d1d5e7')

    l = Label(newWindow, text = "About Dabin", background='#d1d5e7')
    l.config(font = ("Arial Black", 20, "bold"))

    Fact = "Dabin is a JUNO nominated music producer & instrumentalist originally from Toronto. \n \nHaving spent his teens learning to play the piano, drums and guitar, Dabin started producing electronic music in 2011. \n \n Dabin has gained hundreds of millions of plays while refining his musical style into what it is today. \n His work includes high profile collaborations with Seven Lions, Slander, Said The Sky and remixes for Illenium & Gramatik. \n \n He released his sophomore album ”Wild Youth” in March 2019 via MrSuicideSheep’s label, Seeking Blue, which he then stripped down into an acoustic EP in 2020. \n \n Dabin distinguishes himself with a unique genre-defying live show in which he incorporates electronic guitar, synthesizers and drum pads."

    l.pack()
    T.pack()

    T.insert(END, Fact)

    # Download Icon and Button
    def downloadData():
        showinfo(
        title='Data',
        message='Downloading...'
    )

    download_button = Button(
        newWindow,
        text="Download Data",
        command=downloadData)

    download_button.pack(
        ipadx=5,
        ipady=5,
        expand=True
    )




Tour_button = customtkinter.CTkButton(root, text="Biography", fg_color='#D7E3DD', command=openNewWindow)
Tour_button.place(x=500)


vid_1 = customtkinter.CTkButton(text="Merch Store", fg_color='#E3E3EE',
                   command=lambda: webbrowser.open("https://dabinmusic.com/collections/all-merch"))
vid_1.place(x=750)

vid_2 = customtkinter.CTkButton(root, text="Dabin EDC 2018",fg_color='#E3D7E3', command=lambda: webbrowser.open("https://www.youtube.com/watch?v=gxH3_2uS3DA"))
vid_2.place(x=1000)



root.mainloop()
