import random
import pandas as pd
import matplotlib.pyplot as plt
import io


DAYS_OF_WEEK = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
TIME_SLOTS = ['08:40-09:30', '09:40-10:30', '10:40-11:30', '11:40-12:30', '12:40-13:30', '13:40-14:30', '14:40-15:30', '15:40-16:30', '16:40-17:30']


def generate_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def highlight_same_courses(val, course_colors):
    course_code = val.split(' - ')[0] if pd.notna(val) else ''
    return f'background-color: {course_colors.get(course_code, "")}'

def save_schedule_as_image(schedule, course_colors):
    # Şık görsel boyutlarını ayarla
    fig, ax = plt.subplots(figsize=(14, 8))  # Boyutları biraz büyüttük
    
    # Eksenleri kapat
    ax.axis('tight')
    ax.axis('off')
    
    # Tablo oluştur
    table = ax.table(cellText=schedule.fillna('').values,
                     colLabels=schedule.columns,
                     rowLabels=schedule.index,
                     cellLoc='center',
                     loc='center')

    # Tablo hücrelerine stil ekle
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # Yazı boyutunu ayarladık
    table.scale(1.2, 1.2)  # Hücrelerin boyutlarını ayarladık
    
    # Hücre kenarlarını ve arkaplanlarını ayarla
    for i in range(len(schedule.index)):
        for j in range(len(schedule.columns)):
            cell_value = schedule.iloc[i, j]
            cell = table[(i + 1, j)]
            
            # Eğer hücre doluysa renklendir
            if pd.notna(cell_value) and cell_value != '':
                course_code = cell_value.split(' - ')[0]
                color = course_colors.get(course_code, "#d3d3d3")  # Varsayılan rengi gri yaptık
                cell.set_facecolor(color)
                cell.set_edgecolor('black')  # Kenarları siyah yaptık
            else:
                # Boş hücreler için varsayılan beyaz rengi
                cell.set_facecolor("#f0f0f0")  # Daha şık bir beyaz tonu
                cell.set_edgecolor('black')

    # Tablo başlığını stilize et
    plt.title("Ders Programı", fontsize=16, fontweight='bold', pad=20)
    
    # Görseli bir buffer'a kaydet
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)  # DPI değeriyle kaliteyi artırdık
    buf.seek(0)
    
    return buf
