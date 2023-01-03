import connexion

capp = connexion.FlaskApp(__name__, specification_dir='openapi/')


capp.app
print(type(capp))
print(type(capp.app))


capp.add_api('my_api.yaml')
capp.run(port=8080)
