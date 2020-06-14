#!/usr/bin/python3
import os

from flask import Flask
from python_json_config import ConfigBuilder


#TODO: Handling wenn Datei nicht gefunden
#TODO: Pfad der Config Datei ueber ENV einlesen
def loadconfig(app,test_config):

    try:
        settings_file = os.environ['KLINGEL_SETTING_FILE']
        print("Reading Settings from: "+settings_file)
    except:
        print("Cannot read environment variable: KLINGEL_SETTING_FILE")
        print("using default: config.json")
        settings_file = 'config.json'
    

    # create config parser
    builder = ConfigBuilder()

    # parse config
    try:
        config = builder.parse_config(settings_file)    
    except: 
        print("Cannot read setting file: " + settings_file)
        return

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'klingel.sqlite'),
        host='0.0.0.0',
        PIC_PATH=config.path,
    )

    if test_config != None:
        print("Loading Testconfig")
        app.config.from_mapping(test_config)
        




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    loadconfig(app,test_config)

    if not os.path.isdir(app.config['PIC_PATH']):
        print('ERROR: PIC_PATH is not a valid path!')
        

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import lists
    app.register_blueprint(lists.bp)

    from . import live
    app.register_blueprint(live.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    return app