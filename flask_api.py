import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 

# Initialize Flask app
app = Flask(__name__)

# SQLite DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the DB
db = SQLAlchemy(app)

# Define a model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)    
    des = db.Column(db.String(320), nullable=False)
    date = db.Column(db.String(100), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User('{self.title}', '{self.des}', '{self.date}')"

# Routes (optional)
@app.route("/",methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = User(title=request.form['title'], des=request.form['des'])
        db.session.add(todo)      # Add the object to the session
        db.session.commit()       # Commit the session to the DB

    # Query all users
    users = User.query.all()
    # Print all users
    for user in users:
        print(user)
    return render_template('index.html',users=users)


@app.route("/delete/<int:id>")
def delete(id):
    # Query all users
    users = User.query.filter_by(id=id).first()
    print(users.title)
    db.session.delete(users)
    db.session.commit()      
    return redirect('/')

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        users = User.query.filter_by(id=id).first()
        users.title = title
        users.des = des
        db.session.add(users)      
        db.session.commit()       # Commit the session to the DB
        return redirect('/')

    users = User.query.filter_by(id=id).first()
    print(users.title)
    return render_template('update.html',users=users)

# Run the app and create DB
if __name__ == "__main__":
    with app.app_context():     # Required for db.create_all()
        db.create_all()         # 🔥 This will create site.db with User table
    app.run(debug=True)
