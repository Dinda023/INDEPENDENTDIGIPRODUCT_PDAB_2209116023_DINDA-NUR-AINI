import streamlit as st
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle
import joblib

df = pd.read_csv('study performance.csv')
df_file = pd.read_csv('new study performance.csv')

# Sidebar
st.sidebar.title('Faktor dan Pengaruhnya Terhadap Skor Siswa')
selected_option = st.sidebar.selectbox('Select an option:', ['Dashboard', 'Distribution', 'Comparison', 'Composition', 'Relationship', 'Regresi'])

# Main content based on selected option
if selected_option == 'Dashboard':
    st.title("Dashboard")
    st.subheader("""
    Analisis Faktor-faktor yang Mempengaruhi Skor Tes Siswa
    """)

    # Mendefinisikan gambar
    gambar = 'image.jpg'

    # Menampilkan gambar dengan st.image()
    st.image(gambar, use_column_width=True)
    st.markdown("""
Proyek ini bertujuan untuk memahami bagaimana kinerja siswa (skor tes) dipengaruhi oleh variabel lain seperti Gender, Etnis, Tingkat Pendidikan Orang Tua, Makan Siang, dan Kursus Persiapan Ujian.

Deskripsi Kolom dalam Tabel:
                
- gender: Jenis kelamin siswa (Laki-laki/Perempuan)
                
- race/ethnicity: Etnis siswa (Kelompok A, B, C, D, E)
                
- parental level of education: Tingkat pendidikan terakhir orang tua siswa (gelar sarjana, beberapa perguruan tinggi, gelar magister, gelar associate, sekolah menengah atas)
                
- lunch: Makan siang sebelum ujian (standar atau gratis/diskon)
                
- test preparation course: Kelas persiapan tes sudah lengkap atau belum sebelum ujian
                
- math score: Nilai ujian matematika
                
- reading score: Nilai ujian membaca
                
- writing score: Nilai ujian menulis
                
Link dataset yang digunakan: https://www.kaggle.com/datasets/bhavikjikadara/student-study-performance
                """)
    
    st.subheader('Tabel')
    st.write(df)
