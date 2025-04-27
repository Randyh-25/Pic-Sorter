# 🚀 Image Sorter App

Aplikasi desktop Python untuk menyortir gambar secara cepat dan intuitif. Cukup pilih kategori, tekan shortcut, dan biarkan aplikasi menangani sisanya. 🎉

---

## ✨ Fitur Utama

- 🎬 **Tampilan Layar Penuh**  
  Menampilkan satu gambar per satu, optimal untuk proses review cepat.  
- ⌨️ **Shortcut Keyboard (1–9)**  
  Pindahkan gambar ke kategori dengan menekan angka yang sesuai.  
- 🖱️ **Tombol Kategori Interaktif**  
  Klik tombol di layar untuk memindahkan gambar.  
- 🔄 **Navigasi Gambar**  
  ◀️ `←` / ▶️ `→` pindah gambar sebelumnya/berikutnya.  
- ⏭️ **Skip & Auto-Select**  
  `Esc` untuk lewati, `Enter` untuk kirim ke kategori pertama.  
- 📊 **Progress Bar**  
  Lacak kemajuan penyortiran secara real time.  
- 🪟 **Multi-Platform**  
  Mendukung Windows dan Linux (full-screen & zoom otomatis).

---

## 📁 Struktur Direktori

```
/Pic-Sorter
├── libs/              # (vendored) dependensi Pillow
├── Pictures/          # Tempat gambar mentah yang akan disortir
├── Sorter/            # Dibuat otomatis, berisi folder kategori
├── Sorter.py          # Kode utama aplikasi
└── README.md          # Dokumentasi
```

---

## ⚙️ Persiapan & Instalasi

1. **Clone repo**  
   ```bash
   git clone https://github.com/username/Pic-Sorter.git
   cd Pic-Sorter
   ```

2. **(Opsional) Vendor Pillow**  
   Jika `libs/` belum ada atau ingin memperbarui:  
   ```bash
   pip install --upgrade Pillow --target=libs
   ```

3. **Jalankan Aplikasi**  
   ```bash
   python Sorter.py
   ```

> Catatan: Bila `libs/` sudah ada di repo, Anda tidak perlu menjalankan langkah `pip install Pillow`. Cukup `python Sorter.py`.

---

## 🎮 Cara Pakai

1. **Pertama Kali**
   - Download file di [Release](https://github.com/Randyh-25/Pic-Sorter/releases)
   - Masukan gambar yang ingin di sortir ke folder `Pictures/`
   - Lalu jalankan aplikasi
   - Aplikasi akan cek folder `Sorter/`.  
   - Jika belum ada, Anda diminta membuatnya.  
   - Masukkan jumlah kategori (1–9) dan beri nama tiap folder.

2. **Menyortir Gambar**  
   - Gambar tampil satu per satu.  
   - Tekan `1–9` atau klik tombol kategori untuk memindahkan.  
   - Gunakan `←` / `→` untuk berpindah gambar.  
   - `Esc` untuk skip, `Enter` untuk kategori pertama.  

3. **Selesai**  
   Aplikasi otomatis menutup ketika semua gambar sudah diproses.

---

## 🏗️ Build .exe (Windows)

1. Install PyInstaller:  
   ```bash
   pip install pyinstaller
   ```
2. Bundle jadi single executable:  
   ```bash
   pyinstaller --onefile --noconsole Sorter.py
   ```
3. Temukan hasil di folder `dist/Sorter.exe` dan distribusikan!

---

## 📸 Screenshot
1. Masukan jumlah kategor yang diinginkan!(Maksimal 9)
![Screenshot Image Sorter](https://raw.githubusercontent.com/Randyh-25/Pic-Sorter/refs/heads/main/Screenshoot/1.TentukanJumlahKategori.png)

2. Tentukan nama dari kategori yang ingin dibuat!
![Screenshot Image Sorter](https://raw.githubusercontent.com/Randyh-25/Pic-Sorter/refs/heads/main/Screenshoot/2.MasukanKategori.png)

3. Sortir gambar dengan klik tombol atau dengan shortcut pada keyboard!(1 - 9)
![Screenshot Image Sorter](https://raw.githubusercontent.com/Randyh-25/Pic-Sorter/refs/heads/main/Screenshoot/3.%20Sortir.png)

---

## 🤝 Kontribusi

Semua kontribusi, ide, dan saran sangat kami hargai!  
1. Fork repo  
2. Buat branch fitur/bugfix  
3. Commit & Push  
4. Buka Pull Request

