from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(28), nullable=False, unique=True)
	public_id = db.Column(db.String, nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	todos=db.relationship('Todo', backref='owner', lazy='dynamic')

	def __repr__(self):
		return f'User <{self.email}>'

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	name = db.Column(db.String(20), nullable=False)
	is_completed = db.Column(db.Boolean, default=False)
	public_id = db.Column(db.String, nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return f'Todo: <{self.name}>'

@app.route('/')
def home():
	return {
		'message': 'Welcome to building RESTful APIs with Flask and SQLAlchemy'
	}

@app.route('/users/')
def get_users():
	return jsonify([
		{
			'id': user.public_id, 'name': user.name, 'email': user.email,
			'is admin': user.is_admin
			} for user in User.query.all()
	])

# @app.route('/home/')
# def home():
#   return render_template('home.html')

# @app.route('/about')
# def about():
#    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)