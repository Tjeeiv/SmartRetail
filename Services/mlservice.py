import pandas as pd
import logging
from Services.ingestservice import getengine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
 
import joblib
import os

MODEL_DIR = "./models"
os.makedirs(MODEL_DIR, exist_ok=True)

def monthlyfeatures():

    df = pd.read_sql ("select * from gold.sales" , getengine() )

    df['monthnumber'] = pd.to_datetime(df['yearmonth']).dt.month

    encoded = pd.get_dummies(df["monthnumber"], prefix="month")
    df = pd.concat([df, encoded], axis=1)
    df = df.drop(columns=["monthnumber"])
    df["target"] = df["MonthlyRevenue"].shift(-1)

    df = df.dropna(subset=["target"])

    return df


def trainmodel():
    df = monthlyfeatures()
  
 

    X = df.drop(columns=["target","yearmonth"])
    y = df["target"]

    scaler = StandardScaler()
    numeric_cols = ["MonthlyRevenue", "Invoicecount",   "monAvgRev"]
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)
    
    joblib.dump(model, f"{MODEL_DIR}/linear_regression.pkl")
    joblib.dump(scaler, f"{MODEL_DIR}/scaler.pkl")
    joblib.dump(list(X.columns), f"{MODEL_DIR}/feature_columns.pkl")

    predictions = model.predict(X_test)

    return {
        "r2_score": r2_score(y_test, predictions),
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions) ** 0.5
    }


def predictrevenue(input_features: dict):
    model = joblib.load(f"{MODEL_DIR}/linear_regression.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    feature_columns = joblib.load(f"{MODEL_DIR}/feature_columns.pkl")
    
    # build DataFrame from input
    df = pd.DataFrame([input_features])
    # reindex to match training columns
    df = df.reindex(columns=feature_columns, fill_value=0)
    # scale numeric columns
    numeric_cols = ["MonthlyRevenue", "Invoicecount",   "monAvgRev"]
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    prediction = model.predict(df)
    return float(prediction[0])
     