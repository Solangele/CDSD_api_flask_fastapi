from flask import Flask, jsonify, request

def create_app() -> Flask:
    app = Flask(__name__)


    # from .blueprints.posts import bp as posts_bp
    from exo6 import bp as posts_bp

    app.register_blueprint(posts_bp)

    register_error_handlers(app)
    return app



def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint not found',
            'path': request.path,
            'method': request.method
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method not allowed',
            'path': request.path,
            'method': request.method,
            'allowed_methods': 'GET, POST, PUT, DELETE'
        }), 405