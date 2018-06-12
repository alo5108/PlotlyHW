# import necessary libraries
import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///DataSets/Belly_Button_Biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
BB_sample = Base.classes.samples
BB_otu=Base.classes.otu
Meta=Base.classes.samples_metadata
session=Session(engine)

#################################################
# Flask Routes
#################################################
app = Flask(__name__)

#create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/names')

def names():
    results = BB_sample.__table__.columns.keys()

    return jsonify(results)

@app.route('/otu')

def otu():
    results = session.query(BB_otu.lowest_taxonomic_unit_found).all()

    olist= list(np.ravel(results))

    return jsonify(olist)

@app.route('/meta')
def meta():
    results = session.query(Meta.AGE,Meta.BBTYPE,Meta.ETHNICITY,Meta.GENDER,Meta.LOCATION,Meta.SAMPLEID).all()
    for res in results:
        data=[]
        data.append ({
            "Age": [res[0]],
            "BB Type": [res[1]],
            "Ethnicity": [res[2]],
            "Gender": [res[3]],
            "Location": [res[4]],
            "Sample ID": [res[5]]
        })

    return jsonify(data)

@app.route('/wfreq')
def wfreq():
    results =session.query(Meta.SAMPLEID.Meta.WFREQ).all()
    
    return jsonify(results)

def samples():
    st=session.query(samples).statement
    df = pd.read_sql_query(st, session.bind)

if __name__ == "__main__":
    app.run(debug=True)




