from abc import ABC, abstractmethod
from flask import Flask, Blueprint


class Router(ABC):
    @abstractmethod
    def list_routes(self):
        pass


class Engine(ABC):
    @abstractmethod
    def run(self, host: str = 'localhost', port: int = 5000, enable_debug: bool = False):
        pass

    @abstractmethod
    def register_router(self, router: Router, url_prefix: str = ''):
        pass


class WebServer(ABC):
    host: str
    port: int
    debug_enabled: bool
    engine: Engine
    router: Router

    def set_router(self, router: Router):
        self.router = router

    def set_engine(self, engine: Engine):
        self.engine = engine

    def setup(self, url_prefix: str = ''):
        if not self.is_compatible(self.engine, self.router):
            raise ValueError("Engine and router are not compatible for this web server.")
        self.engine.register_router(self.router, url_prefix)

    @abstractmethod
    def is_compatible(self, engine: Engine, router: Router):
        pass

    def run(self, host: str = 'localhost', port: int = 5000, enable_debug: bool = False):
        self.engine.run(host=host, port=port, enable_debug=enable_debug)


class FlaskBlueprintRouter(Router):
    def __init__(self, blueprint: Blueprint = None):
        self.blueprint = blueprint if blueprint else Blueprint('router', __name__)

    def to_blueprint(self):
        return self.blueprint

    def list_routes(self):
        pass


class FlaskEngine(Engine):
    def __init__(self):
        self.app = Flask(__name__)

    def register_router(self, router: FlaskBlueprintRouter, url_prefix: str = ''):
        self.app.register_blueprint(router.to_blueprint(), url_prefix=url_prefix)

    def run(self, host: str = 'localhost', port: int = 5000, enable_debug: bool = False):
        self.app.run(host=host, port=port, debug=enable_debug)


class FlaskWebServer(WebServer):
    def __init__(self, blueprint: Blueprint):
        self.engine = FlaskEngine()
        self.router = FlaskBlueprintRouter(blueprint)

    def is_compatible(self, engine, router):
        return isinstance(engine, FlaskEngine) and isinstance(router, FlaskBlueprintRouter)
