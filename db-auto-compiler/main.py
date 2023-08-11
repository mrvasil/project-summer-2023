import pandas as pd
sheet_name = "Контакты учеников"
skiprows = None
header = 0
names = None
usecols = ["Класс", "Фамилия", "Имя", "Отчество"]
dtype = None
df = pd.read_excel("C:/Users/alexe/Desktop/Alexey/Projects/project-summer-2023/db-auto-compiler/Силаэдр 2022-23.xlsx")
print(df)