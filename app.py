import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__)

# Load trained model and scaler safely
model_path = "model.pkl"
scaler_path = "scaler.pkl"

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    raise FileNotFoundError("❌ Model or scaler file not found!")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract input values safely
        input_keys = ["avg_temp", "co2", "traffic", "population", "urbanization", "green_cover"]
        data = []

        for key in input_keys:
            value = request.form.get(key)
            if value is None or value.strip() == "":
                return render_template("index.html", prediction_text=f"❌ Missing input: {key}")

            data.append(float(value))

        # Convert input to DataFrame & scale it
        df_scaled = scaler.transform(pd.DataFrame([data]))

        # Make prediction
        prediction = model.predict(df_scaled)[0]

        return render_template("index.html", prediction_text=f"🌍 Predicted Climate Change Index: {prediction:.4f}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Remove debug=True for production
