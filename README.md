# 🏦 Loan Repayment Risk Prediction

A comprehensive machine learning project to predict loan repayment risk using Logistic Regression.

## 📋 Project Overview

This project analyzes historical loan data to predict whether a borrower is likely to repay or default on their loan. It uses data analytics and machine learning techniques to help financial institutions make better lending decisions.

**Domain:** Data Analytics & Machine Learning  
**Algorithm:** Logistic Regression (Binary Classification)

## 🗂️ Project Structure

```
loan_risk_prediction/
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py    # Data cleaning and feature engineering
│   ├── model.py                 # Logistic Regression model
│   └── evaluation.py            # Metrics and visualizations
├── models/
│   ├── loan_risk_model.pkl      # Trained model
│   └── scaler.pkl               # Feature scaler
├── notebooks/
│   └── Loan_Risk_Analysis.ipynb # Jupyter analysis notebook
├── outputs/
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── feature_importance.png
├── main.py                      # Training pipeline
├── app.py                       # Streamlit web application
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### 1. Clone & Setup
```bash
git clone <repository-url>
cd loan_risk_prediction
python -m venv venv
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
```bash
python main.py
```
This will generate:
- `models/loan_risk_model.pkl` - Trained Logistic Regression model
- `models/scaler.pkl` - Feature scaler for normalization
- `outputs/` - Performance plots (Confusion Matrix, ROC Curve)

### 4. Launch Web Application
```bash
streamlit run app.py
```
The app will open at `http://localhost:8502`

### 5. Explore Analysis
```bash
jupyter notebook notebooks/Loan_Risk_Analysis.ipynb
```

## 🎯 Dashboard Features

**Interactive Risk Assessment:**
- Adjust loan parameters with intuitive sliders
- Real-time risk prediction (Low/Medium/High)
- Visual risk gauge for quick assessment

**Analytics Tab:**
- Model accuracy metrics
- Confusion matrix visualization
- ROC curve analysis
- Feature importance rankings

## 📊 Dataset Features

| Feature | Description |
|---------|-------------|
| age | Borrower's age (21-64) |
| income | Annual income |
| loan_amount | Loan amount requested |
| credit_score | Credit score (300-850) |
| employment_years | Years of employment |
| existing_loans | Number of existing loans |
| loan_term | Loan term in months |
| interest_rate | Interest rate (%) |
| **default** | Target: 0=Repay, 1=Default |

## 🔬 Engineered Features

- **debt_to_income**: Loan amount / Income ratio
- **monthly_payment**: Estimated monthly payment
- **payment_to_income**: Monthly payment / Monthly income ratio
- **risk_score**: Composite risk indicator

## 📈 Model Performance

After training, the model achieves:
- **Accuracy**: ~75-80%
- **Precision**: High precision for identifying defaults
- **ROC-AUC**: Good discrimination ability

## ✅ Project Status

**✨ FULLY OPERATIONAL** - All development and deployment phases complete:
- ✅ Machine Learning pipeline implemented
- ✅ Training script ready (`main.py`)
- ✅ Interactive web dashboard deployed (`app.py`)
- ✅ Model artifacts generated (`models/`)
- ✅ Performance visualizations created (`outputs/`)
- ✅ Jupyter notebook for EDA available (`notebooks/`)

**Live Dashboard:** Available at `http://localhost:8502` after running `streamlit run app.py`

## 👥 Team

- B. Prakash Reddy (22781A3324)
- C. Sai Prakash Reddy (22781A3330)
- D. Jakeer (22781A3333)
- D.S. Pranay Kumar (22781A3334)
- K. Santhosh (22781A3361)

**Guide:** Mr. K. Anjaneyulu  
**College:** Sri Venkateswara College Of Engineering & Technology  
**Academic Year:** 2025-2026

## 📄 License

This project is for educational purposes.
