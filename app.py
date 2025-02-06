import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Replace this with your Render database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://liv_tot_user:W1RyiS7p9yxojoIzw704mPAwEJOYCQDW@dpg-cuigakhu0jms738p11qg-a.frankfurt-postgres.render.com/liv_tot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize the migration extension
migrate = Migrate(app, db)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liverpool_score = db.Column(db.Integer, nullable=False)
    tottenham_score = db.Column(db.Integer, nullable=False)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No JSON data provided"}), 400
        
        # Log the data to check its format
        print("Received data:", data)

        liverpool_score = data.get('liverpoolScore')
        tottenham_score = data.get('tottenhamScore')

        if liverpool_score is None or tottenham_score is None:
            return jsonify({"message": "Missing score values"}), 400

        # Save prediction in the database
        new_prediction = Prediction(liverpool_score=liverpool_score, tottenham_score=tottenham_score)
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({'message': 'Prediction saved'}), 201

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


