from flask import Flask, jsonify, request
from config import configure_db
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Initialize MySQL connection
mysql = configure_db(app)


# Sample route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    """
    This is the endpoint to get all users.
    ---
    responses:
      200:
        description: A list of all users
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)


# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
    """
    This is the endpoint to add a new user.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Name of the user
            email:
              type: string
              description: Email of the user
    responses:
      200:
        description: User added successfully
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    data = request.get_json()
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User added successfully'})


# Route to edit an existing user
@app.route('/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    """
    This is the endpoint to edit an existing user.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to edit
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: New name of the user
            email:
              type: string
              description: New email of the user
    responses:
      200:
        description: User edited successfully
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    data = request.get_json()
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User edited successfully'})


# Route to delete an existing user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    This is the endpoint to delete an existing user.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted successfully
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
