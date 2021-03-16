from flask import Flask, Blueprint, request
from db.database import User, connection, select, delete, insert, update, metadata, and_
import inspect
user = Blueprint('user', __name__, template_folder='templates')


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
    for (a, b) in zip((User.c.keys()), list):
        op[a] = str(b).replace('user.', '')
    return op


@user.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
    obj = {}
    for key in User.c.keys():
        obj[key] = '1'
    return obj


@user.route('/login', methods=["GET", "POST"])
def login():
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    
    for req in req_data:
        if (req in User.c.keys()):
            json_data[req] = req_data[req]
    print(json_data) 


    if('email' in json_data and 'password' in json_data):
        # check for User_type

        query = select([User]).where(and_(User.columns.email ==
                                          json_data['email'], User.columns.password == json_data['password']))
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        if(not ResultSet):
            print('Unable to find the user for Login')
            return {'error': 'Unable to find the user for Login'}
        else:
            print(list_to_json(ResultSet))
            return {'success': ' User logs in', 'user_id': list_to_json(ResultSet)}

    print('Cannot login')
    return {'error': 'Cannot Login'}
 
@user.route('/addOne', methods=["PUT"])
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
        if (req in User.c.keys()):
            json_data[req] = req_data[req]
    query = (
        insert(User).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Users")
        return {'error': 'Unable to Add the given users'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}   
    
 

@user.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the Userss Data

    Returns:
        users data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([User])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@user.route('/<id>', methods=["GET", "POST"])
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
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given users'}
    print(ResultSet)
    return list_to_json(ResultSet)


@user.route('/<id>', methods=["DELETE"])
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
    query = User.delete().where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given user')
        return {'error': 'Unable to find the given user'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@user.route('/<id>', methods=["PUT"])
def updateOne(id):
    """
    [summary]
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
    query = select([User]).where(User.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given users')
    return {'error': 'Unable to Find the given users'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in User.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(User).
        where(User.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("unable to update users")
        return {'error': 'Unable to Update the given user'}
    print("Update Succesful")
    return {'status': "Update Succesful"}
