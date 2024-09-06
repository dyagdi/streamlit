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
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')


    table = ax.table(cellText=schedule.fillna('').values, colLabels=schedule.columns, rowLabels=schedule.index, cellLoc='center', loc='center')


    for i in range(len(schedule.index)):
        for j in range(len(schedule.columns)):
            cell_value = schedule.iloc[i, j]
            if pd.notna(cell_value) and cell_value != '': 
                course_code = cell_value.split(' - ')[0]
                color = course_colors.get(course_code, "#FFFFFF")  
                table[(i+1, j)].set_facecolor(color)  
            else:
                table[(i+1, j)].set_facecolor("#FFFFFF")  


    plt.title("ODTÜ Ders Programı")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf
