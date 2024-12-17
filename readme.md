Nama Anggota dan ID GitHub:
1. Bani Adam Tampubolon (121140187) : baniadamtampubolon
2. Zahra Areefa Ananta (121140138) : ZahraAreefaAnanta

Deskripsi filter Tilt and Answer:
Proyek ini adalah sebuah filter kuis interaktif yang menggunakan deteksi gerakan kepala untuk memilih jawaban, dikembangkan dengan Python menggunakan pustaka OpenCV dan MediaPipe. Filter ini menampilkan pertanyaan secara acak dengan dua pilihan jawaban, di mana pengguna dapat menjawab dengan menggerakkan kepala ke kanan atau ke kiri. Setelah setiap jawaban diberikan, pertanyaan secara otomatis berganti hingga 10 pertanyaan selesai dijawab, dan skor akhir akan ditampilkan. Proyek ini dirancang untuk memberikan pengalaman interaktif tanpa memerlukan perangkat keras tambahan seperti mouse atau keyboard, sehingga cocok digunakan untuk hiburan, pembelajaran, atau aplikasi berbasis teknologi lainnya.

Logbook mingguan:

Instruksi dan instalasi untuk penggunaan program:
a. Persyaratan sistem: python 3.12, kamera.
b. Instalasi.
1. Clone Repository:
   Unduh atau clone repository ini ke komputer Anda:
   git clone https://github.com/baniadamtampubolon/tilt-and-answer-multimedia.git
   cd tilt-and-answer-multimedia
2. Buat Virtual Environment.
3. Install Dependencies.
   Install semua library yang dibutuhkan dengan perintah:
   pip install -r requirements.txt
4. Folder Struktur.
   Siapkan folder berikut:
   .
   ├── quiz-question/
   │   ├── q1.png
   │   ├── q2.png
   │   ├── q3.png
   │   ├── q4.png
   │   └── q5.png
   ├── hasil/
   │   ├── skor1.png
   │   ├── skor2.png
   │   ├── skor3.png
   │   ├── skor4.png
   │   └── skor5.png
   ├── main.py
   └── requirements.txt




next to do:
1. setiap abis jawab, posisi kepala harus di re-calibrate
2. saat jawab harus dikasih jeda 2 detik buat re-calibrate
3. waktu 4 detik buat jawab
4. ganti pertanyaan setelah jawab
5. jawaban divalidasi ketika telah 2 detik wajah terdeteksi miring ke arah jawaban
6. saat kepala lurus artinya belum menjawab
7. melihat sudut kemiringan secara live
8. jeje test
9. jeje test II



