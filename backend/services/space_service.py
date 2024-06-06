from flask import Blueprint, request, jsonify
from models import EspacosComuns
from database import get_db_session

space_bp = Blueprint('space_bp', __name__)

@space_bp.route('/', methods=['POST'])
def registro_espacos():

    data = request.form
    nome = data['nome']
    session = next(get_db_session())

    if session.query(EspacosComuns).filter(EspacosComuns.nome == nome).first():
        session.close()
        return jsonify({'error': 'Espaço já existe'}), 400

    novo_espaco = EspacosComuns(nome=nome)
    session.add(novo_espaco)
    session.commit()
    session.close()
    return jsonify({'message': 'Espaço adicionado com sucesso'}), 201

@space_bp.route('/', methods=['GET'])
def get_espacos_comuns():
    session = next(get_db_session())
    espacos = session.query(EspacosComuns).all()
    session.close()
    return jsonify([{'id': espaco.id, 'name': espaco.nome} for espaco in espacos])

@space_bp.route('/', methods=['PUT'])
def atualizar_espaco():
    data = request.form
    espaco_id = int(data.get('id'))
    novo_nome = data.get('nome')

    if not espaco_id:
        return jsonify({'error': 'ID do espaço é necessário'}), 400

    session = next(get_db_session())
    espaco = session.query(EspacosComuns).filter(EspacosComuns.id == espaco_id).first()

    if not espaco:
        session.close()
        return jsonify({'error': 'Espaço não encontrado'}), 404

    espaco.nome = novo_nome
    session.commit()
    session.close()
    return jsonify({'message': 'Espaço atualizado com sucesso'}), 200

@space_bp.route('/<int:espaco_id>', methods=['DELETE'])
def excluir_espaco(espaco_id):
    session = next(get_db_session())
    espaco = session.query(EspacosComuns).filter(EspacosComuns.id == espaco_id).first()

    if not espaco:
        session.close()
        return jsonify({'error': 'Espaço não encontrado'}), 404

    session.delete(espaco)
    session.commit()
    session.close()
    return jsonify({'message': 'Espaço excluído com sucesso'}), 200
