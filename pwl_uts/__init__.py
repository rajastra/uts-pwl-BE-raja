from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
        config.include('pyramid_jwt')
        config.add_request_method(lambda r: r.jwt_claims.get('sub'), 'userid', reify=True)
        config.scan()
    return config.make_wsgi_app()
