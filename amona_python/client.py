from flask import Flask, Blueprint, request
from db.database import Client, connection, select, delete, insert, update, metadata, and_
import inspect
client = Blueprint('client', __name__, template_folder='templates')


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
    for (a, b) in zip((Client.c.keys()), list):
        op[a] = str(b).replace('client.', '')
    return op


@client.route('/test/', methods=["GET", "POST"])
def viewTableAll():
    print(inspect.stack()[1][3])
    obj = {}
    for key in Client.c.keys():
        obj[key] = '1'
    return obj


"""@client.route('/loginfx', methods=["GET", "POST"])
def loginfx():
    print(inspect.stack()[1][3])
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    for req in req_data:
        if (req in Client.c.keys()):
            json_data[req] = req_data[req]

#Left to be edited

    if('username' in json_data and 'pwd' in json_data):
        # check for User_type

        query = select([User]).where(and_(Client.columns.username ==
                                          json_data['username'], Client.columns.pwd == json_data['pwd']))
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        if(not ResultSet):
            print('Unable to find the user for Login')
            return {'error': 'Unable to find the user for Login'}

        print(list_to_json(ResultSet))
        return {'success': ' User logs in', 'user_id': list_to_json(ResultSet)}

    print('Cannot login')
    return {'error': 'Cannot Login'}"""
    
    
 

@client.route('/', methods=["GET", "POST"])
def viewAll():
    """[summary]
    TESTED - FOUND OK
    View all the Userss Data

    Returns:
        users data in a String (Do in JSON)
        [type]: [description]
    """
    print(inspect.stack()[1][3])
    query = select([Client])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    res = []
    for rs in ResultSet:
        print(rs)
        res.append(list_to_json(rs))
    return dict(enumerate(res))


@client.route('/<id>', methods=["GET", "POST"])
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
    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        return {'error': 'Unable to find the given client1'}
    print(ResultSet)
    return list_to_json(ResultSet)


@client.route('/<id>', methods=["DELETE"])
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
    query = Client.delete().where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print('Unable to find the given Client2')
        return {'error': 'Unable to find the given Client3'}
    print("Delete Succesful for ID: " + str(id))
    return {'status': "Delete Succesful for ID: " + str(id)}


@client.route('/<id>', methods=["PUT"])
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
    query = select([Client]).where(Client.columns.id == id)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchone()
    if(not ResultSet):
        print('Unable to find the given Client4')
        return {'error': 'Unable to Find the given Client5'}

    # Update the URL
    json_data = {}

    for req in req_data:
        if (req in Client.c.keys()):
            json_data[req] = req_data[req]

    query = (
        update(Client).
        where(Client.columns.id == id).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("unable to update Client6")
        return {'error': 'Unable to Update the given Client7'}
    print("Update Succesful")
    return {'status': "Update Succesful"}


@client.route('/addOne', methods=["PUT"])
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
    #req_data = request.form.to_dict()
    req_data = request.get_json()
    print(req_data)
    json_data = {}

    for req in req_data:
        if (req in Client.c.keys()):
            json_data[req] = req_data[req]
    query = (
        insert(Client).
        values(json_data)
    )
    ResultProxy = connection.execute(query)
    if(not ResultProxy):
        print("Unable to Add Client8")
        return {'error': 'Unable to Add the given client9'}
    print("Add Succesful")
    return {'status': "Adding Succesful"}
    
    
    """
    cli_name=request.form['clientname']
    cli_url= request.form['logo_url']
    cli_priority=request.form['priority']
    cursor.execute("INSERT INTO client VALUES (%s,%s,%s)", (cli_name,cli_url,cli_priority)) 
    con.commit() 
    return "successfully Added"
    """
   
