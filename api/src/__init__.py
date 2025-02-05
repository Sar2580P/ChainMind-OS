from flask import Flask
from src.routes import agent_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(agent_routes.bp, url_prefix="/api/v1/agents")
    return app
