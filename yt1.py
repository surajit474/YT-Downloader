import multiprocessing
import threading

import customtkinter as ctk
from PIL import Image
from pytube import YouTube


class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#242424", corner_radius=0)
        # creating grid
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure(0, weight=1)

        # file format selction
        self.format_list = ["720p", "480p", "360p", "240p", "144p"]

        self.format = ctk.CTkOptionMenu(
            self,
            variable=format_var,
            values=["mp4", "mp3"],
            command=lambda a: self.selection(parent),
        )
        self.format.grid(column=0, row=0, sticky="n")

        # resolution

        self.resolution = ctk.CTkOptionMenu(
            self,
            values=["720p", "480p", "360p", "240p", "144p"],
            variable=res_var,
        )
        self.resolution.grid(column=1, row=0, sticky="n")

        ctk.CTkLabel(self, text="Resolution", text_color="white").grid(column=1, row=0)

    def selection(self, parent):

        if str(format_var.get()) == "mp4":
            res_var.set("720p")
            ctk.CTkOptionMenu(
                self,
                variable=res_var,
                values=["720p", "480p", "360p", "240p", "144p"],
            ).grid(column=1, row=0, sticky="n")

        else:
            res_var.set("160kbps")
            ctk.CTkOptionMenu(
                self,
                variable=res_var,
                values=["160kbps", "128kbps", "70kbps", "50kbps"],
            ).grid(column=1, row=0, sticky="n")


class Yt(YouTube):
    def __init__(self, link):
        super().__init__(link, on_progress_callback=Progress)
        try:
            if format_var.get() == "mp4":
                self.stream = self.streams.filter(progressive=True)
                self.video = self.stream.get_by_resolution(res_var.get())

                # lable2 = ctk.CTkLabel(
                #     parent.frame,
                #     text=f"size: {(self.video.filesize_mb)} MB",
                #     text_color="blue",
                # )
                # self.video.on_progress(chunk=self.video.filesize,file_handler=self.video.)
                # lable2.pack()
                self.video.download(filename=f"{self.title}  {res_var.get()} .mp4")

                # parent.after(4000, lambda: lable2.pack_forget())
            else:
                self.audio_stream = self.streams.filter(
                    only_audio=True, abr=res_var.get()
                )
                self.audio = self.audio_stream.first()
                self.audio.download(filename=f"{self.title} {res_var.get()} .mp3")

        except:
            print("Error!")
            # lable1 = ctk.CTkLabel(
            #     parent.frame, text="Download Error", text_color="red"
            # )
            # lable1.pack(pady=2)
            # parent.after(4000, lambda: lable1.pack_forget())


class Progress:
    def __init__(self, video_stream, total_size, bytes_remaining):
        total_size = video_stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = (bytes_downloaded / total_size) * 100
        print(
            "\r"
            + "▌" * int(percent)
            + " " * (100 - int(percent))
            + " {}%".format(int(percent)),
            end="",
        )


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Youtube Downloader")
        self._set_appearance_mode("dark")
        global format_var, res_var
        format_var = ctk.StringVar(value="mp4")
        res_var = ctk.StringVar(value="720p")

        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure((1, 2), weight=2, uniform="a")
        # for displaying image
        im = Image.open("download.png")
        im_ctk = ctk.CTkImage(light_image=im, dark_image=im)

        # creating frame
        self.frame = ctk.CTkFrame(self, bg_color="#242424", fg_color="#242424")
        # link entry
        self.link = ctk.StringVar()
        ctk.CTkEntry(
            self.frame,
            textvariable=self.link,
        ).pack(pady=6, fill="x")
        # Download button

        self.frame.grid(column=1, row=1, sticky="nsew")
        im_ctk = ctk.CTkImage(light_image=im, dark_image=im)
        # creating variables

        menu = Menu(self)
        menu.grid(column=0, row=0, columnspan=3, sticky="nesw")

        ctk.CTkButton(
            self.frame,
            text="Download",
            fg_color="#348ceb",
            image=im_ctk,
            command=lambda:threading.Thread(target=lambda:Yt(self.link.get())).start(),
        ).pack(pady=6)

        self.mainloop()


app = App()
