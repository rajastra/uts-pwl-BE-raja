from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized
from pyramid_jwt import _request_create_token as create_jwt_token

from .. import models

@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    dbsession = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('name', 'email', 'password')):
        raise HTTPBadRequest('Missing required fields')

    # Create a new User object with the input values
    user = models.User(name=data['name'], email=data['email'])
    user.set_password(data['password'])

    # Add the new user to the database
    dbsession.add(user)

    try:
        dbsession.commit()
    except IntegrityError:
        raise HTTPBadRequest('Email address already in use')

    # Generate a JWT token for the new user
    token = create_jwt_token(request, {'sub': user.id})

    # Return the JWT token as a cookie
    response = Response(json_body={'message': 'User created'})
    response.set_cookie('jwt_token', token, httponly=True)
    return response



@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    dbsession = request.dbsession
    data = request.json_body

    # Validate input data
    if not all(key in data for key in ('email', 'password')):
        raise HTTPBadRequest('Missing required fields')

    # Retrieve the user from the database
    user = dbsession.query(models.User).filter_by(email=data['email']).first()

    # Verify the password
    if user is None or not user.check_password(data['password']):
        raise HTTPUnauthorized('Invalid email or password')

    # Generate a JWT token for the user
    token = create_jwt_token(request, {'sub': user.id})

    # Return the JWT token as a cookie
    response = Response(json_body={'message': 'Login successful'})
    response.set_cookie('jwt_token', token, httponly=True)
    return response