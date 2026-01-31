# 📚 EduMerdeka Optimizer

Platform optimasi pembelajaran berbasis web untuk Kurikulum Merdeka Indonesia. Tool ini dirancang untuk membantu guru dan siswa dalam mengelola pembelajaran, asesmen diagnostik, learning path adaptif, projek P5, dan e-portofolio.

## 🎯 Vision

Tools ini bertujuan menciptakan SaaS pendidikan adaptif untuk Kurikulum Merdeka Indonesia, membantu guru dan siswa mengoptimalkan pembelajaran, pengembangan Profil Pelajar Pancasila, dan tracking kemajuan tanpa koneksi wajib ke sistem kementerian.

## ✨ Fitur Utama

### 1. 🎯 Asesmen Diagnostik Adaptif
- Input soal tes (manual atau CSV)
- Penyesuaian tingkat kesulitan real-time berdasarkan jawaban
- Analisis hasil kognitif menggunakan Taksonomi Bloom (C1-C6)
- Perhitungan daya serap dengan confidence interval

### 2. 🛤️ Learning Path Generator
- Generate jalur pembelajaran personal berdasarkan:
  - Hasil asesmen diagnostik
  - Gaya belajar (visual/auditori/kinestetik)
  - Minat siswa
  - Target Profil Pelajar Pancasila
- Rekomendasi materi adaptif
- Actionable recommendations untuk improvement

### 3. 🎨 Modul P5 (Projek Penguatan Profil Pelajar Pancasila)
- Manajemen projek lintas mata pelajaran
- Monitoring kemajuan dengan jurnal refleksi
- Penilaian 6 dimensi karakter:
  - Beriman & Bertakwa
  - Mandiri
  - Bergotong Royong
  - Berkebinekaan Global
  - Bernalar Kritis
  - Kreatif
- Visualisasi skor per dimensi

### 4. 📁 E-Portofolio Kemajuan
- Upload karya siswa (foto/dokumen)
- Catatan perkembangan kompetensi berbasis narasi
- Timeline kemajuan visual
- Summary perkembangan komprehensif

### 5. 📊 Dashboard Analisis
- Key Performance Indicators (KPI)
- Threshold alerts otomatis
- Scenario simulation (What-If analysis)
- Multi-semester projection
- Comparison vs benchmark nasional
- Optimization suggestions

### 6. 💾 Export & Integrasi
- Export data ke CSV/Excel
- Generate laporan PDF
- Save/Load session untuk offline use
- Hook untuk future API integration (PMM, LLM, dll.)

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.8 atau lebih baru
- pip (Python package installer)

### Instalasi

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`

## 📱 Fitur Mobile-Friendly

- UI responsif untuk berbagai ukuran layar
- Optimasi untuk koneksi low bandwidth
- Accessibility features (ARIA labels)
- Offline mode dengan local caching

## 🔧 Teknologi yang Digunakan

- **Framework**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Optimization**: PuLP (linear programming)
- **Export**: FPDF (PDF), OpenPyXL (Excel)
- **Image Processing**: Pillow

## 📊 Formula & Metodologi

### Daya Serap Kognitif
```
Skor = (Jumlah TP dikuasai / Total TP) × 100
```
- Adjust adaptif: Jika jawaban benar >70%, tingkatkan kesulitan Bloom +1

### Skor Karakter
```
Avg(dimensi1 + ... + dimensi6) / 6 × 100
Kemajuan = (Skor akhir - Skor awal) / Skor awal × 100%
```

### Ketercapaian ATP
```
(Materi dikuasai / Target ATP) × 100%
```

### Minat Siswa
```
Frekuensi interaksi konten / Total interaksi × 100%
```

## 🎓 Panduan Penggunaan

### Untuk Guru:

1. **Setup Awal**: Input data guru dan siswa di sidebar
2. **Asesmen**: Mulai dengan asesmen diagnostik untuk baseline
3. **Learning Path**: Generate learning path berdasarkan hasil asesmen
4. **P5 Monitoring**: Track projek P5 dan perkembangan karakter
5. **Portofolio**: Dokumentasikan karya dan kemajuan siswa
6. **Analisis**: Monitor progress di dashboard
7. **Export**: Download laporan untuk dokumentasi

### Untuk Siswa:

1. Lihat hasil asesmen dan rekomendasi learning path
2. Upload karya ke e-portofolio
3. Isi jurnal refleksi untuk projek P5
4. Monitor progress pribadi di dashboard

## ⚠️ Disclaimer

Tool ini menghasilkan **estimasi kasar** berdasarkan data yang diinput. Hasil ini **bukan pengganti asesmen resmi** dan konsultasi dengan guru/mentor sangat direkomendasikan untuk keputusan pembelajaran yang lebih tepat.

## 🔮 Future Development

### Planned Features:
- [ ] Integrasi API LLM (Groq/Gemini) untuk AI-powered learning path
- [ ] Integrasi dengan Platform Merdeka Mengajar (PMM)
- [ ] REST API untuk integrasi dengan sistem eksternal
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time collaboration features
- [ ] Advanced analytics dengan ML predictions
- [ ] Gamification elements
- [ ] Multi-language support

### Integration Hooks Ready:
- API endpoints structure prepared
- PMM data fetching capability
- Offline-first architecture
- Anonymized usage logging

## 📝 License & Usage

**Non-Open Source** - This software is proprietary and not available for public collaboration or redistribution.

**For Educational Use** - Designed specifically for optimizing education within the Indonesian Kurikulum Merdeka framework.

## 👤 Author

**Ary HH**  
Email: aryhharyanto@proton.me

## 🙏 Acknowledgments

- Kurikulum Merdeka framework by Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia
- Platform Merdeka Mengajar (PMM)
- Taksonomi Bloom untuk cognitive assessment framework

## 📞 Support

Untuk pertanyaan, feedback, atau dukungan teknis, silakan hubungi:
- Email: aryhharyanto@proton.me

---

**EduMerdeka Optimizer** - Mengoptimalkan pembelajaran untuk generasi Profil Pelajar Pancasila 🇮🇩
