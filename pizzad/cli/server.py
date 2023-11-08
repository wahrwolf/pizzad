import click

from pizzad.web.server import WebServer


def build_server_commands(server: WebServer):
    @click.group("server")
    def server_commands():
        pass

    @server_commands.command()
    @click.option('--port', type=int, default=5000,
                  help='Port number (default: 5000)')
    @click.option('--host', type=str, default='localhost',
                  help='Host name (default: localhost)')
    @click.option('--enable-debug', is_flag=True,
                  help='Enable debug mode')
    @click.option('--url-prefix', type=str, default='',
                  help='Proxy url prefix (default: "")')
    def run(host, port, enable_debug, url_prefix):
        try:
            server.setup(url_prefix)
            server.run(host=host, port=port, enable_debug=enable_debug)
        except Exception as error:
            click.echo(f"Could not start server due: {error}")

    return server_commands
