from flask import Flask, jsonify, render_template, request, redirect
import json
from random import randint, shuffle
from re import sub

# Configure app
app = Flask(__name__)

with open('static/bandnames.json', 'r') as f:
    band_names = json.load(f)

fonts = ["Times New Roman", "Book Antiqua", "Gadget", "Arial", "Comic Sans MS",
         "Impact", "Courier New"]

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    """Render main page"""
    if request.method == "GET":
        # Get band names
        band_names_tmp = band_names[:]
        shuffle(band_names_tmp)
        # Generate CSS
        gen_css = []
        prev = randint(2, 80)
        rand_1 = randint(-10, 10)
        for i, item in enumerate(band_names_tmp):
            # Randomization
            rand_1 = randint(-50, 50)
            while (prev + rand_1) < 0 or (prev + rand_1) > 80:
                rand_1 = randint(-50, 50)
            rand_2 = randint(0, 40)
            r = lambda: randint(0,255)
            color = format('#%02X%02X%02X' % (r(),r(),r()))
            fontrand = randint(0, len(fonts) - 1)
            font = fonts[fontrand]
            # Create individual CSS string
            tmp = "#name-"
            tmp.join(str(i))
            tmp.join("{width:10%; padding-left: ")
            tmp.join(str(prev + rand_1))
            tmp.join("%; padding-top: ")
            tmp.join(str(rand_2))
            tmp.join("px; color: ")
            tmp.join(color)
            tmp.join("; font-family: ")
            tmp.join(font)
            tmp.join(";}")
            gen_css.append(tmp)
        return render_template("index.html",
                               band_names=band_names_tmp,
                               gen_css=gen_css)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")

    if request.method == "POST":
        submission = request.form.get("bandname")
        submission = sub(r'[^\w\. ]*', '', submission)
        band_names.append(submission)
        with open('static/bandnames.json', 'w') as f:
            json.dump(band_names, f)
        return redirect('/')