elif selected_option == 'Distribution':
    st.subheader('Perbandingan Nilai MTK, Membaca, dan Menulis')
    
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram for math score
    ax.hist(df['math_score'], bins=10, color='b', alpha=0.7, label='Math Score')

    # Histogram for reading score
    ax.hist(df['reading_score'], bins=10, color='g', alpha=0.7, label='Reading Score')

    # Histogram for writing score
    ax.hist(df['writing_score'], bins=10, color='r', alpha=0.7, label='Writing Score')

    # Add labels and title
    ax.set_xlabel('Score', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title('Distribution of Scores')
    ax.legend()
    st.markdown(
"""Sumbu x mewakili skor, mulai dari 0 hingga 100, dan sumbu y mewakili frekuensi dari skor tersebut.

Setiap kategori direpresentasikan dengan warna yang berbeda:
- Skor Matematika ditunjukkan dengan warna biru,
- Skor Membaca ditunjukkan dengan warna hijau, dan
- Skor Menulis ditunjukkan dengan warna merah.

Batang histogram tumpang tindih, memungkinkan perbandingan antara distribusi frekuensi dari ketiga jenis skor tersebut. Nampaknya Skor Menulis memiliki frekuensi tertinggi di sebagian besar rentang skor, diikuti oleh Skor Membaca dan Skor Matematika."""
)
    # Show plot
    ax.grid(True)
    st.pyplot(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    st.subheader("Density Plot")
    # Plot each density plot
    sns.kdeplot(df['math_score'], shade=True, ax=axes[0, 0])
    axes[0, 0].set_title('Density Plot for Math Score')

    sns.kdeplot(df['reading_score'], shade=True, ax=axes[0, 1])
    axes[0, 1].set_title('Density Plot for Reading Score')

    sns.kdeplot(df['writing_score'], shade=True, ax=axes[1, 0])
    axes[1, 0].set_title('Density Plot for Writing Score')

    sns.kdeplot(df['average_score'], shade=True, ax=axes[1, 1])
    axes[1, 1].set_title('Density Plot for Average Score')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    st.pyplot(fig)
    st.markdown(
"""Setiap plot dilengkapi dengan judul yang menunjukkan jenis skor yang direpresentasikan:

1. Kiri atas: "Density Plot for Math Score"
2. Kanan atas: "Density Plot for Reading Score"
3. Kiri bawah: "Density Plot for Writing Score"
4. Kanan bawah: "Density Plot for Average Score"

Bentuk plot kepadatan menunjukkan bahwa skor tersebut sekitar terdistribusi secara normal, dengan puncak tunggal di mana sebagian besar skor terkonsentrasi di sekitar rata-rata. Plot untuk skor matematika, membaca, dan rata-rata memiliki bentuk yang mirip, dengan puncak di sekitar rentang skor 60-70. Distribusi skor menulis memiliki puncaknya sedikit ke kiri, menunjukkan bahwa skor menulis rata-rata mungkin lebih rendah dibandingkan dengan skor lainnya.
"""
)
elif selected_option == 'Comparison':
    st.title('Comparison')

    st.subheader('Histogram of Average Score by Gender')
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(df[df['gender'] == 'female']['average_score'], bins=10, alpha=0.7, label='Female', color='pink')
    ax.hist(df[df['gender'] == 'male']['average_score'], bins=10, alpha=0.7, label='Male', color='blue')
    ax.set_xlabel('Average Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Average Score by Gender')
    ax.legend()
    st.pyplot(fig)

    st.markdown(
    """Dari histogram tersebut, terlihat bahwa distribusi skor rata-rata antara siswa perempuan dan laki-laki cenderung berbeda. Skor rata-rata siswa perempuan memiliki puncak frekuensi yang lebih tinggi di sekitar 80-90, sementara skor rata-rata siswa laki-laki memiliki puncak frekuensi yang lebih rendah di sekitar 60-70.""")

    st.subheader('Box Plot of Average Score by Race/Ethnicity')
    fig = px.box(df, x='race_ethnicity', y='average_score', title='Average Score by Race/Ethnicity')
    st.plotly_chart(fig)

    st.markdown("""Dari diagram tersebut, terlihat bahwa terdapat perbedaan skor rata-rata yang signifikan antara kelompok ras/etnis. Kelompok E memiliki skor rata-rata tertinggi, diikuti oleh kelompok D, C, B, dan A. Hal ini menunjukkan bahwa terdapat disparitas dalam skor rata-rata siswa antar kelompok ras/etnis yang diwakili dalam diagram.""")

    st.subheader('Box Plot of Average Score by Parental Level of Education')
    fig = px.box(df, x='parental_level_of_education', y='average_score', title='Average Score by Parental Level of Education')
    st.plotly_chart(fig)

    st.markdown("""Dari diagram tersebut, terlihat bahwa skor rata-rata cenderung meningkat seiring dengan tingkat pendidikan orang tua yang lebih tinggi. Orang tua dengan gelar master cenderung memiliki skor rata-rata tertinggi, diikuti oleh associate's degree, bachelor's degree, some college, high school, dan some high school.""")
    
    st.subheader("Histogram Perbandingan Average Score antar Lunch")
    fig = px.histogram(df, x='average_score', color='lunch',
                   labels={'average_score': 'Average Score'})
    fig.update_layout(barmode='overlay')
    st.plotly_chart(fig)

    st.markdown("""Dari histogram tersebut, terlihat bahwa untuk kategori makan siang "standard," distribusi skor rata-rata cenderung lebih tinggi, dengan puncak frekuensi terletak di sekitar 80-90. Sedangkan untuk kategori makan siang "free/reduced," distribusi skor rata-rata cenderung lebih rendah, dengan puncak frekuensi terletak di sekitar 60-70.""")

    # Visualisasi bar stacked untuk perbandingan average_score antar test_preparation_course
    st.subheader('Histogram of Average Score by Test Preparation Course')
    # Histogram
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(df[df['test_preparation_course'] == 'none']['average_score'], bins=10, alpha=0.7, label='None', color='skyblue')
    ax.hist(df[df['test_preparation_course'] == 'completed']['average_score'], bins=10, alpha=0.7, label='Completed', color='orange')
    ax.set_xlabel('Average Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Average Score by Test Preparation Course')
    ax.legend()
    st.pyplot(fig)
 
    st.markdown("""Dari histogram tersebut, terlihat bahwa distribusi skor rata-rata antara siswa perempuan dan laki-laki cenderung berbeda. Skor rata-rata siswa perempuan memiliki puncak frekuensi yang lebih tinggi di sekitar 80-90, sementara skor rata-rata siswa laki-laki memiliki puncak frekuensi yang lebih rendah di sekitar 60-70.""")

elif selected_option == 'Composition':
    st.title('Composition')

    # Hitung jumlah data untuk setiap gender
    gender_counts = df['gender'].value_counts()

    st.subheader("Pie Chart Perbandingan Jumlah Data antar Gender")
    # Visualisasi pie chart perbandingan jumlah data antar gender
    fig = px.pie(values=gender_counts, names=gender_counts.index)
    st.plotly_chart(fig)

    st.markdown("""Terdapat sedikit lebih banyak jumlah laki-laki dibandingkan perempuan dalam populasi yang diwakili dalam gambar tersebut.""")

    st.subheader("Bar Plot Perbandingan Jumlah Data antar Race/Ethnicity")
    race_counts = df['race_ethnicity'].value_counts()

    # Plot diagram batang
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(race_counts.index, race_counts.values, color=['blue', 'orange', 'green', 'red', 'purple'])
    ax.set_xlabel('Race/Ethnicity')
    ax.set_ylabel('Count')
    ax.set_title('Race/Ethnicity Distribution')

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    st.markdown("""Grafik tersebut menunjukkan jumlah siswa dalam kelompok ras/etnis yang berbeda, dengan kelompok E memiliki jumlah siswa terbanyak diikuti oleh kelompok D, C, B, dan A.""")

    st.subheader("Bar Plot Perbandingan Jumlah Data antar Parental Level of Education")
    education_counts = df['parental_level_of_education'].value_counts()

    # Plot diagram batang
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(education_counts.index, education_counts.values, color='skyblue')
    ax.set_xlabel('Parental Level of Education')
    ax.set_ylabel('Count')
    ax.set_title('Parental Level of Education Distribution')

    # Atur rotasi label x agar lebih renggang
    plt.xticks(rotation=45, ha='right')

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

    st.markdown("""Grafik tersebut menunjukkan distribusi tingkat pendidikan orang tua (Parental Level of Education) dalam jumlah siswa, dengan some college dan associate's degree memiliki jumlah siswa terbanyak.""")

    st.subheader("Pie Chart Perbandingan Jumlah Data antar Kategori Lunch")
    # Hitung jumlah data berdasarkan lunch
    lunch_counts = df['lunch'].value_counts()

    # Visualisasi pie chart perbandingan jumlah data antar lunch
    fig = px.pie(values=lunch_counts, names=lunch_counts.index)
    st.plotly_chart(fig)

    st.markdown("""Grafik menunjukkan distribusi status makanan siswa, dengan persentase 34.9% siswa menerima makanan berbayar (standard) dan 65.1% siswa menerima makanan gratis atau dengan diskon (free/reduced).""")

    test_preparation_counts = df['test_preparation_course'].value_counts()

    # Visualisasi bar stack
    st.subheader('Stacked Bar Chart Perbandingan Jumlah Data antar Kategori Test Preparation Course')
    fig = px.bar(df, x='test_preparation_course', color='gender', barmode='stack')
    st.plotly_chart(fig)

    st.markdown("""Grafik tersebut menunjukkan informasi status kelulusan kursus persiapan none yang jauh lebih banyak dari complete.""")

elif selected_option == 'Relationship':
    st.title('Relationship')

    correlation_matrix = df_file.corr()

    # Visualisasi heatmap korelasi
    st.subheader('Heatmap Korelasi')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Heatmap Korelasi')
    st.pyplot(fig)

    st.markdown(
"""Setiap sel dalam matriks mewakili koefisien korelasi antar variabel, berkisar dari -1 hingga 1, dengan 1 menunjukkan korelasi positif sempurna, -1 menunjukkan korelasi negatif sempurna, dan 0 menunjukkan tidak ada korelasi.

Skala warna di sisi kanan berkisar dari merah gelap (korelasi positif) hingga putih (tidak ada korelasi) hingga biru gelap (korelasi negatif). Korelasi terkuat dalam matriks tersebut adalah antara skor ujian itu sendiri (matematika, membaca, menulis, dan skor rata-rata), yang ditunjukkan dalam warna merah gelap, menunjukkan korelasi positif tinggi (nilai sekitar 0,8 hingga 0,97). Variabel lain menunjukkan korelasi yang lebih lemah dengan skor dan satu sama lain, dengan nilai mendekati nol atau sedikit negatif atau positif, seperti yang ditunjukkan oleh warna yang lebih terang.

Variabel di sepanjang bagian bawah dan sisi kiri bersifat simetris, karena matriks tersebut simetris sepanjang diagonal dari kiri atas ke kanan bawah, yang mewakili korelasi setiap variabel dengan dirinya sendiri, oleh karena itu warna merah gelap 1.0 sepanjang diagonal ini."""
)

elif selected_option == 'Regresi':
    st.title('Regresi')

    try:
        model = joblib.load('lrr_model.pkl')
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'lr_model.pkl' exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.stop()

    # Streamlit app interface
    st.header("Input Features")

    gender = st.selectbox("Gender", [0, 1])
    race_ethnicity = st.selectbox("Race/Ethnicity", [0, 1, 2, 3, 4])
    parental_level_of_education = st.selectbox("Parental Level of Education", [0, 1, 2, 3, 4])
    lunch = st.selectbox("Lunch", [0, 1])
    test_preparation_course = st.selectbox("Test Preparation Course", [0, 1])

    # Make prediction
    if st.button("Predict"):
        # Convert input features into DataFrame
        input_data = pd.DataFrame({
            'gender': [gender],
            'race_ethnicity': [race_ethnicity],
            'parental_level_of_education': [parental_level_of_education],
            'lunch': [lunch],
            'test_preparation_course': [test_preparation_course]
        })

        try:
            # Make prediction using the model
            prediction = model.predict(input_data)
            st.write(f"Predicted Average Score: {prediction[0]}")
        except Exception as e:
            st.error(f"Error making prediction: {e}")
