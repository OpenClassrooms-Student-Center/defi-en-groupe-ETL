"""
Flask module to run the web service

It is built using the "factory application" pattern.
"""
from .load import load
from .webapp import create_app


def run_web_service():
    """ This function runs the web service in debug mode """
    app = create_app()
    app.run(debug=True)

__all__ = ["load", "run_web_service"]