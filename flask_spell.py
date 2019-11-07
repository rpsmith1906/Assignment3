from spell import app
from spell.userman import Users

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5000', debug=app.config['debug'])
     #app.run(host=app.config['host'], port=app.config['port'], debug=app.config['debug'])
     
