from flask import Flask, Blueprint, request
from db.database import Property, connection, select, delete, insert, update, metadata, and_
import inspect
property = Blueprint('property', __name__, template_folder='templates')


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
    for (a, b) in zip((Property.c.keys()), list):
        op[a] = str(b).replace('property.', '')
    return op


@property.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
    obj = {}
    for key in Property.c.keys():
        obj[key] = '1'
    return obj


@property.route('/addone', methods=["PUT"])
def addone():
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
        if (req in Property.c.keys()):
            json_data[req] = req_data[req]
    query = (
        insert(Property).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Property")
        return {'error': 'Unable to Add the given property'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}


 

@property.route('/viewall', methods=["GET", "POST"])
def viewall():
    """[summary]
    TESTED - FOUND OK
    View all the Userss Data

    Returns:
        users data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([Property])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@property.route('/viewone', methods=["GET", "POST"])
def viewone():
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
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    #print(json_data)

    for req in req_data:
            if (req in Property.c.keys()):
                json_data[req] = req_data[req]

    query = select([Property]).where(Property.columns.name == json_data['name'])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    
    if(not ResultSet):
        return {'error': 'Unable to find the given property5'}
    print(ResultSet)
    return list_to_json(ResultSet)


@property.route('/deleteone', methods=["DELETE"])
def deleteone(id):
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
    query = Property.delete().where(Property.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given property4')
        return {'error': 'Unable to find the given property3'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@property.route('/updateone', methods=["PUT"])
def updateone(id):
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
    query = select([Property]).where(Property.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given propertys2')
        return {'error': 'Unable to Find the given propertys1'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Property.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Property).
        where(Property.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("unable to update property")
        return {'error': 'Unable to Update the given property'}
    print("Update Succesful")
    return {'status': "Update Succesful"}

# extra lines added

@property.route('/search', methods=["GET","POST"])
def search():
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
    # query = select([Property]).where(Property.columns.id == id)
    # ResultProxy = connection.execute(query)
    # ResultSet = ResultProxy.fetchone()
    # if(not ResultSet):
    #     print('Unable to find the given property')
    #     return {'error': 'Unable to Find the given property'}
    #return ResultSet    
    
    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Property.c.keys()):
            json_data[req] = req_data[req]

    query = (
        select(Property).
        where(Property.columns.details == req_data.details).
        values(json_data)
    )

    ResultProxy = connection.execute(query)
    print(ResultProxy)
    return (ResultProxy)
   
    if(not ResultProxy):
        print("unable to find property7")
        return {'error': 'Unable to find the given property6'}
    print("Update Succesful")
    return {'status': "Search Succesful"}