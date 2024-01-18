from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.title for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    task = Task(title=request.json['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    task.title = request.json['title']
    db.session.commit()
    return jsonify({'id': task.id})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
