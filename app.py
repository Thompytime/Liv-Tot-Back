from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace this with your Render database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://liv_tot_user:W1RyiS7p9yxojoIzw704mPAwEJOYCQDW@dpg-cuigakhu0jms738p11qg-a/liv_tot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liverpool_score = db.Column(db.Integer, nullable=False)
    tottenham_score = db.Column(db.Integer, nullable=False)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    liverpool_score = data.get('liverpoolScore')
    tottenham_score = data.get('tottenhamScore')

    new_prediction = Prediction(liverpool_score=liverpool_score, tottenham_score=tottenham_score)
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({'message': 'Prediction saved'}), 201

if __name__ == '__main__':
    app.run(debug=True)
