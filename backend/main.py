
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
import csv
import uuid
import os

app = FastAPI(title="Study Mate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "study_data.csv"


class StudyData(BaseModel):
    date: date
    value: float
    memo: str = ""


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def save_data(data):
    with open(DATA_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "date", "value", "memo"]
        )
        writer.writeheader()
        writer.writerows(data)


@app.get("/")
def home():
    return {"message": "Study Mate API is running!"}


@app.get("/api/data")
def get_data():
    return load_data()


@app.post("/api/data")
def add_data(item: StudyData):
    data = load_data()

    new_item = {
        "id": str(uuid.uuid4()),
        "date": str(item.date),
        "value": item.value,
        "memo": item.memo
    }

    data.append(new_item)
    save_data(data)

    return {"message": "공부 기록 추가 완료", "data": new_item}


@app.put("/api/data/{item_id}")
def update_data(item_id: str, item: StudyData):
    data = load_data()

    for row in data:
        if row["id"] == item_id:
            row["date"] = str(item.date)
            row["value"] = item.value
            row["memo"] = item.memo

            save_data(data)
            return {"message": "공부 기록 수정 완료"}

    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")


@app.delete("/api/data/{item_id}")
def delete_data(item_id: str):
    data = load_data()
    new_data = [row for row in data if row["id"] != item_id]

    if len(data) == len(new_data):
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")

    save_data(new_data)
    return {"message": "공부 기록 삭제 완료"}


@app.get("/api/data/summary")
def get_summary():
    data = load_data()

    if not data:
        return {"count": 0, "total": 0, "average": 0, "max": 0, "min": 0}

    study_times = [float(item["value"]) for item in data]

    return {
        "count": len(study_times),
        "total": sum(study_times),
        "average": round(sum(study_times) / len(study_times), 2),
        "max": max(study_times),
        "min": min(study_times)
    }