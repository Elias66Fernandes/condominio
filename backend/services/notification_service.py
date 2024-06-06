from flask import Blueprint, request, jsonify
from models import Notificacao
from database import get_db_session

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/', methods=['POST'])
def criar_notificacao():
    data = request.form
    usuario_id = int(data.get('usuario_id'))
    mensagem = data.get('mensagem')

    if not usuario_id or not mensagem:
        return jsonify({'error': 'Usuário ID e mensagem são obrigatórios'}), 400

    session = next(get_db_session())
    nova_notificacao = Notificacoes(usuario_id=usuario_id, mensagem=mensagem)
    session.add(nova_notificacao)
    session.commit()
    session.close()
    return jsonify({'message': 'Notificação criada com sucesso'}), 201

@notification_bp.route('/', methods=['GET'])
def get_notificacoes():
    session = next(get_db_session())
    notificacoes = session.query(Notificacoes).all()
    session.close()
    return jsonify([{'id': notificacao.id, 'usuario_id': notificacao.usuario_id, 'mensagem': notificacao.mensagem} for notificacao in notificacoes])
