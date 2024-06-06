import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, session, render_template
from models import init_db
from services.user_service import user_bp
from services.space_service import space_bp
from services.visitor_service import visitor_bp
from services.taxa_service import fee_bp
from services.agendamento_service import booking_bp
from services.notification_service import notification_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saruman_tokien'
def initialize_database():
    init_db()

app.register_blueprint(user_bp, url_prefix='/usuario')
app.register_blueprint(space_bp, url_prefix='/espacoscomuns')
app.register_blueprint(visitor_bp, url_prefix='/visitantes')
app.register_blueprint(fee_bp, url_prefix='/taxas')
app.register_blueprint(booking_bp, url_prefix='/agendamento')
app.register_blueprint(notification_bp, url_prefix='/notificacoes')


# Rota para a página inicial (exemplo)
@app.route('/calendario')
def home():
    return render_template('calendario.html')

if __name__ == '__main__':
    app.run(debug=True)
