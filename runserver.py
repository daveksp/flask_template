from flask_template import app

# EXECUTING THROUGH python call
# python runserver.py DevelopmentConfig

# it's faster for you just run 
# resources/scripts/wsgi_start.sh enviroment[Testing, Development, Production]


if __name__ == '__main__':
    app.run('0.0.0.0')
