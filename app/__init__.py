import sys, os.path, importlib
from flask import Flask
from app import hooks

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
app.config.from_pyfile('natsuko_default.cfg')
app.config.from_pyfile('../natsuko.cfg', silent=True)

##  regex router boilerplate
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter
##  regex support done

for module_name in app.config['MODULES']:
    try:
        module = importlib.import_module(module_name)
        hooks.run("module_imported", module_name)

        try: # If the module has controllers, we want them
            mod_controllers = importlib.import_module(module_name + ".controllers")
            try:
                app.register_blueprint(mod_controllers.blueprint)
            except AttributeError:
                print("Module " + module_name + " has a 'controllers' submodule, but no blueprint!")

        except ImportError:
            pass

    except ImportError:
        print("Can't import module " + module_name + "!")


hooks.run("startup")
