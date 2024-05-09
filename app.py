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
st.sidebar.title('Halaman')
selected_option = st.sidebar.selectbox('Select an option:', ['Dashboard', 'Distribution', 'Comparison', 'Composition', 'Relationship', 'Regresi'])

# Main content based on selected option
if selected_option == 'Dashboard':
    st.title("Dashboard")
    st.subheader("""
    Analisis Faktor-faktor yang Mempengaruhi Skor Tes Siswa
    """)
    st.text('Tabel')
    st.write(df)
    st.markdown("""
Tujuan:
Proyek ini bertujuan untuk memahami bagaimana kinerja siswa (skor tes) dipengaruhi oleh variabel lain seperti Gender, Etnis, Tingkat Pendidikan Orang Tua, Makan Siang, dan Kursus Persiapan Ujian.

Deskripsi Data:
Data yang digunakan dalam analisis ini berisi informasi tentang skor tes matematika, membaca, dan menulis siswa, serta beberapa atribut lainnya seperti gender, ras/etnis, tingkat pendidikan orang tua, makan siang, dan apakah siswa mengikuti kursus persiapan ujian atau tidak.
                """)
elif selected_option == 'Distribution':
    st.title('Perbandingan Nilai MTK, Membaca, dan Menulis')
    
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

    # Show plot
    ax.grid(True)
    st.pyplot(fig)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

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

elif selected_option == 'Comparison':
    st.title('Comparison')

    fig = px.bar(df, x='gender', y='average_score', title='Perbandingan Average Score antar Gender', 
             labels={'gender': 'Gender', 'average_score': 'Average Score'})
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

    fig = px.bar(df, x='race_ethnicity', y='average_score', title='Bar Plot Perbandingan Average Score antar Race/Ethnicity',
             labels={'race_ethnicity': 'Race/Ethnicity', 'average_score': 'Average Score'})
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

    fig = px.bar(df, x='parental_level_of_education', y='average_score', title='Bar Plot Perbandingan Average Score antar Parental Level of Education',
             labels={'parental_level_of_education': 'Parental Level of Education', 'average_score': 'Average Score'})
    st.plotly_chart(fig)

    fig = px.histogram(df, x='average_score', color='lunch', title='Histogram Perbandingan Average Score antar Lunch',
                   labels={'average_score': 'Average Score'})
    fig.update_layout(barmode='overlay')
    st.plotly_chart(fig)

    # Visualisasi bar stacked untuk perbandingan average_score antar test_preparation_course
    fig = px.bar(df, x='test_preparation_course', y='average_score', color='gender', barmode='stack',
                title='Stacked Bar Chart Perbandingan Average Score antar Test Preparation Course')
    st.plotly_chart(fig)

elif selected_option == 'Composition':
    st.title('Composition')

    # Hitung jumlah data untuk setiap gender
    gender_counts = df['gender'].value_counts()

# Visualisasi pie chart perbandingan jumlah data antar gender
    fig = px.pie(values=gender_counts, names=gender_counts.index, title='Pie Chart Perbandingan Jumlah Data antar Gender')
    st.plotly_chart(fig)

    race_counts = df['race_ethnicity'].value_counts()

    # Plot diagram batang
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(race_counts.index, race_counts.values, color=['blue', 'orange', 'green', 'red', 'purple'])
    ax.set_xlabel('Race/Ethnicity')
    ax.set_ylabel('Count')
    ax.set_title('Race/Ethnicity Distribution')

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

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

    # Hitung jumlah data berdasarkan lunch
    lunch_counts = df['lunch'].value_counts()

    # Visualisasi pie chart perbandingan jumlah data antar lunch
    fig = px.pie(values=lunch_counts, names=lunch_counts.index, title='Pie Chart Perbandingan Jumlah Data antar Lunch')
    st.plotly_chart(fig)

    test_preparation_counts = df['test_preparation_course'].value_counts()

    # Plot diagram batang
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(test_preparation_counts.index, test_preparation_counts.values, color=['blue', 'orange'])
    ax.set_xlabel('Test Preparation Course')
    ax.set_ylabel('Count')
    ax.set_title('Test Preparation Course Distribution')

    # Tampilkan plot di Streamlit
    st.pyplot(fig)

elif selected_option == 'Relationship':
    st.title('Relationship')

    correlation_matrix = df_file.corr()

    # Visualisasi heatmap korelasi
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Heatmap Korelasi')

    # Menampilkan plot dengan Streamlit
    st.pyplot()

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