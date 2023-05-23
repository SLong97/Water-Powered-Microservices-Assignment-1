from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics
import psutil
from threading import Thread
import time

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    metrics = PrometheusMetrics(app)

    # static information as metric
    metrics.info('app_info', 'Application info', version='1.0.3')

    cpu_metric = metrics.gauge('cpu_usage', 'CPU usage')
    memory_metric = metrics.gauge('memory_usage', 'Memory usage')

    def update_metrics():
        while True:
            cpu_metric.set(psutil.cpu_percent())
            memory_metric.set(psutil.virtual_memory().percent)
            time.sleep(5)

    metrics_thread = Thread(target=update_metrics)
    metrics_thread.start()

    return app
