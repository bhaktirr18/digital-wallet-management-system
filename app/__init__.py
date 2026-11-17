
from flask import Flask, render_template

from config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.wallet import wallet_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(wallet_bp)

    # Custom error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # Create database tables
    with app.app_context():
        from app.models import user, wallet, transaction
        db.create_all()

    return app
