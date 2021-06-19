from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyek.db'
db = SQLAlchemy(app)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)
css.build()

class Sektor_Table(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    alias_sektor = db.Column(db.String(length=1024), nullable=False)
    nama_sektor = db.Column(db.String(length=1024), nullable=False)

    def __repr__(self):
        return f'{self.alias_sektor}'

@app.route("/home")
def home():
    sektor = Sektor_Table.query.all()
    return render_template("index.html", sektor = sektor)

@app.route("/sektor/<sektor>")
def sektor(sektor):
    sektor = Sektor_Table.query.filter_by(alias_sektor = sektor).first()
    return render_template("sektor.html", sektor = sektor)

if __name__ == "__main__":
    app.run(debug=True)