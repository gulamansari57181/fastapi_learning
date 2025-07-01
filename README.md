# 🏥 FastAPI Patient Data API

A sleek and powerful RESTful API built with **FastAPI** to load, view, and sort patient records based on `height`, `weight`, or `BMI`. This project demonstrates clean design, error handling, and interactive API documentation.

---

## 🚀 Features

✅ Load patient data from a JSON file  
✅ View patient details by ID  
✅ Sort patients by height, weight, or BMI  
✅ Query-based sorting in ascending or descending order  
✅ Built-in validation and error handling  
✅ Swagger UI & Redoc API docs included  
✅ Minimal, clean, and beginner-friendly code

---

## 🔧 Tech Stack

- 🐍 Python 3.10+
- ⚡ FastAPI
- 🔁 Uvicorn (`--reload` for dev)
- 📄 JSON file-based dataset

---

## 📁 Project Structure

```bash
📦 FastAPI-Patient-API/
├── app.py              # Main FastAPI application
├── patient.json        # JSON file containing patient records
└── README.md           # You're reading it now 😄
```

---

## 🛠️ Setup Instructions

### 1. 🐍 Create and Activate a Virtual Environment

```bash
python -m venv myvenv
```

- **Windows:**
  ```bash
  myvenv\Scripts\activate
  ```

- **Linux/macOS:**
  ```bash
  source myvenv/bin/activate
  ```

### 2. 📦 Install Dependencies

```bash
pip install fastapi uvicorn
```

---

## ▶️ Run the Server

```bash
uvicorn app:app --reload
```

Open in browser:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📄 Sample `patient.json` Format

```json
{
  "p1": {"name": "Alice", "height": 160, "weight": 60, "bmi": 23.4},
  "p2": {"name": "Bob", "height": 170, "weight": 80, "bmi": 27.7},
  "p3": {"name": "Charlie", "height": 155, "weight": 50, "bmi": 20.8}
}
```

---

## 🔌 API Endpoints

### 🔍 `GET /view/{patient_id}`

Retrieve a specific patient’s details by ID.

**Example Request:**

```
GET /view/p2
```

**Example Response:**

```json
{
  "name": "Bob",
  "height": 170,
  "weight": 80,
  "bmi": 27.7
}
```

**Error (Invalid ID):**

```json
{
  "detail": "Patient not found"
}
```

---

### 🔃 `GET /sort`

Sort patients based on height, weight, or BMI.

#### ✅ Query Parameters:

| Parameter | Type   | Description                           |
|-----------|--------|---------------------------------------|
| `sort_by` | string | Must be one of: `height`, `weight`, `bmi` |
| `order`   | string | `asc` (default) or `desc`             |

#### ✅ Example 1: Ascending by BMI

```
GET /sort?sort_by=bmi&order=asc
```

**Response:**

```json
{
  "sorted_by": "bmi",
  "order": "asc",
  "patients": [
    {
      "name": "Charlie",
      "height": 155,
      "weight": 50,
      "bmi": 20.8
    },
    {
      "name": "Alice",
      "height": 160,
      "weight": 60,
      "bmi": 23.4
    },
    {
      "name": "Bob",
      "height": 170,
      "weight": 80,
      "bmi": 27.7
    }
  ]
}
```

---

#### ✅ Example 2: Descending by Height

```
GET /sort?sort_by=height&order=desc
```

**Response:**

```json
{
  "sorted_by": "height",
  "order": "desc",
  "patients": [
    {
      "name": "Bob",
      "height": 170,
      "weight": 80,
      "bmi": 27.7
    },
    {
      "name": "Alice",
      "height": 160,
      "weight": 60,
      "bmi": 23.4
    },
    {
      "name": "Charlie",
      "height": 155,
      "weight": 50,
      "bmi": 20.8
    }
  ]
}
```

---

#### ❌ Error Example: Invalid `sort_by`

```
GET /sort?sort_by=age
```

**Response:**

```json
{
  "detail": "Invalid sort_by value. Must be one of ['height', 'weight', 'bmi']"
}
```

---

## 🎯 Example CURL Requests

```bash
curl http://127.0.0.1:8000/view/p1

curl "http://127.0.0.1:8000/sort?sort_by=weight&order=desc"
```

---

## 🔥 Cool Badges

![FastAPI](https://img.shields.io/badge/FastAPI-async%20and%20fast-green?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)

---

## 🙌 Contribution

Pull requests are welcome! Feel free to fork the repo and submit improvements.

---

## 📫 Contact

Created with ❤️ by [Gulam Ansari](mailto:gulamansari57181@gmail.com)
