import sys
import os

# Vendored Pillow: cari paket di ./libs dulu
BASE_DIR = os.path.dirname(__file__)
VENDOR_DIR = os.path.join(BASE_DIR, "libs")
if os.path.isdir(VENDOR_DIR) and VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import shutil
import platform

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.base_path     = os.getcwd()
        self.pictures_path = os.path.join(self.base_path, "Pictures")
        self.sorter_path   = os.path.join(self.base_path, "Sorter")

        # window title & icon
        self.root.title("Image Sorter")
        try:
            icon_file = os.path.join(self.base_path, "icon.png")
            icon_img  = ImageTk.PhotoImage(file=icon_file)
            self.root.iconphoto(True, icon_img)
        except Exception:
            pass

        # maximize window
        if platform.system() == "Windows":
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)

        # ensure on top briefly
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        # 1) setup directories
        self.check_directories()
        # if user cancelled creating Pictures folder, quit __init__
        if not os.path.exists(self.pictures_path):
            return

        # 2) load images
        self.image_files = [
            f for f in os.listdir(self.pictures_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"))
        ]
        self.current_index = 0

        # 3) setup UI
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        self.load_folders()

        self.progress = ttk.Progressbar(self.root,
                                        orient="horizontal",
                                        length=300,
                                        mode="determinate")
        self.progress.pack(pady=5)

        # 4) show first image
        self.show_image()

        # 5) key bindings
        for i in range(9):
            self.root.bind(f"<Key-{i+1}>",
                           lambda e, num=i: self.move_image_by_shortcut(num))
        self.root.bind("<Left>",   self.prev_image)
        self.root.bind("<Right>",  self.next_image)
        self.root.bind("<Return>", self.select_folder)
        self.root.bind("<Escape>", self.skip_image)

    def check_directories(self):
        if not os.path.exists(self.pictures_path):
            create = messagebox.askyesno(
                "Folder Tidak Ditemukan",
                "'Pictures' folder tidak ditemukan. Buat sekarang?",
                parent=self.root
            )
            if create:
                os.mkdir(self.pictures_path)
            else:
                self.root.destroy()
                return

        if not os.path.exists(self.sorter_path):
            os.mkdir(self.sorter_path)

        subdirs = [
            d for d in os.listdir(self.sorter_path)
            if os.path.isdir(os.path.join(self.sorter_path, d))
        ]
        if not subdirs:
            self.create_sorter_folders()

    def create_sorter_folders(self):
        try:
            jumlah = simpledialog.askinteger(
                "Input",
                "Masukkan jumlah folder kategori (maks 9):",
                parent=self.root, minvalue=1, maxvalue=9
            )
            if jumlah is None:
                messagebox.showinfo("Batal",
                                    "Pembuatan folder dibatalkan.",
                                    parent=self.root)
                self.root.destroy()
                return

            for i in range(1, jumlah + 1):
                nama = simpledialog.askstring(
                    "Nama Folder",
                    f"Masukkan nama untuk kategori ke-{i}:",
                    parent=self.root
                )
                if not nama or not nama.strip():
                    messagebox.showerror(
                        "Error",
                        "Nama folder tidak boleh kosong.",
                        parent=self.root
                    )
                    self.root.destroy()
                    return
                os.mkdir(os.path.join(self.sorter_path, nama.strip()))
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)
            self.root.destroy()

    def load_folders(self):
        for w in self.button_frame.winfo_children():
            w.destroy()

        self.folder_list = [
            d for d in os.listdir(self.sorter_path)
            if os.path.isdir(os.path.join(self.sorter_path, d))
        ]
        for i, folder in enumerate(self.folder_list):
            btn = tk.Button(
                self.button_frame,
                text=f"{i+1}. {folder}",
                command=lambda f=folder: self.move_image(f)
            )
            btn.pack(side=tk.LEFT, padx=5)

        skip_btn = tk.Button(
            self.button_frame,
            text="Skip",
            bg="orange",
            command=self.skip_image
        )
        skip_btn.pack(side=tk.LEFT, padx=5)

    def show_image(self):
        if not self.root.winfo_exists():
            return

        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Selesai",
                                "Semua gambar sudah diproses!",
                                parent=self.root)
            self.root.quit()
            return

        self.progress['value'] = (self.current_index / len(self.image_files)) * 100

        img_path = os.path.join(self.pictures_path,
                                self.image_files[self.current_index])
        try:
            img = Image.open(img_path)
            win_w = self.root.winfo_width()
            win_h = self.root.winfo_height()
            img_ratio = img.width / img.height
            win_ratio = win_w / win_h

            if img_ratio > win_ratio:
                new_w = win_w - 100
                new_h = int(new_w / img_ratio)
            else:
                new_h = win_h - 200
                new_w = int(new_h * img_ratio)

            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.create_image(win_w/2, win_h/2,
                                     image=self.tk_img,
                                     anchor=tk.CENTER)
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Gagal membuka gambar: {e}",
                                 parent=self.root)
            self.current_index += 1
            self.show_image()

    def move_image(self, folder_name):
        try:
            src = os.path.join(self.pictures_path,
                               self.image_files[self.current_index])
            dst = os.path.join(self.sorter_path,
                               folder_name,
                               self.image_files[self.current_index])
            shutil.move(src, dst)
            self.current_index += 1
            self.show_image()
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Gagal memindahkan gambar: {e}",
                                 parent=self.root)

    def move_image_by_shortcut(self, folder_num):
        if 0 <= folder_num < len(self.folder_list):
            self.move_image(self.folder_list[folder_num])

    def skip_image(self, event=None):
        self.current_index += 1
        self.show_image()

    def prev_image(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def next_image(self, event=None):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()

    def select_folder(self, event=None):
        if self.folder_list:
            self.move_image(self.folder_list[0])

if __name__ == "__main__":
    root = tk.Tk()
    app  = ImageSorterApp(root)
    if root.winfo_exists():
        root.mainloop()
        root.destroy()
