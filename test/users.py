from flask import jsonify
from remote_doctor.models import User  # Assuming your User model is imported from the 'models' module

@app.route('/test/users', methods=['GET'])
def test_users():
    session = Session()  # Assuming you have created the Session object
    users = session.query(User).all()

    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        user_list.append(user_data)

    return jsonify(user_list)

