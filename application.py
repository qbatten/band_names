from flask import Flask, jsonify, render_template, request
import json
from random import randint, shuffle

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
        shuffle(band_names)
        # Generate CSS
        gen_css = []
        for i, item in enumerate(band_names):
            # Randomization
            rand_1 = randint(5, 600)
            rand_2 = randint(0, 40)
            r = lambda: randint(0,255)
            color = format('#%02X%02X%02X' % (r(),r(),r()))
            fontrand = lambda: randint(0, len(fonts))
            font = fonts[fontrand]
            # Create individual CSS string
            tmp = "#name-" + str(i) + "{width:10%; padding-left: " + str(rand_1) + "px; padding-top: " + str(rand_2) + "px; color: " + color + "; font-family: " + font + ";}"
            gen_css.append(tmp)
        return render_template("index.html",
                               band_names=band_names,
                               gen_css=gen_css)
    if request.method == "POST":
        band_names.append(request.form["contents"])
        return redirect(url_for('index'))