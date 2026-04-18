# 🩺 Disease Prediction Web App

A Machine Learning-based web application that predicts possible diseases based on user-selected symptoms. Built using **Flask** and **Scikit-learn**, this project provides real-time predictions, probability scores, and basic medical guidance.

---

## 🚀 Features

* 🔍 Predicts **Top 3 possible diseases**
* 📊 Displays **probability (%) for each prediction**
* 🧠 Provides **reason for prediction** (based on selected symptoms)
* 🏥 Suggests **medical advice**
* ⚠️ Prevents prediction if no symptoms are selected
* 📈 Interactive **bar chart visualization**
* 💻 Clean and user-friendly UI

---

## 🧰 Technologies Used

* **Python**
* **Flask**
* **Pandas**
* **Scikit-learn**
* **HTML, CSS, JavaScript**
* **Chart.js**

---

## 📁 Project Structure

```
Disease-Prediction/
│
├── app.py
├── Dataset.csv
├── requirements.txt
├── .gitignore
│
└── templates/
    └── index.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/Disease-Prediction.git
cd Disease-Prediction
```

### 2️⃣ Create virtual environment (optional)

```
python -m venv .venv
.venv\Scripts\activate   (Windows)
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the application

```
python app.py
```

### 5️⃣ Open in browser

```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

1. User selects symptoms via checkboxes
2. Input is converted into numerical format (0/1)
3. Machine Learning model predicts probabilities
4. Top 3 diseases are displayed
5. Explanation and advice are generated

---

## 📊 Model Details

* Algorithm: **Random Forest Classifier**
* Training Data: Custom generated dataset
* Output:

  * Top 3 predictions
  * Probability scores
  * Explanation based on symptoms

---

## ⚠️ Disclaimer

This project is for **educational purposes only** and should not be used as a substitute for professional medical advice.

---

## 🚀 Future Improvements

* Add real medical dataset
* Improve model accuracy
* Add login & patient history
* Deploy as full-stack application
* Mobile responsiveness

---

## 👨‍💻 Author

**Kausha4ll**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
