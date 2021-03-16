from flask import Flask, Blueprint, request
from db.database import Images, connection, select, delete, insert, update, metadata, and_
import inspect
image = Blueprint('images', __name__, template_folder='templates')


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
    for (a, b) in zip((Images.c.keys()), list):
        op[a] = str(b).replace('image.', '')
    return op


@image.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
    obj = {}
    for key in Images.c.keys():
        obj[key] = '1'
    return obj


@image.route('/addOne', methods=["PUT"])
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
        if (req in Images.c.keys()):
            json_data[req] = req_data[req]
    query = (
        insert(Images).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Image")
        return {'error': 'Unable to Add the given image'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}


 

@image.route('/viewAll', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the Userss Data

    Returns:
        users data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([Images])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@image.route('/<id>', methods=["GET", "POST"])
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
    query = select([Images]).where(Images.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given property1'}
    print(ResultSet)
    return list_to_json(ResultSet)


@image.route('/<id>', methods=["DELETE"])
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
    query = Images.delete().where(Images.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given image')
        return {'error': 'Unable to find the given property2'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@image.route('/<id>', methods=["PUT"])
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
    query = select([Images]).where(Images.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given image3')
        return {'error': 'Unable to Find the given image4'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Images.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Images).
        where(Property.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("unable to update image5")
        return {'error': 'Unable to Update the given image6'}
    print("Update Succesful")
    return {'status': "Update Succesful"}


