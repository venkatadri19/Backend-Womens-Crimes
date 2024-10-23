from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crimes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Database connection
# engine = create_engine('postgresql://username:password@localhost:5432/yourdatabase')
# Define the Crime model
class Crime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rape = db.Column(db.Integer, nullable=False)
    kidnapandassult = db.Column(db.Integer, nullable=False)
    dowry_deaths = db.Column(db.Integer, nullable=False)
    assult_against_women = db.Column(db.Integer, nullable=False)
    assult_against_modesty_of_women = db.Column(db.Integer, nullable=False)
    domestic_violence = db.Column(db.Integer, nullable=False)
    women_trafficking = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "State": self.state,
            "Year": self.year,
            "No of Rape cases": self.rape,
            "Kidnap And Assault": self.kidnapandassult,
            "Dowry Deaths": self.dowry_deaths,
            "Assault against women": self.assult_against_women,
            "Assault against modesty of women": self.assult_against_modesty_of_women,
            "Domestic violence": self.domestic_violence,
            "Women Trafficking": self.women_trafficking,
        }


@app.route("/api/crimes", methods=["GET"])
def get_all_crimes():
    crimes = Crime.query.all()
    return [crime.to_dict() for crime in crimes]


@app.route("/api/crimes/<state>", methods=["GET"])
def get_state_crimes(state):
    crimes = Crime.query.filter_by(state=state).all()
    return [crime.to_dict() for crime in crimes]


@app.route("/api/import/crimes/", methods=["POST"])
def import_crimes():
    url = "/var/www/html/flaskbackendapp/reference/CrimesOnWomenData.csv"  # Update with your downloaded file path
    data = pd.read_csv(url).to_dict(orient="records")
    print(f"{data}")
    for crime_item in data:
        new_crime = Crime(
            state=crime_item["State"],
            year=crime_item["Year"],
            rape=crime_item["Rape"],
            kidnapandassult=crime_item["K&A"],
            dowry_deaths=crime_item["DD"],
            assult_against_women=crime_item["AoW"],
            assult_against_modesty_of_women=crime_item["AoM"],
            domestic_violence=crime_item["DV"],
            women_trafficking=crime_item["WT"],
        )
        db.session.add(new_crime)
        db.session.commit()
    return data


if __name__ == "__main__":
    app.run(debug=True)