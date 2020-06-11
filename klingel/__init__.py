import os

from flask import Flask
from python_json_config import ConfigBuilder



def loadconfig():
    global path

    # create config parser
    builder = ConfigBuilder()

    # parse config
    config = builder.parse_config('config.json')    

    path=config.path




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    loadconfig()

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'klingel.sqlite'),
        host='0.0.0.0',
        PIC_PATH=path,
    )

    if test_config != None:
        print("Loading Testconfig")
        app.config.from_mapping(test_config)
        


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'



    from . import lists
    app.register_blueprint(lists.bp)

    from . import live
    app.register_blueprint(live.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    return app