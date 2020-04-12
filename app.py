from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Create class for table

class Falcon(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    ship = db.Column(db.String(127))
    owner = db.Column(db.String(256))

    def __init__(self,ship,owner):
        self.ship = ship
        self.owner = owner

@app.route('/')
def index():
    all_data = Falcon.query.all()
    return render_template('index.html',ships = all_data)

@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        ship = request.form['ship']
        owner = request.form['owner']

        my_data = Falcon(ship,owner)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Falcon.query.get(request.form.get('id'))
        my_data.ship = request.form['ship']
        my_data.owner = request.form['owner']
        
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/delete/<id>',methods = ['GET','POST'])
def delete(id):
    my_data = Falcon.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)