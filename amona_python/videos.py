from flask import Flask, Blueprint, request
from db.database import Videos, connection, select, delete, insert, update, metadata, and_
import inspect
video = Blueprint('videos', __name__, template_folder='templates')


def list_to_json(list):
    """[summary]
    Appends the Column headers as Keys
    and returns a JSON with the values

    Args:
        list ([type]): [description]

    Returns:
        JSON
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    op = {}
    for (a, b) in zip((Videos.c.keys()), list):
        op[a] = str(b).replace('property.', '')
    return op


@video.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
    obj = {}
    for key in Videos.c.keys():
        obj[key] = '1'
    return obj


@video.route('/addOne', methods=["PUT"])
def addOne():
    """[summary]
    TESTED - FOUND OK
    Add the Users's Data to an entry

    Returns:
        users data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
  
    # read data from the API call
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    for req in req_data:
        if (req in Videos.c.keys()):
            json_data[req] = req_data[req]
    query = (
        insert(Videos).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Property")
        return {'error': 'Unable to Add the given property'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}


 

@video.route('/viewAll', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the Userss Data

    Returns:
        users data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([Videos])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@video.route('/<id>', methods=["GET", "POST"])
def viewOne(id):
    """[summary]
    TESTED - FOUND OK
    View the Users's Data with a specific id

    Returns:
        users data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([Videos]).where(Videos.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given property'}
    print(ResultSet)
    return list_to_json(ResultSet)


@video.route('/<id>', methods=["DELETE"])
def deleteOne(id):
    """[summary]
    TESTED - FOUND OK
    Delete the Users's Data with a specific id

    Returns:
        Success Message
        OR 
        Empty ID Message
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = Videos.delete().where(Videos.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given videos')
        return {'error': 'Unable to find the given videos'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@video.route('/<id>', methods=["PUT"])
def updateOne(id):
    """[summary]
    TESTED - FOUND OK
    Update the Users's Data with a specific id

    Returns:
        users data in a String (Do in JSON)
        OR 
        Empty string Message
        [type]: [description]
    """
    # read data from the API call
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    query = select([Videos]).where(Videos.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given property')
        return {'error': 'Unable to Find the given property'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Videos.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Videos).
        where(Videos.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("unable to update property")
        return {'error': 'Unable to Update the given property'}
    print("Update Succesful")
    return {'status': "Update Succesful"}

