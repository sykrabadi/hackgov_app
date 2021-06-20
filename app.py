from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyek.db'
db = SQLAlchemy(app)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)
css.build()

class sektorTable(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    alias_sektor = db.Column(db.String(length=1024), nullable=False)
    nama_sektor = db.Column(db.String(length=1024), nullable=False)
    pembangunan = db.relationship('pembangunanSektorTable', backref='relasi_antarsektor')

    def __repr__(self):
        return f'{self.id}'

class pembangunanSektorTable(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    kodeTender = db.Column(db.Integer())
    nilaiHps = db.Column(db.Integer())
    namaPembangunan = db.Column(db.String(length=2048), nullable=False)
    statusPembangunan = db.Column(db.String(length=1024), nullable=False)
    kualifikasiUsaha = db.Column(db.String(length=1024), nullable=False)
    syaratKualifikasi = db.Column(db.String(length=4096), nullable=False)
    relasi_sektor = db.Column(db.Integer(), db.ForeignKey('sektor_table.id'))

    def __repr__(self):
         return f'{self.kodeTender}'

@app.route("/home")
def home():
    sektor = sektorTable.query.all()
    return render_template("index.html", sektor = sektor)

@app.route("/sektor/<sektor>")
def sektor(sektor):
    sektor = sektorTable.query.filter_by(id = sektor).first()
    return render_template("sektor.html", sektor = sektor)

if __name__ == "__main__":
    app.run(debug=True)