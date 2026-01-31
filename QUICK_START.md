# ⚡ Quick Start Guide

Panduan super cepat untuk mulai menggunakan EduMerdeka Optimizer dalam 5 menit!

## 🚀 Instalasi Super Cepat

### Opsi 1: Python Virtual Environment (Recommended)

```bash
# 1. Download project
git clone <repository-url>
cd edumerdeka-optimizer

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Jalankan aplikasi
streamlit run app.py
```

### Opsi 2: Docker (Paling Mudah!)

```bash
# 1. Pastikan Docker sudah terinstall
docker --version

# 2. Jalankan dengan docker-compose
docker-compose up -d

# 3. Buka browser
http://localhost:8501
```

### Opsi 3: Direct Install (Tanpa Virtual Env)

```bash
# 1. Download project
cd edumerdeka-optimizer

# 2. Install
pip install -r requirements.txt

# 3. Jalankan
streamlit run app.py
```

## 🎯 First Steps (Langkah Pertama)

### 1. Setup Data Dasar (Sidebar)

Isi parameter di sidebar kiri:
- **NIP/Nama Guru**: Nama Anda
- **Nama Siswa**: Nama siswa yang akan dianalisis
- **Kelas**: Contoh: 7A
- **Tahun Ajaran**: 2025/2026
- **Semester**: Genap
- **Fase**: Pilih sesuai tingkat kelas

### 2. Asesmen Diagnostik (Tab 1)

**Cara Tercepat**:
1. Pilih "Input Manual"
2. Jumlah soal: 10
3. Tingkat Bloom: C2 (Memahami)
4. Jawaban benar: 75%
5. Klik "🔍 Proses Asesmen"

**Hasil**: Lihat daya serap dan rekomendasi level

### 3. Learning Path (Tab 2)

1. Pilih mata pelajaran
2. Pilih gaya belajar (Visual/Auditori/Kinestetik)
3. Set slider minat
4. Pilih dimensi Pancasila
5. Klik "🚀 Generate Learning Path"

**Hasil**: Dapat 5 modul rekomendasi + actionable tips

### 4. Projek P5 (Tab 3)

1. Input nama projek
2. Pilih tema P5
3. Set durasi
4. Beri skor 1-10 untuk 6 dimensi
5. Klik "💾 Simpan Projek P5"

**Hasil**: Visualisasi skor karakter per dimensi

### 5. Export (Tab 6)

1. Klik "📄 Generate Laporan PDF"
2. Download PDF
3. Selesai!

## 📊 Demo Data

Coba dengan data contoh:

### Upload CSV Asesmen

1. Tab "Asesmen Diagnostik"
2. Pilih "Upload CSV"
3. Upload file: `examples/contoh_asesmen.csv`
4. Klik "Proses Asesmen"

### Parameter Contoh

```
Guru: Bu Sari (NIP: 123456789)
Siswa: Ahmad Wijaya
Kelas: 7A
Fase: Fase D (Kelas 7-9)
Mata Pelajaran: IPA
Gaya Belajar: Visual
```

## 🎓 Use Cases Populer

### Case 1: Asesmen Awal Semester
1. Tab Asesmen → Input manual atau CSV
2. Catat baseline daya serap
3. Generate learning path
4. Export laporan untuk dokumentasi

### Case 2: Monitoring Projek P5
1. Tab P5 → Input rencana projek
2. Update jurnal refleksi berkala
3. Isi skor dimensi karakter
4. Export untuk rapor

### Case 3: E-Portofolio Siswa
1. Tab E-Portofolio → Upload karya
2. Tulis narasi kemajuan
3. Lihat timeline progress
4. Export komprehensif

## 🔧 Tips Produktivitas

### 1. Save Session untuk Offline
```
Tab Export → Save Current Session → Download .pkl
```
Bisa lanjutkan kerja nanti tanpa internet!

### 2. Batch Process
Untuk beberapa siswa:
1. Process siswa 1 → Save session
2. Ganti nama siswa di sidebar
3. Process siswa 2 → Save session
4. Dst.

### 3. Template CSV
Gunakan `examples/contoh_asesmen.csv` sebagai template untuk buat CSV sendiri:
```csv
nomor,soal,tingkat_bloom,jawaban_benar
1,Pertanyaan 1,C1,1
2,Pertanyaan 2,C2,0
```

## ⚠️ Common Issues & Quick Fix

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### Aplikasi lambat?
- Tutup tab lain di browser
- Refresh halaman (F5)
- Restart aplikasi

### Data hilang?
- Gunakan "Save Session" sebelum tutup
- Data tersimpan di session browser (temporary)
- Untuk permanent: Export ke file

## 📱 Mobile Access

### Akses dari HP/Tablet

1. **Same WiFi**:
   - Cek IP komputer: `ipconfig` (Windows) atau `ifconfig` (Mac/Linux)
   - Buka di HP: `http://[IP-KOMPUTER]:8501`
   - Contoh: `http://192.168.1.100:8501`

2. **Deploy Online** (Recommended):
   - Deploy ke Streamlit Cloud (gratis!)
   - Akses dari mana saja
   - Lihat `docs/DEPLOYMENT.md`

## 🎯 Next Steps

Setelah familiar dengan basics:

1. 📖 **Baca User Guide lengkap**: `docs/USER_GUIDE.md`
2. 🔌 **Setup API Integration**: `docs/API_DOCUMENTATION.md`
3. 🚀 **Deploy Online**: `docs/DEPLOYMENT.md`
4. 📊 **Advanced Features**: Eksplorasi Dashboard & What-If Analysis

## 💡 Pro Tips

1. **Backup Rutin**: Export session setiap akhir hari
2. **Gunakan Chrome**: Performa terbaik
3. **Keyboard Shortcuts**: 
   - `Ctrl + R`: Refresh data
   - `Ctrl + Shift + R`: Hard refresh
4. **Dark Mode**: Belum support, coming soon!

## 🆘 Butuh Bantuan?

- 📧 Email: aryhharyanto@proton.me
- 📚 Dokumentasi: `docs/USER_GUIDE.md`
- 🐛 Bug Report: Include screenshot & error message

## 🎉 Selamat Mencoba!

EduMerdeka Optimizer siap membantu optimasi pembelajaran Kurikulum Merdeka Anda!

---

**Total Time to First Result**: < 5 menit ⚡

*Last Updated: January 31, 2026*
