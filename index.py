# To start the server, use the following command:
# flask run

from flask import Flask, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv
import pandas as pd
import os

from database_scripts.database_model import db, ExperimentData
from database_scripts.database_functions import new_data, update_data
from algorithms import algorithm1, algorithm2, algorithm3

load_dotenv()

app = Flask(__name__)

if not os.getenv("SQLALCHEMY_DATABASE_URI"):
    raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

# Set database configurations in the Flask app and use them to initialize the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
db.init_app(app)

CORS(app, origins=["http://localhost:3000", "https://thesis.streamwebsite.nl"], methods=["GET", "POST"])

@app.route("/")
def hello_world():
    return jsonify("Hello world!")

# Route is called when preferences are confirmed and does four things:
#   1. Store demographic data in the database and retrieve participant number
#   2. Use participant number to determine condition_id, task order and algorithm order
#   3. Generate carousels + items with each algorithm
#   4. Return results from step 3 together with the user's participant number and results from step 2
@app.route("/api/generate-data", methods=['POST'])
def generate_data():
    print('\033[32m\n--- START LOGS ---\033[0m')
    print('Route === /generate-data')
    # Extract data from request object
    data = request.json
    data_to_store = data.get('data')
    liked_items = data.get('preferenceIDs')
    
    # Step 1: store demographic data in the database and retrieve participant number
    print('\n--- STEP 1 ---')
    participant_number = new_data(db, ExperimentData, data_to_store)
    print('--- STEP 1 ---\n')
    
    # Step 2: Use participant number to determine condition_id, task order and algorithm order
    print('\n--- STEP 2 ---')
    # Calculate condition_id
    condition_id = participant_number - 1
    while condition_id > 35:
        condition_id -= 36
    print(f'\tGenerated condition_id: {condition_id}')
    # Determine algorithm order
    orders = {
        0: [1, 2, 3],
        1: [1, 3, 2],
        2: [2, 3, 1],
        3: [2, 1, 3],
        4: [3, 1, 2],
        5: [3, 2, 1]
    }
    algorithm_number = condition_id // 6
    algorithm_order = orders[algorithm_number]
    print(f'\tGenerated algorithm_order: {algorithm_order}')
    # Determine task order
    task_number = condition_id % 6
    task_order = orders[task_number]
    print(f'\tGenerated task_order: {task_order}')
    print(f'\tTask_order is of type: {type(task_order)}')
    print('--- STEP 2 ---\n')
    
    # Step 3: Generate carousels + items with each algorithm
    print('\n--- STEP 3 ---')
    encoded_data_path = "datasets/encoded_data.csv"
    raw_data_path = "datasets/raw_data.csv"
    df_raw = pd.read_csv(raw_data_path, header=0)
    algorithm1_object = algorithm1(df_raw)
    print(f'\tGenerated data for algorithm 1')
    algorithm2_object = algorithm2(df_raw)
    print(f'\tGenerated data for algorithm 2')
    algorithm3_object = algorithm3(liked_items, df_raw, encoded_data_path)
    print(f'\tGenerated data for algorithm 3')
    print('--- STEP 3 ---\n')

    data =  {
        'algorithm1': algorithm1_object,
        'algorithm2': algorithm2_object,
        'algorithm3': algorithm3_object,
        'algorithm_order': algorithm_order,
        'task_order': task_order,
        'condition_id': condition_id,
        'participant_number': participant_number,
        'success': True
    }
    print('\033[32m--- FINISH LOGS ---\n\033[0m')
    return jsonify(data)


# Route is called everytime the questionnaire is filled in and does two things:
#   1. Store data in request object into the database
#   2. Return success = true if storage was successful
@app.route("/api/update-database", methods=['POST'])
def update_database():
    print('\033[32m\n--- START LOGS ---\033[0m')
    print('Route === /generate-data')
    # Extract data from request object
    data = request.json
    data_to_store = data.get('data')
    participant_number = data.get('participant_number')

    update_data(db, ExperimentData, participant_number, data_to_store)

    print('\033[32m--- FINISH LOGS ---\n\033[0m')
    return jsonify({
        'success': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)