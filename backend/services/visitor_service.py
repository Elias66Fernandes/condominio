from flask import Blueprint, request, jsonify
from models import Visitantes
from database import get_db_session
from datetime import datetime
import json

visitor_bp = Blueprint('visitor_bp', __name__)

@visitor_bp.route('/', methods=['POST'])
def criar_visitante():
    data = request.form
    usuarios_id = int(data.get('usuarios_id'))
    visitantes = json.dumps(list(data['visitantes']))
    data_visita = datetime.strptime(data['data_visita'], "%Y-%m-%d")

    if not usuarios_id or not visitantes:
        return jsonify({'error': 'Usuários ID e pessoas são obrigatórios'}), 400

    session = next(get_db_session())
    novo_visitante = Visitantes(usuarios_id=usuarios_id, visitantes=visitantes, data_visita=data_visita)
    session.add(novo_visitante)
    session.commit()
    session.close()
    return jsonify({'message': 'Visitante criado com sucesso'}), 201

@visitor_bp.route('/', methods=['GET'])
def get_visitantes():
    session = next(get_db_session())
    visitantes = session.query(Visitantes).all()
    session.close()
    return jsonify([{'id': visitante.id, 'usuarios_id': visitante.usuarios_id, 'visitantes': json.loads(visitante.visitantes), 'data_visita': visitante.data_visita.strftime('%Y-%m-%d')} for visitante in visitantes])
