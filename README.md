# 📦 Image Sorter App

Aplikasi desktop berbasis Python untuk **menyortir gambar** dengan cepat ke dalam folder kategori yang kamu tentukan.

---

## ✨ Fitur
- Menampilkan gambar satu per satu dalam layar penuh.
- Memindahkan gambar ke folder kategori dengan **klik tombol** atau **shortcut keyboard (1-9)**.
- **Skip** gambar tanpa memindahkan.
- Progress bar yang menunjukkan kemajuan penyortiran.
- Dukungan **Windows** dan **Linux**.

---

## 🛠️ Cara Kerja
1. Saat pertama kali dijalankan:
   - Aplikasi akan mencari folder `Pictures` dan `Sorter` di direktori yang sama dengan aplikasi.
   - Jika tidak ada, aplikasi akan menawarkan untuk membuatnya.
   - Anda akan diminta menentukan jumlah folder kategori (maksimal 9) dan memberi nama masing-masing.

2. Proses sortir:
   - Gambar dari folder `Pictures` akan ditampilkan satu per satu.
   - Anda dapat:
     - Menekan tombol 1-9 di keyboard untuk langsung memindahkan gambar ke folder kategori terkait.
     - Klik tombol kategori di layar.
     - Menekan `←` untuk gambar sebelumnya, `→` untuk gambar berikutnya.
     - Menekan `Skip` untuk melewati gambar.
     - Menekan `Enter` untuk langsung memilih kategori pertama.
     - Menekan `Esc` untuk skip gambar.

3. Setelah semua gambar selesai disortir, aplikasi akan otomatis menutup.

---

## 📂 Struktur Folder
/(project-folder) 
- ├── Pictures/ (isi gambar yang akan disortir) 
- ├── Sorter/ (otomatis dibuat untuk menampung folder kategori) 
- ├── main.py (kode aplikasi)

---

## 🖥️ Cara Menjalankan
1. Pastikan sudah menginstall dependensi:
   pip install pillow
2. Jalankan aplikasinya:
    python main.py

---

## 📦 Build ke .exe (Opsional)
Jika ingin dijadikan file .exe:
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
