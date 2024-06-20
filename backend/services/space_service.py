from flask import Blueprint, request, jsonify, redirect, render_template
from models import EspacosComuns
from database import get_db_session
from utils import login_required
space_bp = Blueprint('space_bp', __name__)
@login_required
@space_bp.route('/', methods=['POST'])
def registro_espacos():
    data = request.form
    nome = data['nome_espaco']
    session = next(get_db_session())

    if session.query(EspacosComuns).filter(EspacosComuns.nome == nome).first():
        session.close()
        return jsonify({'error': 'Espaço já existe'}), 400

    novo_espaco = EspacosComuns(nome=nome)
    session.add(novo_espaco)
    session.commit()
    session.close()
    return render_template("pag_adm.html")
@login_required
@space_bp.route('/', methods=['GET'])
def get_espacos_comuns():
    session = next(get_db_session())
    espacos = session.query(EspacosComuns).all()
    session.close()
    return jsonify([{'id': espaco.id, 'name': espaco.nome} for espaco in espacos])
@login_required
@space_bp.route('/atualizar', methods=['POST'])
def atualizar_espaco():
    data = request.form
    print(data)
    espaco_id = int(data.get('id_espaco'))
    novo_nome = data.get('nome_espaco')

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
    return render_template("pag_adm.html")
@login_required
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
    return render_template("pag_adm.html")
