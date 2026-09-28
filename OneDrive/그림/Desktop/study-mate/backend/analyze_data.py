
import csv

with open("study_data.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    data = list(reader)

study_times = []

for item in data:
    study_times.append(int(item["value"]))

count = len(study_times)
total = sum(study_times)
average = total / count
maximum = max(study_times)
minimum = min(study_times)

recent = study_times[-7:]
previous = study_times[-14:-7]

recent_average = sum(recent) / len(recent)
previous_average = sum(previous) / len(previous)

print("===== 공부시간 분석 결과 =====")
print("전체 기록 개수:", count, "개")
print("총 공부시간:", total, "시간")
print("평균 공부시간:", round(average, 2), "시간")
print("최대 공부시간:", maximum, "시간")
print("최소 공부시간:", minimum, "시간")

print("최근 7일 평균:", round(recent_average, 2), "시간")
print("이전 7일 평균:", round(previous_average, 2), "시간")

if recent_average > previous_average:
    print("최근 추세: 공부시간 증가")
elif recent_average < previous_average:
    print("최근 추세: 공부시간 감소")
else:
    print("최근 추세: 공부시간 유지")