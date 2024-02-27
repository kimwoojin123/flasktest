from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3308/kimdb2'
db = SQLAlchemy(app)

class Save(db.Model):
    test = db.Column(db.String(255), primary_key=True)  # test 컬럼을 기본키로 사용

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # 폼 데이터 받기
        data = request.form['data']
        
        # 받은 데이터 출력
        print("Received data:", data)
        
        # 원하는 작업 수행
        new_data = Save(test=data)
        db.session.add(new_data)
        db.session.commit()

        # 클라이언트에게 응답
        return 'Data received successfully'

@app.route('/get_data', methods=['GET'])
def get_data():
    # 데이터베이스에서 모든 데이터 가져오기
    data = Save.query.all()
    
    # 데이터를 JSON 형식으로 변환하여 반환
    data_list = [{'test': entry.test} for entry in data]
    return jsonify(data_list)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)