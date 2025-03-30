import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template

# Load trained model and scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input (excluding Region, Climate_Condition, and Year)
        data = [float(request.form.get(key)) for key in [
            "avg_temp", "co2", "traffic", "population", "urbanization", "green_cover"
        ]]

        # Convert input to DataFrame
        df = pd.DataFrame([data])

        # Scale input data
        df_scaled = scaler.transform(df)

        # Make prediction
        prediction = model.predict(df_scaled)[0]

        return render_template("index.html", prediction_text=f"🌍 Predicted Climate Change Index: {prediction:.4f}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
