from flask import Flask, render_template, request, abort
import requests
import json
app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)


def get_data():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        abort(500, description="Failed to fetch data from the API.")

data = get_data()
with open("pokedex.json", 'w') as file:
    file_data = json.load(file)
    file_data["animals"].append(data)
    file.seek(0)
    json.dump(file_data, file, indent=4)