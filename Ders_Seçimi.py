import streamlit as st
import pandas as pd
from helper import DAYS_OF_WEEK, TIME_SLOTS, generate_color, highlight_same_courses, save_schedule_as_image
from dersler import dersler

ders_df = pd.DataFrame(dersler)


ders_secenekleri = ders_df.apply(lambda row: f"{row['Code']} - {row['Name']}", axis=1)


st.title('🚀 Ders Programını Oluştur')


st.info('Bu uygulama portala bağlı değildir. Lütfen ders bilgilerinizi manuel olarak giriniz.', icon="ℹ️")

if 'lessons' not in st.session_state:
    st.session_state.lessons = pd.DataFrame(columns=['Ders Kodu', 'Gün', 'Saat', 'Section'])

if 'download_ready' not in st.session_state:
    st.session_state.download_ready = False


st.subheader('📘 Ders Ekle')
with st.form(key='lesson_form', clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
       
        secilen_ders = st.selectbox("Ders Kodu ve Adını Seçin:", ders_secenekleri)
     
        ders_kodu, _ = secilen_ders.split(" - ", 1)  # Sadece ders kodunu alıyoruz

        
        secilen_section = st.selectbox("Ders Kodu ve Adını Seçin:", {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15})
                          

    with col2:
        gun = st.selectbox('Gün Seçiniz', options=[''] + DAYS_OF_WEEK)
        saatler = st.multiselect('Saat Aralıklarını Seçiniz', options=TIME_SLOTS)

    submit_button = st.form_submit_button(label='➕ Ders Ekle')

    if submit_button:
        if ders_kodu and secilen_section and gun and saatler:
            for saat in saatler:
                new_lesson = pd.DataFrame({'Ders Kodu': [ders_kodu], 'Gün': [gun], 'Saat': [saat], 'Section': [secilen_section]})
                st.session_state.lessons = pd.concat([st.session_state.lessons, new_lesson], ignore_index=True)
            st.success(f'{ders_kodu} - Section {secilen_section} başarıyla eklendi!')
        else:
            st.error('Lütfen tüm alanları doldurun!')


if 'course_colors' not in st.session_state:
    st.session_state.course_colors = {}

if not st.session_state.lessons.empty:
    st.subheader('📚 Eklenen Dersler')
    
    lessons_df = st.session_state.lessons.reset_index(drop=True)

    # Her dersi seçilebilir şekilde listele
    selected_lessons = st.multiselect(
        'Silmek için ders(ler)i seçin:',
        lessons_df.index,
        format_func=lambda x: f"{lessons_df.iloc[x]['Ders Kodu']} - Section {lessons_df.iloc[x]['Section']} ({lessons_df.iloc[x]['Gün']}, {lessons_df.iloc[x]['Saat']})"
    )

    # Dersleri sil
    if selected_lessons and st.button('🗑️ Seçili Dersi Sil'):
        st.session_state.lessons.drop(selected_lessons, inplace=True)
        st.session_state.lessons.reset_index(drop=True, inplace=True)
        st.success('Seçili dersler başarıyla silindi!')

# Ders programı
st.subheader('📅 Ders Programı')

# Ders programı - tablo 
schedule = pd.DataFrame(index=TIME_SLOTS, columns=DAYS_OF_WEEK)

for _, lesson in st.session_state.lessons.iterrows():
    schedule.at[lesson['Saat'], lesson['Gün']] = f"{lesson['Ders Kodu']} - Sec {lesson['Section']}"

    if lesson['Ders Kodu'] not in st.session_state.course_colors:
        st.session_state.course_colors[lesson['Ders Kodu']] = generate_color()

# Tablo
st.write(schedule.fillna(' ').style.applymap(lambda val: highlight_same_courses(val, st.session_state.course_colors)))

# Ders programını indir
if not st.session_state.lessons.empty:
    if not st.session_state.download_ready:
        if st.button('💾 Ders Programını İndir (PNG)'):
            buf = save_schedule_as_image(schedule, st.session_state.course_colors)
            st.download_button(
                label="📥 Dosya Hazır, İndirin",
                data=buf,
                file_name="ders_programi.png",
                mime="image/png"
            )
            st.session_state.download_ready = True
    else:
        st.success("💾 Dosya başarıyla hazırlandı. İndirme işlemini tamamladınız.")
