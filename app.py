from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import os
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/'
app.config['SQLALCHEMY_TRACK_MODIFICATEION'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = 'audio_files'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    uid = db.Column(db.String(8), unique=True, nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=False)
    recordings = db.relationship('Recording', backref='user', lazy=True)

    def __init__(self, username: str, uid: str, token: int) -> None:
        self.username = username
        self.uid = uid
        self.token = token
        # self.recordings = recordings

    def __repr__(self) -> str:
        return f'Username: {self.username}'
    

class Recording(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(32), db.ForeignKey('user.uid'), nullable=False)
    recording_id = db.Column(db.String(32), unique=True, nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    def __init__(self, user_id: int, uid: str, recording_id: str, filename: str) -> None:
        self.user_id = user_id
        self.uid = uid
        self.recording_id = recording_id
        self.filename = filename

    def __repr__(self) -> str:
        return f'User id: {self.user_id} - Filename: {self.filename}'


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if not username:
        return jsonify({'Ошибка': 'Укажите username'}), 400
    
    uid = str(uuid.uuid4())[:8].replace('-', '').lower()
    token = str(uuid.uuid4().hex)

    try:
        new_user = User(uid=uid, username=username, token=token)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'Ошибка': 'Невозможно создать пользователя'}), 500
    return jsonify({'uid': uid, 'token': token})


# @app.route('/recordings', methods=['GET'])
# def recordings_page():
#     return render_template('recordings.html')

@app.route('/recordings', methods=['POST'])
def add_recording():
    
    # uid = request.form['uid']
    # token = request.form['token']
    # audio_file = request.form['audio_file']

    uid = request.json.get('uid')
    token = request.json.get('token')
    audio_file = request.files.get('audio_file')
    
    if not uid:
        return jsonify({'error': 'Укажите uid'})
    if not token:
        return jsonify({'error': 'Укажите token'})
    if not audio_file:
        return jsonify({'error': 'Укажите audio_file'})
    
    try:
        user = User.query.filter_by(uid=uid, token=token).one()
    except NoResultFound:
        return jsonify({'Ошибка': 'Неверные даные пользователя'}), 401
    
    recording_id = str(uuid.uuid4().hex)
    filename = recording_id + '.mp3'
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    audio_file.save(audio_path)

    new_recording = Recording(recording_id=recording_id, uid=uid, filename=filename)
    db.session.add(new_recording)
    db.session.commit()

    return jsonify({'url': f'http://localhost:5000/record?id={recording_id}&user={uid}'}), 201
    

@app.route('/record', methods=['GET'])
def download_recording():
    recording_id = request.args.get('recording_id')
    uid = request.args.get('uid')

    if not recording_id:
        return jsonify({'Ошибка': 'Укажите recording_id'}), 400
    if not uid:
        return jsonify({'Ошибка': 'Укажите uid'}), 400
    
    try:
        recording = Recording.query.filter_by(recording_id=recording_id, uid=uid)
    except NoResultFound:
        return jsonify({'Ошибка': 'Такая запись не найдена'}), 404
    
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], recording.filename)

    return app.send_static_file(audio_path)


if __name__ == '__main__':
    app.run(debug=True)
