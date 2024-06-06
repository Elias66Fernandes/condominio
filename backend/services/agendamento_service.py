from flask import Blueprint, request, jsonify
from models import Agendamento
from database import get_db_session
from datetime import datetime

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/', methods=['POST'])
def criar_agendamento():
    data = request.get_json()
    espaco_id = int(data['espaco_id'])
    usuario_id = int(data['usuarios_id'])
    data_inicio = datetime.strptime(data['data_inicio'], "%Y-%m-%dT%H:%M:%S")
    data_fim = datetime.strptime(data['data_fim'], "%Y-%m-%dT%H:%M:%S")

    if not espaco_id or not usuario_id or not data_inicio or not data_fim:
        return jsonify({'error': 'Espaço ID, Usuário ID e datas são obrigatórios'}), 400

    session = next(get_db_session())
    novo_agendamento = Agendamento(espaco_id=espaco_id, usuarios_id=usuario_id, data_inicio=data_inicio, data_fim=data_fim)
    session.add(novo_agendamento)
    session.commit()
    session.close()
    return jsonify({'message': 'Agendamento criado com sucesso'}), 201

@booking_bp.route('/', methods=['GET'])
def get_agendamentos():
    session = next(get_db_session())
    agendamentos = session.query(Agendamento).all()
    session.close()
    return jsonify([{'id': agendamento.id, 'espaco_id': agendamento.espaco_id, 'usuario_id': agendamento.usuarios_id, 'data_inicio': agendamento.data_inicio.strftime('%Y-%m-%d %H:%M:%S'), 'data_fim': agendamento.data_fim.strftime('%Y-%m-%d %H:%M:%S')} for agendamento in agendamentos])
