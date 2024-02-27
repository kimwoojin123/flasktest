from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MariaDB connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3308/kimdb2'
db = SQLAlchemy(app)

# Define Netflix table model
class Netflix(db.Model):
    __tablename__ = 'netflix'  # Adjust table name if needed

    show_id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    director = db.Column(db.String(255))
    cast = db.Column(db.String(255))
    country = db.Column(db.String(255))
    date_added = db.Column(db.String(255))
    release_year = db.Column(db.Integer)
    duration = db.Column(db.String(255))
    listed_in = db.Column(db.String(255))
    description = db.Column(db.String(255))

# Route to render index.html template
@app.route('/')
def index():
    # Get column names from the Netflix table
    columns = [column.key for column in Netflix.__table__.columns if column.key != 'show_id']
    return render_template('index.html', columns=columns)

# Route to handle search request
@app.route('/search', methods=['POST'])
def search():
    field = request.json['field']
    search_value = request.json['searchValue']

    # Query based on the selected field and search value
    results = Netflix.query.filter(getattr(Netflix, field).like(f'%{search_value}%')).all()

    # Convert results to JSON format
    result_list = [{'title': item.title, 'director': item.director, 'cast' : item.cast, 'country':item.country, 'duration':item.duration, 'release_year': item.release_year, 'description':item.description} for item in results]
    return jsonify(result_list)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)