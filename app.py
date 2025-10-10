from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))

FEATURE_TYPES = {
    "hs" : "int",
    "previous_scores" : "float",
    "ecState" : "str",
    "Sleep_Hours" : "int",
    "Paper_Practice" : "int"
}

def cast_values(name,raw):
    t = FEATURE_TYPES.get(name,"str")

    if raw is None or raw  == "":
        raise ValueError(f"'{name}' can't be empty like your brain")
    
    if t == "float":
        return float(raw)
    
    if t == "int":
        return int(raw)
    
    if t == "str": 
        if raw.lower() == "yes":
            return 1
        elif raw.lower() == "no":
            return 0
        else:
            raise ValueError(f"Invalid value for {name}: {raw}")
    
    return str(raw)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ["GET","POST"])
def predict():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
            inputs = []
            for name in FEATURE_TYPES.keys():
                raw_val = request.form.get(name)
                clean_val = cast_values(name,raw_val)
                inputs.append(clean_val)

            prediction = model.predict([inputs])[0]

            return render_template("index.html", prediction_text=f"PREDICTED SCORE: {prediction:.2f}")
if __name__ == "__main__":
    app.run(debug=True)
