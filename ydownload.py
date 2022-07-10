from tkinter import *   
import PIL.Image
import PIL.ImageTk

import os
import glob
import ffmpeg
import pytube


def DownloadSong(song):
    url= song.get()
    pytube.YouTube(url).streams.filter(progressive=True, file_extension='mp4').first().download('./out/')
    
    videotoaudio()
    complete()

def DownloadPlayList(playlist):
    url= playlist.get()

    for video in pytube.Playlist(url).videos:
        video.streams.filter(progressive=True, file_extension='mp4').first().download('./out/')
    videotoaudio()
    complete()

def videotoaudio():
    for file in os.listdir('./out/'):
        # check only text files
        if file.endswith('.mp4'):
            new = file[:-1]+'3'
            
            stream = ffmpeg.input('./out/'+file)
            stream = ffmpeg.output(stream,'./out/'+new)
            ffmpeg.run(stream)
            os.remove('./out/'+file)

def complete():
    child=Toplevel(window) # Child window
    child.title("Download Complete")
    child.config(width=200, height=100,bg="#9dcea4")
    child.resizable(False, False)
    text = Label(child, text="Download Complete",highlightthickness = 0, bd = 0, bg = "#9dcea4")
    text.place(x=25,y=30)
   
    ok_buton = Button(child,text="Ok",command=child.destroy,highlightthickness = 0, bd = 0, bg = "#18a662")
    ok_buton.place(x=75,y=60)



window = Tk()
window.title("Youtube Downloader")
window.config(width=500, height=300, bg="#9dcea4")
window.resizable(False, False)

img = PIL.Image.open("./icon.png")
img = img.resize((300, 100))
photo = PIL.ImageTk.PhotoImage(img)

canvas = Canvas(window,width=300, height=100,bg="#9dcea4",bd=0, highlightthickness=0, relief='ridge')
canvas.create_image(0, 0, image=photo, anchor=NW)
canvas.place(x=125, y=30)

song = StringVar()
playlist = StringVar()

song_entry = Entry(window,textvariable=song,width=35)
song_entry.place(x=20, y=150)

song_button = Button(text="Descargar Cancion",command= lambda: DownloadSong(song), bg="#18a662",highlightthickness = 0, bd = 0)
song_button.place(x=330, y=150)

playList_entry = Entry(window,textvariable=playlist, width=35)
playList_entry.place(x=20, y=200)

playlist_button = Button(text="Descargar PlayList",command= lambda: DownloadPlayList(playlist), bg="#18a662" ,highlightthickness = 0, bd = 0)
playlist_button.place(x=330, y=200)

exit_buton = Button(window,text="Salir",command=window.destroy,highlightthickness = 0, bd = 0, bg = "#d23c00")
exit_buton.place(x=250, y=250)

window.mainloop()
