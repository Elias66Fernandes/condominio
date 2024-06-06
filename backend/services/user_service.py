from flask import Blueprint, request, jsonify, session, flash, render_template, redirect

from models import Usuarios
from database import get_db_session
from utils import hash_password, check_password
from datetime import datetime
import json

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/registro', methods=['GET','POST'])
def registro_usuarios():
    if request.method == 'POST':
        data = request.form
        nome = data['nome']
        username = data['username']
        email = data['email']
        cpf = data['cpf']
        data_nascimento = datetime.strptime(data['data_nascimento'], "%Y-%m-%d")
        ctt = data['ctt']
        password = data['senha']
        identificador = int(data['identificador'])
        dependentes = []
        # Coleta informações de dependentes
        for i in range(1, 10):  # Define o limite máximo de dependentes
            nome_dependente = request.form.get(f'dependente_nome_{i}', '')
            cpf_dependente = request.form.get(f'dependente_cpf_{i}', '')

            # Se algum dos campos estiver vazio, interrompe a coleta
            if not nome_dependente or not cpf_dependente:
                break
            dependentes.append({'nome': nome_dependente, 'cpf': cpf_dependente})
        dependentes = json.dumps(dependentes)
        data_admissao = datetime.strptime(data['admissao'], "%Y-%m-%d")
        session = next(get_db_session())

        if session.query(Usuarios).filter((Usuarios.username == username) | (Usuarios.email == email)).first():
            session.close()
            return jsonify({'error': 'User already exists'}), 400

        hashed_password = hash_password(password)
        novo_usuario = Usuarios(username=username, email=email, senha=hashed_password, nome=nome, data_nascimento=data_nascimento, ctt=ctt, cpf=cpf, identificador=identificador, dependentes=dependentes, admissao=data_admissao)
        session.add(novo_usuario)
        session.commit()
        session.close()
        return jsonify({'message': 'User created successfully'}), 201
        
    return render_template('registro.html')

@user_bp.route('/', methods=['GET'])
def obter_usuarios():
    session = next(get_db_session())
    users = session.query(Usuarios).all()
    session.close()
    return jsonify([{'id': user.id, 'name': user.nome, 'email': user.email, 'dependentes': json.loads(user.dependentes), 'contato': user.ctt} for user in users])

@user_bp.route('/<int:user_id>', methods=['PUT'])
def atualizar_usuario(user_id):
    data = request.form
    novo_email = data.get('email')
    novo_contato = data.get('ctt')
    nova_senha = data.get('senha')
    novos_dependentes = data['dependentes']

    if not user_id:
        return jsonify({'error': 'ID do usuário é necessário'}), 400

    session = next(get_db_session())
    usuario = session.query(Usuarios).filter(Usuarios.id == user_id).first()

    if not usuario:
        session.close()
        return jsonify({'error': 'Usuário não encontrado'}), 404

    if novo_email:
        usuario.email = novo_email
    if novo_contato:
        usuario.ctt = novo_contato
    if nova_senha:
        usuario.senha = hash_password(nova_senha)
    if novos_dependentes is not None:
        usuario.dependentes = json.dumps(novos_dependentes)

    session.commit()
    session.close()
    return jsonify({'message': 'Usuário atualizado com sucesso'}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def excluir_usuario(user_id):
    session = next(get_db_session())
    usuario = session.query(Usuarios).filter(Usuarios.id == user_id).first()

    if not usuario:
        session.close()
        return jsonify({'error': 'Usuário não encontrado'}), 404

    session.delete(usuario)
    session.commit()
    session.close()
    return jsonify({'message': 'Usuário excluído com sucesso'}), 200

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        db_session = next(get_db_session())
        user = db_session.query(Usuarios).filter(Usuarios.username == username).first()
        db_session.close()

        if user and check_password(user.senha, password):
            session['username'] = username
            session['logged_in'] = True
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 400

    return render_template('login.html')
