import os
import re

folder_path = "/Users/maria/PycharmProjects/PythonProject/udesa/I100/tutorial"
pattern = re.compile(r"(\d{1,2})-(\d{1,2})-(\d{2})(.*)\.py")

for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        day, month, year, rest = match.groups()
        day = day.zfill(2)
        month = month.zfill(2)
        year = year.zfill(2)
        new_name = f"{month}-{day}-{year}{rest}.py"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
        print(f"{filename} → {new_name}")
