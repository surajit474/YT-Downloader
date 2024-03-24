import threading

import customtkinter as ctk
from PIL import Image
from pytube import YouTube
from pytube.cli import on_progress


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Youtube Downloader")
        self._set_appearance_mode("dark")

        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure((1, 2), weight=2, uniform="a")
        # for displaying image
        im = Image.open("download.png")
        im_ctk = ctk.CTkImage(light_image=im, dark_image=im)

        # creating widget
        self.frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")

        self.link = ctk.StringVar()
        ctk.CTkEntry(
            self.frame,
            textvariable=self.link,
        ).pack(pady=6, fill="x")

        t1=threading.Thread(target=self.Yt)
        ctk.CTkButton(
            self.frame,
            text="Download",
            fg_color="#348ceb",
            image=im_ctk,
            command=lambda:threading.Thread(target=self.Yt).start(),
        ).pack(pady=6)
        

        self.frame.grid(column=1, row=1, sticky="nsew")

        # menu frame

        self.menu_frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=0)
        self.menu_frame.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.menu_frame.rowconfigure(0, weight=1)

        # format selction
        self.format_list = ["720p", "480p", "360p", "240p", "144p"]
        self.format_var = ctk.StringVar(value="mp4")
        ctk.CTkOptionMenu(
            self.menu_frame,
            variable=self.format_var,
            values=["mp4", "mp3"],
            command=self.selection,
        ).grid(column=0, row=0, sticky="n")

        self.menu_frame.grid(column=0, row=0, columnspan=3, sticky="nesw")

        # resolution

        self.res_var = ctk.StringVar(value="720p")
        ctk.CTkOptionMenu(
            self.menu_frame,
            values=["720p", "480p", "360p", "240p", "144p"],
            variable=self.res_var,
        ).grid(column=1, row=0, sticky="n")

        ctk.CTkLabel(self.menu_frame, text="Resolution", text_color="white").grid(
            column=1, row=0
        )
        print(f"link:{self.link.get()}")

        self.mainloop()

    def Yt(self):
        # youtube
        try:
            self.yt = YouTube(self.link.get())
            if self.format_var.get() == "mp4":
                self.stream = self.yt.streams.filter(progressive=True)
                self.video = self.stream.get_by_resolution(self.res_var.get())

                lable2 = ctk.CTkLabel(
                    self.frame,
                    text=f"size: {(self.video.filesize_mb)} MB",
                    text_color="blue",
                )
                # self.video.on_progress(chunk=self.video.filesize,file_handler=self.video.)
                # lable2.pack()
                self.video.download(
                    filename=f"{self.yt.title}  {self.res_var.get()} .mp4"
                )
                self.after(4000, lambda: lable2.pack_forget())
            else:
                self.audio_stream = self.yt.streams.filter(
                    only_audio=True, abr=self.res_var.get()
                )
                self.audio = self.audio_stream.first()
                self.audio.download(
                    filename=f"{self.yt.title} {self.res_var.get()} .mp3"
                )
        except:
            lable1 = ctk.CTkLabel(
                self.frame, text="please enter a URL", text_color="red"
            )
            lable1.pack(pady=2)
            self.after(4000, lambda: lable1.pack_forget())

    def selection(self, f):

        if str(self.format_var.get()) == "mp4":
            self.res_var.set("720p")
            ctk.CTkOptionMenu(
                self.menu_frame,
                variable=self.res_var,
                values=["720p", "480p", "360p", "240p", "144p"],
            ).grid(column=1, row=0, sticky="n")

        else:
            self.res_var.set("160kbps")
            ctk.CTkOptionMenu(
                self.menu_frame,
                variable=self.res_var,
                values=["160kbps", "128kbps", "70kbps", "50kbps"],
            ).grid(column=1, row=0, sticky="n")


app = App()


# yt=YouTube('https://youtu.be/r_QyRJf3rtQ?si=2gfjDGFYdn8oGz_h')
# filter_stream=yt.streams.filter(only_audio=True)
# print(filter_stream)
