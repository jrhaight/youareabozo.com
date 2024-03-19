from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nominees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    latest_nominee = Nominee.query.order_by(Nominee.timestamp.desc()).first()
    return render_template('index.html', latest_nominee=latest_nominee)

@app.route('/nominate', methods=['GET', 'POST'])
def nominate():
    if request.method == 'POST':
        nominee_name = request.form['name']
        nominee = Nominee(name=nominee_name)
        db.session.add(nominee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('nominate.html')

@app.route('/past_awardees')
def past_awardees():
    nominees = Nominee.query.order_by(Nominee.timestamp.asc()).all()
    return render_template('past_awardees.html', nominees=nominees)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
