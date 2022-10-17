from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route('/delete/<int:car_id>', methods=['POST'])
def delete(car_id):
    """ recieved post requests for entry delete """
    print(car_id)

    try:
        db_helper.remove_car_by_id(car_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route('/create', methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    response = db_helper.insert_new_car(
        color=data['color'],
        model=data['model'],
        owner=data['owner']
    )

    if response == -1:
        result = {'success': False, 'response': 'Owner exceeded car limit'}
    else:
        result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/create_owner', methods=['POST'])
def create_owner():
    """recieves post request to add new owner"""
    data = request.get_json()
    response = db_helper.insert_new_owner(
        data['owner_name']
    )

    if response == -1:
        result = {'success': False, 'response': 'Owner already in database'}
    else:
        result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/')
def homepage():
    """ returns rendered homepage """
    cars, owners = db_helper.fetch_cars()
    return render_template("index.html", cars=cars, owners=owners)