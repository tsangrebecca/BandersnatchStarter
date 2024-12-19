''' when running this file to open webpage, make sure cd to bandersnatchstarter,
run pipenv shell to turn on virtual environment,
and type $ py -m app.main to rerun the file with all the packages and imports'''

from base64 import b64decode
import os

import random
from MonsterLab import Monster
from flask import Flask, render_template, request
from pandas import DataFrame

from dotenv import load_dotenv # loading environment variables

from app.data import Database
from app.graph import chart
from app.machine import Machine



# Load environment variables from .env file
load_dotenv()

SPRINT = 3
APP = Flask(__name__)

# configure the app
APP.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
APP.config['MONGO_URL'] = os.getenv('MONGO_URL')

# MongoDB connection string from .env
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL is not set in your environment variables.")

# Pass the connection string to the Database class
# db = Database(MONGO_URL)

@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    # Just return the empty .html webpage with no data
    if SPRINT < 1:
        return render_template("data.html")
    print("trying to connect db now")
    db = Database()
    print(f"db ${db}")
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")
    
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]

    # Fetch the dataframe
    df = db.dataframe()

    # Convert the _id (ObjectId) to string because
    #   MongoDB's _id field is stored as an ObjectID, not directly
    #   serializable to JSON, but Altair is trying to convert the df to JSON
    #   Hence we have to convert ObjectID to a string in my df before passing
    #   it to the Altair chart
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)

    # Generate the chart, Altair uses JSON    
    graph = chart(
        # df=db.dataframe(),
        df=df,
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()

    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )

@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("app", "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    stats = [round(random.uniform(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random.randint(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    info = machine.info()
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )


# if __name__ == '__main__':
#     # Use a production-ready WSGI server like Gunicorn or uWSGI in production
#     APP.run(host="0.0.0.0", port=5000)
