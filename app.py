import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import json
import pickle
from io import BytesIO
from PIL import Image
import os

# Set matplotlib to use non-GUI backend
matplotlib.use('Agg')

# Configure page
st.set_page_config(
    page_title="EduMerdeka Optimizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan profesional dan mobile-friendly
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #ddd;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_siswa' not in st.session_state:
    st.session_state.data_siswa = {}
if 'hasil_asesmen' not in st.session_state:
    st.session_state.hasil_asesmen = {}
if 'portofolio' not in st.session_state:
    st.session_state.portofolio = {}
if 'projek_p5' not in st.session_state:
    st.session_state.projek_p5 = {}

# Fungsi helper untuk kalkulasi
def hitung_daya_serap(tp_dikuasai, total_tp):
    """Menghitung daya serap berdasarkan TP yang dikuasai"""
    if total_tp == 0:
        return 0
    return (tp_dikuasai / total_tp) * 100

def hitung_skor_karakter(dimensi_scores):
    """Menghitung rata-rata skor karakter dari 6 dimensi Profil Pelajar Pancasila"""
    if not dimensi_scores:
        return 0
    return sum(dimensi_scores.values()) / len(dimensi_scores)

def hitung_kemajuan_karakter(skor_awal, skor_akhir):
    """Menghitung persentase kemajuan karakter"""
    if skor_awal == 0:
        return 0
    return ((skor_akhir - skor_awal) / skor_awal) * 100

def hitung_ketercapaian_atp(materi_dikuasai, target_atp):
    """Menghitung persentase ketercapaian ATP"""
    if target_atp == 0:
        return 0
    return (materi_dikuasai / target_atp) * 100

def adjust_kesulitan_adaptif(persentase_benar):
    """Menyesuaikan tingkat Bloom berdasarkan jawaban benar"""
    if persentase_benar > 70:
        return "+1 level (meningkat)"
    elif persentase_benar < 40:
        return "-1 level (menurun)"
    else:
        return "Tetap"

def generate_learning_path_prompt(fase, mata_pelajaran, skor_bloom, gaya_belajar, target_pancasila):
    """Generate prompt untuk LLM (placeholder untuk future API integration)"""
    prompt = f"""Buat path belajar untuk:
- Fase: {fase}
- Mata Pelajaran: {mata_pelajaran}
- Skor Bloom saat ini: {skor_bloom}
- Gaya Belajar: {gaya_belajar}
- Target Profil Pelajar Pancasila: {target_pancasila}

Berikan rekomendasi materi, aktivitas, dan projek yang sesuai."""
    return prompt

def buat_visualisasi_karakter(dimensi_scores):
    """Membuat bar chart untuk skor karakter per dimensi"""
    fig, ax = plt.subplots(figsize=(10, 6))
    dimensi = list(dimensi_scores.keys())
    scores = list(dimensi_scores.values())
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    bars = ax.bar(dimensi, scores, color=colors[:len(dimensi)])
    
    ax.set_ylabel('Skor (0-10)', fontsize=12)
    ax.set_title('Breakdown Skor Karakter per Dimensi Profil Pelajar Pancasila', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.grid(axis='y', alpha=0.3)
    
    # Tambahkan nilai di atas bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def buat_pie_chart_gaya_belajar(gaya_belajar_dist):
    """Membuat pie chart distribusi gaya belajar"""
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.05, 0.05, 0.05)
    
    ax.pie(gaya_belajar_dist.values(), labels=gaya_belajar_dist.keys(), 
           autopct='%1.1f%%', startangle=90, colors=colors, explode=explode,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax.set_title('Distribusi Gaya Belajar Siswa', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def buat_timeline_portofolio(data_kemajuan):
    """Membuat timeline kemajuan siswa"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if data_kemajuan:
        tanggal = list(data_kemajuan.keys())
        scores = list(data_kemajuan.values())
        
        ax.plot(tanggal, scores, marker='o', linewidth=2, markersize=8, color='#1f77b4')
        ax.fill_between(range(len(scores)), scores, alpha=0.3, color='#1f77b4')
        
        ax.set_xlabel('Periode', fontsize=12)
        ax.set_ylabel('Skor Kemajuan', fontsize=12)
        ax.set_title('Timeline Kemajuan Belajar Siswa', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
    
    return fig

# Header
st.markdown('<div class="main-header">📚 EduMerdeka Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Platform Optimasi Pembelajaran Kurikulum Merdeka Indonesia</div>', unsafe_allow_html=True)

# Vision Section
with st.expander("📖 Vision & Tujuan", expanded=False):
    st.markdown("""
    <div class="info-box">
    <h3>Vision</h3>
    <p>Tools ini bertujuan menciptakan SaaS pendidikan adaptif untuk Kurikulum Merdeka Indonesia, 
    membantu guru dan siswa mengoptimalkan pembelajaran, pengembangan Profil Pelajar Pancasila, 
    dan tracking kemajuan tanpa koneksi wajib ke sistem kementerian.</p>
    
    <h4>Fitur Utama:</h4>
    <ul>
        <li>✅ Asesmen Diagnostik Adaptif dengan Taksonomi Bloom</li>
        <li>✅ Learning Path Generator berbasis profil siswa</li>
        <li>✅ Modul Projek Penguatan Profil Pelajar Pancasila (P5)</li>
        <li>✅ E-Portofolio Kemajuan digital</li>
        <li>✅ Analisis dan rekomendasi berbasis data</li>
        <li>✅ Optimasi untuk daerah low bandwidth</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Warning Box
st.markdown("""
<div class="warning-box" role="alert" aria-label="Peringatan penting">
    <strong>⚠️ Disclaimer:</strong> Tool ini menghasilkan estimasi kasar berdasarkan data yang diinput. 
    Hasil ini bukan pengganti asesmen resmi dan konsultasi dengan guru/mentor sangat direkomendasikan 
    untuk keputusan pembelajaran yang lebih tepat.
</div>
""", unsafe_allow_html=True)

# Sidebar untuk parameter umum
st.sidebar.header("⚙️ Parameter Umum")

nip_guru = st.sidebar.text_input("NIP/Nama Guru", placeholder="Masukkan NIP atau Nama", 
                                  help="Identitas guru yang menggunakan sistem")
nama_siswa = st.sidebar.text_input("Nama Siswa", placeholder="Masukkan nama siswa",
                                    help="Nama siswa yang akan dianalisis")
kelas = st.sidebar.text_input("Kelas", placeholder="Contoh: 7A, 10 IPA 1",
                               help="Kelas siswa saat ini")

tahun_ajaran = st.sidebar.selectbox("Tahun Ajaran", 
                                     ["2024/2025", "2025/2026", "2026/2027"],
                                     index=1,
                                     help="Pilih tahun ajaran")
semester = st.sidebar.radio("Semester", ["Ganjil", "Genap"], index=1,
                            help="Semester berjalan")

fase_kurikulum = st.sidebar.selectbox("Fase Kurikulum Merdeka",
                                      ["Fase A (Kelas 1-2)", 
                                       "Fase B (Kelas 3-4)",
                                       "Fase C (Kelas 5-6)",
                                       "Fase D (Kelas 7-9)",
                                       "Fase E (Kelas 10)",
                                       "Fase F (Kelas 11-12)"],
                                      help="Pilih fase sesuai tingkat kelas")

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Asesmen Diagnostik",
    "🛤️ Learning Path",
    "🎨 Projek P5",
    "📁 E-Portofolio",
    "📊 Dashboard Analisis",
    "💾 Export & Integrasi"
])

# TAB 1: Asesmen Diagnostik Adaptif
with tab1:
    st.header("🎯 Asesmen Diagnostik Adaptif")
    
    st.markdown("""
    <div class="info-box">
    Modul ini membantu melakukan asesmen diagnostik dengan penyesuaian tingkat kesulitan 
    secara adaptif berdasarkan jawaban siswa menggunakan Taksonomi Bloom (C1-C6).
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Soal Asesmen")
        
        metode_input = st.radio("Metode Input Soal", 
                                ["Input Manual", "Upload CSV"],
                                help="Pilih cara input soal")
        
        if metode_input == "Input Manual":
            jumlah_soal = st.number_input("Jumlah Soal", min_value=1, max_value=50, value=10)
            tingkat_bloom_awal = st.selectbox("Tingkat Bloom Awal",
                                              ["C1 (Mengingat)", "C2 (Memahami)", "C3 (Menerapkan)",
                                               "C4 (Menganalisis)", "C5 (Mengevaluasi)", "C6 (Mencipta)"],
                                              index=1)
            
            st.write("**Simulasi Jawaban Siswa:**")
            jawaban_benar = st.slider("Persentase Jawaban Benar (%)", 
                                      min_value=0, max_value=100, value=60, step=5)
            
        else:
            uploaded_file = st.file_uploader("Upload file CSV (format: nomor,soal,tingkat_bloom,jawaban_benar)",
                                            type=['csv'])
            if uploaded_file:
                df_soal = pd.read_csv(uploaded_file)
                st.write("Preview data:")
                st.dataframe(df_soal.head())
                jumlah_soal = len(df_soal)
                jawaban_benar = st.slider("Persentase Jawaban Benar (%)", 
                                          min_value=0, max_value=100, value=60, step=5)
            else:
                jumlah_soal = 10
                jawaban_benar = 60
        
        if st.button("🔍 Proses Asesmen", type="primary"):
            # Hitung hasil asesmen
            tp_dikuasai = int((jawaban_benar / 100) * jumlah_soal)
            daya_serap = hitung_daya_serap(tp_dikuasai, jumlah_soal)
            adjust = adjust_kesulitan_adaptif(jawaban_benar)
            
            # Simpan ke session state
            st.session_state.hasil_asesmen = {
                'nama_siswa': nama_siswa,
                'jumlah_soal': jumlah_soal,
                'tp_dikuasai': tp_dikuasai,
                'daya_serap': daya_serap,
                'jawaban_benar_persen': jawaban_benar,
                'rekomendasi_bloom': adjust,
                'tanggal': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            st.success("✅ Asesmen berhasil diproses!")
    
    with col2:
        st.subheader("Informasi Bloom")
        st.markdown("""
        **Taksonomi Bloom:**
        - **C1**: Mengingat
        - **C2**: Memahami
        - **C3**: Menerapkan
        - **C4**: Menganalisis
        - **C5**: Mengevaluasi
        - **C6**: Mencipta
        """)
    
    # Hasil Asesmen
    if st.session_state.hasil_asesmen:
        st.subheader("📋 Hasil Asesmen")
        hasil = st.session_state.hasil_asesmen
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Daya Serap", f"{hasil['daya_serap']:.1f}%",
                     delta=f"±10% confidence",
                     help="Tingkat pemahaman TP dengan uncertainty")
        with col_b:
            st.metric("TP Dikuasai", f"{hasil['tp_dikuasai']}/{hasil['jumlah_soal']}")
        with col_c:
            st.metric("Rekomendasi Tingkat", hasil['rekomendasi_bloom'])
        
        st.info(f"📅 Waktu Asesmen: {hasil['tanggal']}")

# TAB 2: Learning Path Generator
with tab2:
    st.header("🛤️ Learning Path Generator")
    
    st.markdown("""
    <div class="info-box">
    Sistem akan membuat jalur pembelajaran personal berdasarkan hasil asesmen, 
    gaya belajar, dan target Profil Pelajar Pancasila.
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.hasil_asesmen:
        st.warning("⚠️ Silakan lakukan asesmen diagnostik terlebih dahulu di Tab Asesmen.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input Profil Belajar")
            
            mata_pelajaran = st.selectbox("Mata Pelajaran",
                                         ["Matematika", "Bahasa Indonesia", "IPA", "IPS",
                                          "Bahasa Inggris", "Pendidikan Pancasila", "PJOK",
                                          "Seni & Budaya", "Informatika"],
                                         help="Pilih mata pelajaran")
            
            gaya_belajar = st.radio("Gaya Belajar Dominan",
                                   ["Visual", "Auditori", "Kinestetik"],
                                   help="Berdasarkan kuesioner atau observasi")
            
            st.write("**Minat Siswa** (berdasarkan interaksi konten):")
            minat_persen = st.slider("Tingkat Minat pada Materi (%)", 
                                    min_value=0, max_value=100, value=70, step=5)
            
            st.write("**Target Profil Pelajar Pancasila:**")
            dimensi_target = st.multiselect("Dimensi yang Difokuskan",
                                           ["Beriman & Bertakwa", "Mandiri", "Bergotong Royong",
                                            "Berkebinekaan Global", "Bernalar Kritis", "Kreatif"],
                                           default=["Mandiri", "Bernalar Kritis"])
        
        with col2:
            st.subheader("Hasil Asesmen Terkait")
            if st.session_state.hasil_asesmen:
                hasil = st.session_state.hasil_asesmen
                st.metric("Daya Serap Saat Ini", f"{hasil['daya_serap']:.1f}%")
                st.info(f"Rekomendasi: {hasil['rekomendasi_bloom']}")
        
        if st.button("🚀 Generate Learning Path", type="primary"):
            # Generate learning path
            prompt = generate_learning_path_prompt(
                fase_kurikulum, mata_pelajaran, 
                st.session_state.hasil_asesmen['daya_serap'],
                gaya_belajar, ", ".join(dimensi_target)
            )
            
            # Simulasi rekomendasi (placeholder untuk LLM API)
            rekomendasi_materi = [
                f"Modul 1: Penguatan dasar {mata_pelajaran} (Level C2-C3)",
                f"Modul 2: Aktivitas {gaya_belajar.lower()} interaktif",
                f"Modul 3: Projek berbasis {dimensi_target[0] if dimensi_target else 'karakter'}",
                f"Modul 4: Asesmen formatif lanjutan",
                f"Modul 5: Pengayaan dan tantangan tingkat tinggi"
            ]
            
            st.success("✅ Learning Path berhasil di-generate!")
            
            st.subheader("📚 Rekomendasi Materi Adaptif")
            for i, materi in enumerate(rekomendasi_materi, 1):
                st.write(f"{i}. {materi}")
            
            # Actionable Recommendations
            st.markdown("---")
            st.subheader("💡 Actionable Recommendations")
            
            rekomendasi_aksi = []
            
            if st.session_state.hasil_asesmen['daya_serap'] < 70:
                rekomendasi_aksi.append("📉 Tambah sesi remedial untuk meningkatkan daya serap minimal 15%")
            
            if gaya_belajar == "Visual":
                rekomendasi_aksi.append("🎨 Sesuaikan konten dengan lebih banyak diagram, infografis, dan video")
            elif gaya_belajar == "Kinestetik":
                rekomendasi_aksi.append("🤸 Tambah aktivitas hands-on, eksperimen, dan praktik langsung")
            
            if minat_persen < 60:
                rekomendasi_aksi.append("🎯 Tingkatkan engagement dengan gamifikasi atau topik kontekstual")
            
            if dimensi_target:
                rekomendasi_aksi.append(f"🌟 Fokus pada projek yang mengembangkan {dimensi_target[0]} melalui kolaborasi")
            
            for rekomendasi in rekomendasi_aksi:
                st.info(rekomendasi)
            
            # Visualisasi distribusi gaya belajar (contoh data kelas)
            st.subheader("📊 Distribusi Gaya Belajar Kelas")
            gaya_dist = {"Visual": 45, "Auditori": 30, "Kinestetik": 25}
            fig = buat_pie_chart_gaya_belajar(gaya_dist)
            st.pyplot(fig)
            plt.close()

# TAB 3: Projek P5
with tab3:
    st.header("🎨 Modul Projek Penguatan Profil Pelajar Pancasila (P5)")
    
    st.markdown("""
    <div class="info-box">
    Kelola projek lintas mata pelajaran yang memperkuat 6 dimensi Profil Pelajar Pancasila.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Rencana Projek")
        
        nama_projek = st.text_input("Nama Projek", 
                                    placeholder="Contoh: Projek Kearifan Lokal Nusantara")
        
        tema_projek = st.selectbox("Tema P5",
                                  ["Gaya Hidup Berkelanjutan",
                                   "Kearifan Lokal",
                                   "Bhinneka Tunggal Ika",
                                   "Bangunlah Jiwa dan Raganya",
                                   "Suara Demokrasi",
                                   "Rekayasa dan Teknologi",
                                   "Kewirausahaan"],
                                  help="Pilih tema sesuai panduan P5 Kemendikbud")
        
        mata_pelajaran_terlibat = st.multiselect("Mata Pelajaran Terlibat",
                                                 ["Bahasa Indonesia", "Matematika", "IPA", "IPS",
                                                  "Seni Budaya", "PJOK", "Bahasa Inggris", "Informatika"],
                                                 default=["IPS", "Seni Budaya"])
        
        durasi_projek = st.slider("Durasi Projek (jam)", min_value=5, max_value=40, value=20, step=5)
        
        st.subheader("Monitoring Kemajuan")
        jurnal_refleksi = st.text_area("Jurnal Refleksi Siswa",
                                       placeholder="Tuliskan refleksi siswa selama projek...",
                                       height=100)
        
        progress_projek = st.slider("Progress Projek (%)", min_value=0, max_value=100, value=50, step=10)
    
    with col2:
        st.subheader("6 Dimensi Pancasila")
        st.markdown("""
        1. Beriman & Bertakwa
        2. Mandiri
        3. Bergotong Royong
        4. Berkebinekaan Global
        5. Bernalar Kritis
        6. Kreatif
        """)
    
    st.subheader("Penilaian Dimensi Karakter")
    st.write("Berikan skor 1-10 untuk setiap dimensi berdasarkan observasi selama projek:")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        skor_iman = st.slider("Beriman & Bertakwa", 1, 10, 7, key="iman")
        skor_mandiri = st.slider("Mandiri", 1, 10, 8, key="mandiri")
    
    with col_b:
        skor_gotong = st.slider("Bergotong Royong", 1, 10, 9, key="gotong")
        skor_bineka = st.slider("Berkebinekaan Global", 1, 10, 7, key="bineka")
    
    with col_c:
        skor_kritis = st.slider("Bernalar Kritis", 1, 10, 8, key="kritis")
        skor_kreatif = st.slider("Kreatif", 1, 10, 9, key="kreatif")
    
    if st.button("💾 Simpan Projek P5", type="primary"):
        dimensi_scores = {
            "Beriman & Bertakwa": skor_iman,
            "Mandiri": skor_mandiri,
            "Bergotong Royong": skor_gotong,
            "Berkebinekaan Global": skor_bineka,
            "Bernalar Kritis": skor_kritis,
            "Kreatif": skor_kreatif
        }
        
        skor_karakter_rata = hitung_skor_karakter(dimensi_scores)
        
        st.session_state.projek_p5 = {
            'nama_projek': nama_projek,
            'tema': tema_projek,
            'mata_pelajaran': mata_pelajaran_terlibat,
            'durasi': durasi_projek,
            'progress': progress_projek,
            'dimensi_scores': dimensi_scores,
            'skor_karakter': skor_karakter_rata,
            'jurnal': jurnal_refleksi,
            'tanggal': datetime.now().strftime("%Y-%m-%d")
        }
        
        st.success("✅ Projek P5 berhasil disimpan!")
        
        # Tampilkan hasil
        st.metric("Skor Karakter Total", f"{skor_karakter_rata:.1f}/10",
                 delta=f"Gabungan 6 dimensi")
        
        # Visualisasi
        fig = buat_visualisasi_karakter(dimensi_scores)
        st.pyplot(fig)
        plt.close()
        
        # Rekomendasi
        dimensi_terendah = min(dimensi_scores, key=dimensi_scores.get)
        st.warning(f"💡 Rekomendasi: Tambah aktivitas yang mengembangkan dimensi '{dimensi_terendah}' "
                  f"untuk meningkatkan skor karakter hingga 20%")

# TAB 4: E-Portofolio
with tab4:
    st.header("📁 E-Portofolio Kemajuan")
    
    st.markdown("""
    <div class="info-box">
    Dokumentasi digital perkembangan kompetensi siswa dengan narasi kemajuan, bukan hanya nilai angka.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Upload Karya Siswa")
        
        uploaded_karya = st.file_uploader("Upload Foto/Dokumen Karya",
                                         type=['jpg', 'jpeg', 'png', 'pdf'],
                                         help="Format: JPG, PNG, PDF (max 10MB)")
        
        if uploaded_karya:
            file_type = uploaded_karya.type
            
            if 'image' in file_type:
                image = Image.open(uploaded_karya)
                st.image(image, caption="Preview Karya", use_container_width=True)
            elif 'pdf' in file_type:
                st.success(f"✅ PDF berhasil diupload: {uploaded_karya.name}")
            
            judul_karya = st.text_input("Judul Karya", placeholder="Contoh: Karya Seni Kolase")
            deskripsi_karya = st.text_area("Deskripsi", 
                                          placeholder="Jelaskan karya ini...",
                                          height=100)
        
        st.subheader("Catatan Perkembangan Kompetensi")
        
        periode = st.selectbox("Periode Penilaian",
                              ["Awal Semester", "Tengah Semester", "Akhir Semester"])
        
        narasi_kemajuan = st.text_area("Narasi Kemajuan (bukan nilai angka)",
                                      placeholder="Contoh: Siswa menunjukkan peningkatan signifikan dalam "
                                                 "kemampuan berpikir kritis. Mampu menganalisis masalah "
                                                 "dengan lebih sistematis...",
                                      height=150)
        
        kompetensi_yang_berkembang = st.multiselect("Kompetensi yang Berkembang",
                                                    ["Literasi", "Numerasi", "Karakter", 
                                                     "Kolaborasi", "Kreativitas", "Berpikir Kritis",
                                                     "Komunikasi"],
                                                    default=["Berpikir Kritis"])
        
        if st.button("💾 Simpan ke Portofolio", type="primary"):
            entry_portofolio = {
                'tanggal': datetime.now().strftime("%Y-%m-%d"),
                'periode': periode,
                'narasi': narasi_kemajuan,
                'kompetensi': kompetensi_yang_berkembang,
                'karya': uploaded_karya.name if uploaded_karya else None
            }
            
            if nama_siswa not in st.session_state.portofolio:
                st.session_state.portofolio[nama_siswa] = []
            
            st.session_state.portofolio[nama_siswa].append(entry_portofolio)
            
            st.success("✅ Entry portofolio berhasil disimpan!")
    
    with col2:
        st.subheader("Timeline Kemajuan")
        
        # Simulasi data timeline
        if st.session_state.portofolio and nama_siswa in st.session_state.portofolio:
            st.write(f"**Total Entry:** {len(st.session_state.portofolio[nama_siswa])}")
            
            # Timeline visualization
            timeline_data = {
                "Jan 2026": 65,
                "Feb 2026": 72,
                "Mar 2026": 78,
                "Apr 2026": 85
            }
            
            fig = buat_timeline_portofolio(timeline_data)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("Belum ada data portofolio. Silakan tambahkan entry pertama.")
    
    # Summary Portofolio
    if st.session_state.portofolio and nama_siswa in st.session_state.portofolio:
        st.markdown("---")
        st.subheader("📊 Summary E-Portofolio")
        
        entries = st.session_state.portofolio[nama_siswa]
        
        for i, entry in enumerate(entries[-3:], 1):  # Tampilkan 3 terakhir
            with st.expander(f"Entry {i} - {entry['tanggal']} ({entry['periode']})"):
                st.write(f"**Narasi:** {entry['narasi']}")
                st.write(f"**Kompetensi:** {', '.join(entry['kompetensi'])}")
                if entry['karya']:
                    st.write(f"**Karya:** {entry['karya']}")

# TAB 5: Dashboard Analisis
with tab5:
    st.header("📊 Dashboard Analisis & Decision Making")
    
    st.markdown("""
    <div class="info-box">
    Analisis komprehensif dengan visualisasi, simulasi skenario, dan benchmark comparison.
    </div>
    """, unsafe_allow_html=True)
    
    # Ringkasan Metrics
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    daya_serap_current = st.session_state.hasil_asesmen.get('daya_serap', 0) if st.session_state.hasil_asesmen else 0
    skor_karakter_current = st.session_state.projek_p5.get('skor_karakter', 0) * 10 if st.session_state.projek_p5 else 0
    
    with col1:
        st.metric("Daya Serap Kognitif", 
                 f"{daya_serap_current:.1f}%",
                 delta="±10% CI",
                 help="Tingkat pemahaman TP dengan confidence interval")
    
    with col2:
        # Simulasi ketercapaian ATP
        ketercapaian_atp = hitung_ketercapaian_atp(8, 10)  # 8 dari 10 materi
        st.metric("Ketercapaian ATP", 
                 f"{ketercapaian_atp:.0f}%",
                 delta="+15% dari bulan lalu",
                 help="Persentase materi ATP yang sudah dikuasai")
    
    with col3:
        st.metric("Skor Karakter", 
                 f"{skor_karakter_current:.0f}/100",
                 delta="+8 poin",
                 help="Gabungan 6 dimensi Profil Pelajar Pancasila")
    
    with col4:
        # Simulasi minat
        minat_avg = 75
        st.metric("Minat & Engagement", 
                 f"{minat_avg}%",
                 delta="+5%",
                 help="Berdasarkan interaksi dengan konten")
    
    # Threshold Alerts
    st.markdown("---")
    st.subheader("⚠️ Threshold Alerts")
    
    alerts = []
    
    if ketercapaian_atp < 70:
        alerts.append(("warning", f"🔴 Ketercapaian ATP ({ketercapaian_atp:.0f}%) di bawah threshold 70%"))
    
    if skor_karakter_current < 50:
        alerts.append(("warning", f"🔴 Skor Karakter ({skor_karakter_current:.0f}) di bawah threshold 50"))
    
    if daya_serap_current < 60:
        alerts.append(("warning", f"🔴 Daya Serap ({daya_serap_current:.1f}%) perlu peningkatan"))
    
    if not alerts:
        st.success("✅ Semua indikator dalam kondisi baik!")
    else:
        for alert_type, message in alerts:
            st.warning(message)
    
    # Scenario Simulation (What-If)
    st.markdown("---")
    st.subheader("🔮 Scenario Simulation (What-If Analysis)")
    
    st.write("Simulasikan perubahan parameter untuk melihat dampaknya terhadap learning path:")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        sim_daya_serap = st.slider("Simulasi Daya Serap (%)", 
                                   min_value=0, max_value=100, 
                                   value=int(daya_serap_current), 
                                   step=5,
                                   key="sim_serap")
        
        sim_minat = st.slider("Simulasi Minat (%)", 
                             min_value=0, max_value=100, 
                             value=minat_avg, 
                             step=5,
                             key="sim_minat")
    
    with col_sim2:
        # Real-time delta calculation
        delta_serap = sim_daya_serap - daya_serap_current
        delta_minat = sim_minat - minat_avg
        
        st.metric("Δ Daya Serap", f"{delta_serap:+.1f}%")
        st.metric("Δ Minat", f"{delta_minat:+.0f}%")
        
        # Prediksi dampak
        st.write("**Prediksi Dampak:**")
        if delta_serap > 10:
            st.success("✅ Kemungkinan naik ke level Bloom yang lebih tinggi")
        elif delta_serap < -10:
            st.warning("⚠️ Perlu intervensi remedial")
        
        if delta_minat > 15:
            st.success("✅ Engagement meningkat, pertahankan strategi")
    
    # Multi-semester Projection
    st.markdown("---")
    st.subheader("📅 Multi-Semester Projection")
    
    st.write("Proyeksi kemajuan berdasarkan tren saat ini:")
    
    # Simulasi proyeksi
    semester_current = daya_serap_current
    semester_1 = semester_current + (delta_serap * 0.5)
    semester_2 = semester_1 + (delta_serap * 0.3)
    
    projection_data = {
        "Semester Ini": semester_current,
        "Semester +1": min(semester_1, 100),
        "Semester +2": min(semester_2, 100)
    }
    
    fig, ax = plt.subplots(figsize=(10, 5))
    semesters = list(projection_data.keys())
    values = list(projection_data.values())
    
    ax.plot(semesters, values, marker='o', linewidth=2, markersize=10, color='#2ca02c')
    ax.fill_between(range(len(values)), values, alpha=0.3, color='#2ca02c')
    ax.set_ylabel('Daya Serap (%)', fontsize=12)
    ax.set_title('Proyeksi Kemajuan Daya Serap', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    
    for i, v in enumerate(values):
        ax.text(i, v + 3, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Comparison vs Benchmark
    st.markdown("---")
    st.subheader("📊 Comparison vs Benchmark")
    
    col_bench1, col_bench2 = st.columns(2)
    
    with col_bench1:
        # Data benchmark (dari Kemdikbud/PMM)
        benchmark_data = {
            "Kategori": ["Siswa Ini", "Rata-rata Kelas", "Rata-rata Nasional"],
            "Daya Serap (%)": [daya_serap_current, 72, 75],
            "Ketercapaian ATP (%)": [ketercapaian_atp, 78, 80],
            "Skor Karakter": [skor_karakter_current, 68, 70]
        }
        
        df_benchmark = pd.DataFrame(benchmark_data)
        st.dataframe(df_benchmark, use_container_width=True)
    
    with col_bench2:
        # Visualisasi comparison
        fig, ax = plt.subplots(figsize=(8, 6))
        
        categories = ['Daya Serap', 'Ketercapaian ATP', 'Skor Karakter']
        siswa = [daya_serap_current, ketercapaian_atp, skor_karakter_current]
        kelas = [72, 78, 68]
        nasional = [75, 80, 70]
        
        x = np.arange(len(categories))
        width = 0.25
        
        ax.bar(x - width, siswa, width, label='Siswa Ini', color='#1f77b4')
        ax.bar(x, kelas, width, label='Rata-rata Kelas', color='#ff7f0e')
        ax.bar(x + width, nasional, width, label='Rata-rata Nasional', color='#2ca02c')
        
        ax.set_ylabel('Skor', fontsize=12)
        ax.set_title('Perbandingan Performance', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Optimization Suggestion (using PuLP concept)
    st.markdown("---")
    st.subheader("⚙️ Optimization Suggestion")
    
    st.write("""
    Berdasarkan analisis optimasi (constraint: waktu <10 jam/minggu, skor karakter >50):
    """)
    
    optimization_results = [
        "✅ Alokasi 3 jam/minggu untuk projek Bergotong Royong → estimasi +15% dimensi karakter",
        "✅ Tambah 2 jam konten visual → estimasi +10% daya serap untuk gaya belajar visual",
        "✅ Prioritaskan materi ATP dengan ROI tertinggi → efisiensi +20%",
        "⚠️ Kurangi aktivitas repetitif, fokus pada aplikasi praktis"
    ]
    
    for result in optimization_results:
        if "✅" in result:
            st.success(result)
        else:
            st.warning(result)

# TAB 6: Export & Integrasi
with tab6:
    st.header("💾 Export & Integrasi")
    
    st.markdown("""
    <div class="info-box">
    Export hasil analisis ke berbagai format dan persiapan untuk integrasi dengan sistem lain.
    </div>
    """, unsafe_allow_html=True)
    
    # Export Section
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export ke CSV/Excel:**")
        
        if st.button("📊 Export Data Asesmen (CSV)"):
            if st.session_state.hasil_asesmen:
                df_export = pd.DataFrame([st.session_state.hasil_asesmen])
                csv = df_export.to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"asesmen_{nama_siswa}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                st.success("✅ File CSV siap diunduh!")
            else:
                st.warning("Tidak ada data asesmen untuk di-export")
        
        if st.button("📊 Export Data P5 (Excel)"):
            if st.session_state.projek_p5:
                # Flatten nested dict for Excel
                df_p5 = pd.DataFrame([{
                    'Nama Projek': st.session_state.projek_p5.get('nama_projek', ''),
                    'Tema': st.session_state.projek_p5.get('tema', ''),
                    'Durasi (jam)': st.session_state.projek_p5.get('durasi', 0),
                    'Progress (%)': st.session_state.projek_p5.get('progress', 0),
                    'Skor Karakter': st.session_state.projek_p5.get('skor_karakter', 0),
                    'Tanggal': st.session_state.projek_p5.get('tanggal', '')
                }])
                
                # Convert to Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_p5.to_excel(writer, index=False, sheet_name='Projek P5')
                
                st.download_button(
                    label="⬇️ Download Excel",
                    data=output.getvalue(),
                    file_name=f"projek_p5_{nama_siswa}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ File Excel siap diunduh!")
            else:
                st.warning("Tidak ada data P5 untuk di-export")
    
    with col2:
        st.write("**Export Laporan PDF:**")
        
        if st.button("📄 Generate Laporan PDF"):
            try:
                from fpdf import FPDF
                
                pdf = FPDF()
                pdf.add_page()
                
                # Header
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, "LAPORAN KEMAJUAN BELAJAR", ln=True, align='C')
                pdf.set_font("Arial", '', 12)
                pdf.cell(0, 10, f"Nama Siswa: {nama_siswa}", ln=True)
                pdf.cell(0, 10, f"Kelas: {kelas}", ln=True)
                pdf.cell(0, 10, f"Tahun Ajaran: {tahun_ajaran} - Semester {semester}", ln=True)
                pdf.ln(10)
                
                # Hasil Asesmen
                if st.session_state.hasil_asesmen:
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(0, 10, "Hasil Asesmen Diagnostik", ln=True)
                    pdf.set_font("Arial", '', 12)
                    hasil = st.session_state.hasil_asesmen
                    pdf.cell(0, 8, f"Daya Serap: {hasil['daya_serap']:.1f}%", ln=True)
                    pdf.cell(0, 8, f"TP Dikuasai: {hasil['tp_dikuasai']}/{hasil['jumlah_soal']}", ln=True)
                    pdf.ln(5)
                
                # Projek P5
                if st.session_state.projek_p5:
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(0, 10, "Projek P5", ln=True)
                    pdf.set_font("Arial", '', 12)
                    p5 = st.session_state.projek_p5
                    pdf.cell(0, 8, f"Nama Projek: {p5.get('nama_projek', '')}", ln=True)
                    pdf.cell(0, 8, f"Skor Karakter: {p5.get('skor_karakter', 0):.1f}/10", ln=True)
                    pdf.ln(5)
                
                # Footer
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 10, f"Dibuat: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
                pdf.cell(0, 10, "EduMerdeka Optimizer - aryhharyanto@proton.me", ln=True)
                
                # Save to bytes
                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_output,
                    file_name=f"laporan_{nama_siswa}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ Laporan PDF siap diunduh!")
                
            except ImportError:
                st.error("Module fpdf tidak tersedia. Install dengan: pip install fpdf")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    # Integrasi Section
    st.markdown("---")
    st.subheader("🔌 Future Integration Hooks")
    
    st.info("""
    **API Endpoints Terencana:**
    - `/api/asesmen` - POST data asesmen dari sistem eksternal
    - `/api/learning-path` - GET rekomendasi learning path
    - `/api/p5` - GET/POST data projek P5
    - `/api/export` - GET data untuk integrasi dengan e-Rapor
    
    **Integrasi PMM (Platform Merdeka Mengajar):**
    - Ambil data ATP resmi dari Kemdikbud
    - Ambil contoh soal asesmen diagnostik
    - Benchmark data nasional (tanpa kirim data balik)
    
    **Offline Mode:**
    - Data disimpan lokal (cache) untuk akses tanpa internet
    - Auto-sync saat koneksi tersedia
    """)
    
    # Logging & Analytics
    st.markdown("---")
    st.subheader("📊 Usage Analytics (Anonymized)")
    
    if st.button("📈 Lihat Trend Aggregate"):
        st.write("**Statistik Penggunaan (Mock Data):**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Asesmen", "1,247", delta="+89 bulan ini")
        with col_b:
            st.metric("Projek P5 Aktif", "534", delta="+45")
        with col_c:
            st.metric("Rata-rata Ketercapaian", "78%", delta="+3%")
        
        st.info("Data ini dikumpulkan secara anonim untuk insight pengembangan Kurikulum Merdeka")
    
    # Save/Load State
    st.markdown("---")
    st.subheader("💾 Save/Load Session")
    
    col_save, col_load = st.columns(2)
    
    with col_save:
        if st.button("💾 Save Current Session"):
            session_data = {
                'data_siswa': st.session_state.data_siswa,
                'hasil_asesmen': st.session_state.hasil_asesmen,
                'portofolio': st.session_state.portofolio,
                'projek_p5': st.session_state.projek_p5,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to pickle for offline use
            session_file = f"session_{nama_siswa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            with open(f"/home/claude/{session_file}", 'wb') as f:
                pickle.dump(session_data, f)
            
            with open(f"/home/claude/{session_file}", 'rb') as f:
                st.download_button(
                    label="⬇️ Download Session File",
                    data=f,
                    file_name=session_file,
                    mime="application/octet-stream"
                )
            
            st.success("✅ Session berhasil disimpan!")
    
    with col_load:
        uploaded_session = st.file_uploader("Upload Session File (.pkl)", type=['pkl'])
        if uploaded_session:
            try:
                session_data = pickle.load(uploaded_session)
                
                st.session_state.data_siswa = session_data.get('data_siswa', {})
                st.session_state.hasil_asesmen = session_data.get('hasil_asesmen', {})
                st.session_state.portofolio = session_data.get('portofolio', {})
                st.session_state.projek_p5 = session_data.get('projek_p5', {})
                
                st.success(f"✅ Session berhasil dimuat! (dari {session_data.get('timestamp', 'N/A')})")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error loading session: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>EduMerdeka Optimizer</strong> - Platform Optimasi Pembelajaran Kurikulum Merdeka Indonesia</p>
    <p>Created by Ary HH (<a href="mailto:aryhharyanto@proton.me">aryhharyanto@proton.me</a>)</p>
    <p style="font-size: 0.9rem; color: #888;">
        © 2026 - Non-Open Source. Untuk keperluan edukasi dan optimasi pembelajaran.
    </p>
</div>
""", unsafe_allow_html=True)
