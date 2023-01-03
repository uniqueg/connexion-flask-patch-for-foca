from connexion.apps.flask_app import FlaskApp as FlaskAppOriginal
from connexion.apps.flask_app import (
    FlaskJSONEncoder,
    IntegerConverter,
    NumberConverter,
)
from flask import Flask
from flask.globals import _find_app
from foca.models.config import Config
from werkzeug.local import LocalProxy


class FocaApp(Flask):
    """Patch Flask to include `foca` attribute.
    
    Note that this will exist at `app.foca`, *not* at `app.config.foca`. A
    further patch of `flask.config.Config` would be needed for the latter.
    """
    def __init__(self, import_name, **server_args):
        super().__init__(import_name, **server_args)
        self.foca: Config = Config()


class FlaskApp(FlaskAppOriginal):
    """Patching `FlaskApp` to return `FocaApp` instead of `Flask`.

    Type of `FlaskApp` (original or patched) is `None`, according to the
    editor, so there is something not quite right in the way Connexion defines
    this app object, type-wise. Changing this would probably take a lot of
    patching, which may then need constant maintenance to keep up with
    Connexion development (v3 is on the horizon!). So it may be best to bite
    the bullet and live with the type checker complaining about seemingly
    assiging `None` to `FocaApp` (which we can explicitly ignore, knowing that
    it's not true).
    """
    def __init__(
        self,
        import_name,
        **kwargs,
    ):
        super().__init__(import_name, **kwargs)

    def create_app(self):
        app = FocaApp(self.import_name, **self.server_args)
        app.json_encoder = FlaskJSONEncoder
        app.url_map.converters['float'] = NumberConverter
        app.url_map.converters['int'] = IntegerConverter
        return app


current_app: FocaApp = LocalProxy(_find_app)  # type: ignore