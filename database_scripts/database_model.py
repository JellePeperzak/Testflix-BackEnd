from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# db.BigInteger
# db.SmallInteger
# db.Boolean

class ExperimentData(db.Model):
    __tablename__ = 'experimentdata'

    # Metadata Columns
    id = db.Column(db.Integer, primary_key=True)
    time_start = db.Column(db.BigInteger)
    time_finish = db.Column(db.BigInteger)
    task1_start = db.Column(db.BigInteger)
    task1_finish = db.Column(db.BigInteger)
    task2_start = db.Column(db.BigInteger)
    task2_finish = db.Column(db.BigInteger)
    task3_start = db.Column(db.BigInteger)
    task3_finish = db.Column(db.BigInteger)
    condition_id = db.Column(db.SmallInteger)
    first_task = db.Column(db.SmallInteger)
    second_task = db.Column(db.SmallInteger)
    third_task = db.Column(db.SmallInteger)
    first_algorithm = db.Column(db.SmallInteger)
    second_algorithm = db.Column(db.SmallInteger)
    third_algorithm = db.Column(db.SmallInteger)

    # Demographic Questionnaire Columns
    age = db.Column(db.SmallInteger)
    gender = db.Column(db.String(20))
    nationality = db.Column(db.String(80))
    experience = db.Column(db.SmallInteger)
    consumption = db.Column(db.Integer)

    # Task Data Columns
    task1_movie = db.Column(db.Boolean)
    task1_series = db.Column(db.Boolean)
    task1_search = db.Column(db.Boolean)
    task2_movie = db.Column(db.Boolean)
    task2_series = db.Column(db.Boolean)
    task2_search = db.Column(db.Boolean)
    task3_movie = db.Column(db.Boolean)
    task3_series = db.Column(db.Boolean)
    task3_search = db.Column(db.Boolean)

    # Algorithm Data Columns
    algorithm1_movie = db.Column(db.Boolean)
    algorithm1_series = db.Column(db.Boolean)
    algorithm1_search = db.Column(db.Boolean)
    algorithm2_movie = db.Column(db.Boolean)
    algorithm2_series = db.Column(db.Boolean)
    algorithm2_search = db.Column(db.Boolean)
    algorithm3_movie = db.Column(db.Boolean)
    algorithm3_series = db.Column(db.Boolean)
    algorithm3_search = db.Column(db.Boolean)

    # Gratification Questionnaire Columns
    cn_1_1 = db.Column(db.SmallInteger)
    cn_1_2 = db.Column(db.SmallInteger)
    cn_1_3 = db.Column(db.SmallInteger)
    cn_2_1 = db.Column(db.SmallInteger)
    cn_2_2 = db.Column(db.SmallInteger)
    cn_2_3 = db.Column(db.SmallInteger)
    en_1_1 = db.Column(db.SmallInteger)
    en_1_2 = db.Column(db.SmallInteger)
    en_1_3 = db.Column(db.SmallInteger)
    se_1_1 = db.Column(db.SmallInteger)
    se_1_2 = db.Column(db.SmallInteger)
    se_1_3 = db.Column(db.SmallInteger)

    # Evaluation Questionnaire Columns
    eval_1_1 = db.Column(db.SmallInteger)
    eval_1_2 = db.Column(db.SmallInteger)
    eval_1_3 = db.Column(db.SmallInteger)
    eval_2_1 = db.Column(db.SmallInteger)
    eval_2_2 = db.Column(db.SmallInteger)
    eval_2_3 = db.Column(db.SmallInteger)
    eval_3_1 = db.Column(db.SmallInteger)
    eval_3_2 = db.Column(db.SmallInteger)
    eval_3_3 = db.Column(db.SmallInteger)

    # Comments Column
    feedback = db.Column(db.String(800))