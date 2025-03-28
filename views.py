import os
import joblib
from django.shortcuts import render

# Load the trained model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file NOT found at: {MODEL_PATH}\nMake sure you have trained and saved the model!")

model = joblib.load(MODEL_PATH)

def home(request):
    return render(request, 'home.html')

def predict(request):
    return render(request, 'predict.html')

def result(request):
    if request.method == "POST":
        if "n1" in request.POST:
            val1 = float(request.POST.get('n1', 0))  
            val2 = float(request.POST.get('n2', 0))
            val3 = float(request.POST.get('n3', 0))
            val6 = float(request.POST.get('n6', 0))  
            val7 = float(request.POST.get('n7', 0))
            val8 = float(request.POST.get('n8', 0))

            pred = model.predict([[val1, val2, val3, 0, 0, val6, val7, val8]])

        elif "symptom1" in request.POST:
            symptom1 = int(request.POST.get("symptom1", 0))
            symptom2 = int(request.POST.get("symptom2", 0))
            symptom3 = int(request.POST.get("symptom3", 0))
            symptom4 = int(request.POST.get("symptom4", 0))
            lifestyle1 = int(request.POST.get("lifestyle1", 0))
            lifestyle2 = int(request.POST.get("lifestyle2", 0))
            lifestyle3 = int(request.POST.get("lifestyle3", 0))

            val1 = lifestyle3  
            val2 = 150 if symptom1 else 100  
            val3 = 130 if symptom2 else 80  
            val6 = 35 if lifestyle2 == 0 else 25  
            val7 = lifestyle3  
            val8 = 45  

            pred = model.predict([[val1, val2, val3, 0, 0, val6, val7, val8]])

        else:
            return render(request, 'predict.html', {"error": "Invalid form submission"})

        # Assign Risk Level
        if pred[0] == 1:
            risk_level = "POSITIVE"
        elif val2 > 140 or val6 > 30:
            risk_level = "MODERATE"
        else:
            risk_level = "NEGATIVE"

        return render(request, 'predict.html', {"result2": risk_level})