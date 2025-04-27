import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
import shutil
import platform

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter")

        if platform.system() == "Windows":
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)

        # Setup paths
        self.base_path = os.getcwd()
        self.pictures_path = os.path.join(self.base_path, "Pictures")
        self.sorter_path = os.path.join(self.base_path, "Sorter")

        # Cek folder
        self.check_directories()

        # Load gambar
        self.image_files = [f for f in os.listdir(self.pictures_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"))]
        self.current_index = 0

        # Setup UI
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.load_folders()

        # Progress bar setup
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        self.show_image()

        # Keyboard bindings for number keys (1-9)
        for i in range(9):
            self.root.bind(f"<Key-{i+1}>", lambda event, folder_num=i: self.move_image_by_shortcut(folder_num))

        # Keyboard bindings for navigation
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Return>", self.select_folder)
        self.root.bind("<Escape>", self.skip_image)

    def check_directories(self):
        if not os.path.exists(self.pictures_path):
            create_folder = messagebox.askyesno("Folder Tidak Ditemukan", "'Pictures' folder tidak ditemukan. Apakah Anda ingin membuatnya?")
            if create_folder:
                os.mkdir(self.pictures_path)
            else:
                self.root.destroy()
                return

        if not os.path.exists(self.sorter_path):
            os.mkdir(self.sorter_path)

        # Cek apakah ada subfolder di Sorter
        if not any(os.path.isdir(os.path.join(self.sorter_path, d)) for d in os.listdir(self.sorter_path)):
            self.create_sorter_folders()

    def create_sorter_folders(self):
        try:
            jumlah = simpledialog.askinteger("Input", "Masukkan jumlah folder kategori (maks 9):", minvalue=1, maxvalue=9)
            if jumlah is None:
                messagebox.showinfo("Batal", "Pembuatan folder dibatalkan.")
                self.root.destroy()
                return
            
            self.folder_list = []  # Reset the folder list
            for i in range(1, jumlah + 1):
                nama_folder = simpledialog.askstring("Nama Folder", f"Masukkan nama untuk kategori ke-{i}:")
                if nama_folder is None or nama_folder.strip() == "":
                    messagebox.showerror("Error", "Nama folder tidak boleh kosong.")
                    self.root.destroy()
                    return
                os.mkdir(os.path.join(self.sorter_path, nama_folder.strip()))
                self.folder_list.append(nama_folder.strip())  # Add to folder list
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.root.destroy()

    def load_folders(self):
        # Clear button sebelumnya
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Create a button for each folder in sorter, in the order they were created
        self.folder_list = [d for d in os.listdir(self.sorter_path) if os.path.isdir(os.path.join(self.sorter_path, d))]
        for i, folder in enumerate(self.folder_list):
            btn = tk.Button(self.button_frame, text=f"{i+1}. {folder}", command=lambda f=folder: self.move_image(f))
            btn.pack(side=tk.LEFT, padx=5)

        # Tambah tombol Skip
        skip_btn = tk.Button(self.button_frame, text="Skip", bg="orange", command=self.skip_image)
        skip_btn.pack(side=tk.LEFT, padx=5)

    def show_image(self):
        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Selesai", "Semua gambar sudah diproses!")
            self.root.destroy()
            return

        # Update progress bar
        self.progress['value'] = (self.current_index / len(self.image_files)) * 100

        img_path = os.path.join(self.pictures_path, self.image_files[self.current_index])
        try:
            img = Image.open(img_path)

            # Resize gambar dengan menjaga rasio, agar sesuai ukuran window
            win_width = self.root.winfo_width()
            win_height = self.root.winfo_height()

            img_ratio = img.width / img.height
            win_ratio = win_width / win_height

            if img_ratio > win_ratio:
                new_width = win_width - 100
                new_height = int(new_width / img_ratio)
            else:
                new_height = win_height - 200
                new_width = int(new_height * img_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.create_image(win_width/2, win_height/2, image=self.tk_img, anchor=tk.CENTER)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka gambar: {e}")
            self.current_index += 1
            self.show_image()

    def move_image(self, folder_name):
        try:
            src_path = os.path.join(self.pictures_path, self.image_files[self.current_index])
            dst_path = os.path.join(self.sorter_path, folder_name, self.image_files[self.current_index])
            shutil.move(src_path, dst_path)
            self.current_index += 1
            self.show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memindahkan gambar: {e}")

    def move_image_by_shortcut(self, folder_num):
        # Ensure folder_num is within range (0-8 for 9 categories)
        if 0 <= folder_num < len(self.folder_list):
            folder_name = self.folder_list[folder_num]
            self.move_image(folder_name)

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
    app = ImageSorterApp(root)
    root.mainloop()
