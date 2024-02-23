from flask import Flask, jsonify, request
from flasgger import Swagger
import sqlite3


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hello', methods=["GET"])
def hello():
    """
    This is the hello endpoint.
    ---
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: An authorization token
    responses:
      200:
        description: A successful response
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    try:
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        data = "hello, this is our first flask website"
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({"Error": "Invalid request"}), 400



@app.route('/view', methods=["GET"])
def view():
    """
        This is the hello endpoint.
        ---
        parameters:
          - name: token
            in: header
            type: string
            required: true
            description: An authorization token
        responses:
          200:
            description: A successful response
          401:
            description: Token is missing
          400:
            description: Invalid request
        """
    try:
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Employees")
        data = cur.fetchall()
        DATAUSER = []
        for d in data:
            DATAUSER.append(dict(d))
        return jsonify({"data": DATAUSER})
    except Exception as e:
        return jsonify({"Error": "Invalid request"}), 400

@app.route("/savedetails", methods=["POST"])
def saveDetails():
    """
    This is the saveDetails endpoint.
    ---
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: An authorization token
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Name of the employee
            email:
              type: string
              description: Email of the employee
            mobilenumber:
              type: string
              description: Mobile number of the employee
    responses:
      200:
        description: A successful response
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    try:
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        name = request.json.get("name")
        email = request.json.get("email")
        mobilenumber = request.json.get("mobilenumber")

        if not name or not email or not mobilenumber:
            return jsonify({"error": "Invalid request data"}), 400

        with sqlite3.connect("user.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Employees (name, email, mobilenumber) VALUES (?, ?, ?)", (name, email, mobilenumber))
            con.commit()
            return jsonify({"data": "Employee successfully Added", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"}), 400

@app.route("/edit/<int:id>", methods=["PUT"])
def edit(id):
    """
    This endpoint updates employee details.
    ---
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: An authorization token
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the employee to be updated
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Name of the employee
            email:
              type: string
              description: Email of the employee
            mobilenumber:
              type: string
              description: Mobile number of the employee
    responses:
      200:
        description: Employee details successfully updated
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    try:
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        name = request.json.get("name")
        email = request.json.get("email")
        mobilenumber = request.json.get("mobilenumber")

        if not name or not email or not mobilenumber:
            return jsonify({"error": "Invalid request data"}), 400

        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""UPDATE Employees SET name = ?, email = ?, mobilenumber = ? WHERE id = ? """, (name, email, mobilenumber, id))
        con.commit()
        return jsonify({"data": "Employee successfully Updated", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"}), 400

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    """
    This is the hello endpoint.
    ---
    parameters:
      - name: token
        in: header
        type: string
        required: true
        description: An authorization token
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the employee to be deleted
    responses:
      200:
        description: A successful response
      401:
        description: Token is missing
      400:
        description: Invalid request
    """
    try:
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        con = sqlite3.connect("user.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("DELETE FROM Employees WHERE id = ?", (id,))
        con.commit()
        return jsonify({"data": "Employee successfully Deleted", 'status': 200})
    except Exception as e:
        return jsonify({"Error": "Invalid request"}), 400


if __name__ == '__main__':
    app.run(debug=True)
