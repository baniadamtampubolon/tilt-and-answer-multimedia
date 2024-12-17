**Nama Anggota dan ID GitHub:**
1. Bani Adam Tampubolon (121140187) : baniadamtampubolon
2. Zahra Areefa Ananta (121140138) : ZahraAreefaAnanta

**Deskripsi filter Tilt and Answer:**

Proyek ini adalah sebuah filter kuis interaktif yang menggunakan deteksi gerakan kepala untuk memilih jawaban, dikembangkan dengan Python menggunakan pustaka OpenCV dan MediaPipe. Filter ini menampilkan pertanyaan secara acak dengan dua pilihan jawaban, di mana pengguna dapat menjawab dengan menggerakkan kepala ke kanan atau ke kiri. Setelah setiap jawaban diberikan, pertanyaan secara otomatis berganti hingga 10 pertanyaan selesai dijawab, dan skor akhir akan ditampilkan. Proyek ini dirancang untuk memberikan pengalaman interaktif tanpa memerlukan perangkat keras tambahan seperti mouse atau keyboard, sehingga cocok digunakan untuk hiburan, pembelajaran, atau aplikasi berbasis teknologi lainnya.

**Logbook mingguan:**

**Instruksi dan instalasi untuk penggunaan program:**

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

**Menjalankan Program**

1. Aktifkan virtual environment
2. Jalankan program dengan perintah:

   python main.py
3. Penggunaan Program:
- Program akan mendeteksi wajah Anda menggunakan kamera web.
- Miringkan kepala Anda ke Kanan untuk menjawab YES.
- Miringkan kepala Anda ke Kiri untuk menjawab NO.
- Pertanyaan akan muncul di atas kepala Anda, dan sistem akan mencatat jawaban Anda.
4. Keluar Program:

   Tekan q pada keyboard untuk keluar dari program kapan saja.

**Contoh Penggunaan**
1. Setelah program dimulai, posisi kepala pengguna akan dideteksi.
2. Jawab pertanyaan dengan:
- Miring Kanan → YES
- Miring Kiri → NO
3. Setelah semua pertanyaan selesai, skor akhir akan ditampilkan.

**Hasil Skor**

Skor akhir akan ditampilkan di layar dan diambil dari folder hasil/. Pastikan file gambar seperti skor1.png hingga skor5.png telah tersedia.
