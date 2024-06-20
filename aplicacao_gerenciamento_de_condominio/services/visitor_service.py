from flask import Blueprint, request, jsonify, render_template
from models import Visitantes
from database import get_db_session
from datetime import datetime
import json
from utils import *
visitor_bp = Blueprint('visitor_bp', __name__)
@login_required
@visitor_bp.route('/', methods=['POST'])
def criar_visitante():
    data = request.form
    usuarios_id = get_logged_in_user_id()
    visitantes = []
    # Coleta informações de visitantes
    for i in range(1, 10):  # Define o limite máximo de visitantes
        nome_dependente = request.form.get(f'visitante_nome_{i}', '')
        cpf_dependente = request.form.get(f'visitante_cpf_{i}', '')

        # Se algum dos campos estiver vazio, interrompe a coleta
        if not nome_dependente or not cpf_dependente:
            break
        visitantes.append({'nome': nome_dependente, 'cpf': cpf_dependente})
    visitantes = json.dumps(visitantes)
    data_visita = datetime.strptime(data['data_visita'], "%Y-%m-%d")

    if not usuarios_id or not visitantes:
        return jsonify({'error': 'Usuários ID e pessoas são obrigatórios'}), 400

    session = next(get_db_session())
    novo_visitante = Visitantes(usuarios_id=usuarios_id, pessoas=visitantes, data=data_visita)
    session.add(novo_visitante)
    session.commit()
    session.close()
    return render_template("pag_condomino.html")

@visitor_bp.route('/', methods=['GET'])
def get_visitantes():
    session = next(get_db_session())
    visitantes = session.query(Visitantes).all()
    session.close()
    return jsonify([{'id': visitante.id, 'usuarios_id': visitante.usuarios_id, 'visitantes': json.loads(visitante.pessoas), 'data_visita': visitante.data.strftime('%Y-%m-%d')} for visitante in visitantes])

@visitor_bp.route('/usuario', methods=['GET'])
def get_visitantes_usuario():
    session = next(get_db_session())
    id = get_logged_in_user_id()
    visitantes = session.query(Visitantes).filter(Visitantes.usuarios_id == id)
    session.close()
    return jsonify([{'id': visitante.id, 'usuarios_id': visitante.usuarios_id, 'visitantes': json.loads(visitante.pessoas), 'data_visita': visitante.data.strftime('%Y-%m-%d')} for visitante in visitantes])

@visitor_bp.route('/atualizar', methods=['POST'])
def atualizar_visitantes():
    data = request.form
    id = data['id_visita']
    
    usuarios_id = get_logged_in_user_id()
    visitantes = []
    # Coleta informações de visitantes
    for i in range(1, 10):  # Define o limite máximo de visitantes
        nome_dependente = request.form.get(f'visitante_nome_{i}', '')
        cpf_dependente = request.form.get(f'visitante_cpf_{i}', '')
        print(nome_dependente) 
        print(cpf_dependente) 
        # Se algum dos campos estiver vazio, interrompe a coleta
        if not nome_dependente or not cpf_dependente:
            break
        visitantes.append({'nome': nome_dependente, 'cpf': cpf_dependente})
    print(visitantes) 
    visitantes = json.dumps(visitantes)
    data_visita = datetime.strptime(data['data_visita'], "%Y-%m-%d")

    if not usuarios_id or not visitantes:
        return jsonify({'error': 'Usuários ID e pessoas são obrigatórios'}), 400

    session = next(get_db_session())
    visitante = session.query(Visitantes).filter(Visitantes.id == id).first()
    visitante.pessoas=visitantes
    visitante.data=data_visita
    session.commit()
    session.close()
    return render_template("pag_condomino.html")


@visitor_bp.route('/<int:id>', methods=['DELETE'])
def excluir_visitante(id):
    session = next(get_db_session())
    visitante = session.query(Visitantes).filter(Visitantes.id == id).first()
    
    if not visitante:
        session.close()
        return jsonify({'error': 'Visitante não encontrado'}), 404

    session.delete(visitante)
    session.commit()
    session.close()
    
    return jsonify({'message': 'Visitante excluído com sucesso'}), 200