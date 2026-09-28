
import csv
from datetime import date, timedelta
import random

start_date = date(2026, 1, 1)

with open("study_data.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow(["date", "value", "memo"])

    for i in range(100):
        study_date = start_date + timedelta(days=i)
        study_time = random.randint(1, 5)

        if study_date.weekday() >= 5:
            study_time = random.randint(0, 3)

        memo = "공부 기록"

        writer.writerow([
            study_date,
            study_time,
            memo
        ])

print("공부시간 데이터 100개 생성 완료!")