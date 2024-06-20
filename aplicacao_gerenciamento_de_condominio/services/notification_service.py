from flask import Blueprint, request, jsonify,render_template
from models import Notificacao,Usuarios
from database import get_db_session
from datetime import datetime
from utils import get_logged_in_user_id, login_required

notification_bp = Blueprint('notification_bp', __name__)
@login_required
@notification_bp.route('/', methods=['POST'])
def criar_notificacao():
    data = request.form
    usuario_id = get_logged_in_user_id()
    
    mensagem = data.get('mensagem')
    data_manutencao = datetime.strptime(data['data_manutencao'], "%Y-%m-%d")

    if not usuario_id or not mensagem:
        return jsonify({'error': 'Usuário ID e mensagem são obrigatórios'}), 400

    session = next(get_db_session())
    usuario = session.query(Usuarios).filter(Usuarios.id == usuario_id).one()
    nova_notificacao = Notificacao(usuarios_id=usuario_id, mensagem=mensagem,data=data_manutencao)
    session.add(nova_notificacao)
    session.commit()
    session.close()


    session = next(get_db_session())
    usuario = session.query(Usuarios).filter(Usuarios.id == usuario_id).one()
    session.close()
    if usuario.identificador == 3:
        return render_template("pag_portaria.html")
    else:
        return render_template("pag_adm.html")

@notification_bp.route('/', methods=['GET'])
def get_notificacoes():
    session = next(get_db_session())
    notificacoes = session.query(Notificacao).all()
    session.close()
    return jsonify([{'id': notificacao.id, 'usuario_id': notificacao.usuarios_id, 'mensagem': notificacao.mensagem, 'data': notificacao.data} for notificacao in notificacoes])
