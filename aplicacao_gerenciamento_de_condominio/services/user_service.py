from flask import Blueprint, request, jsonify, session, flash, render_template, redirect, send_file

from models import Usuarios
from database import get_db_session
from utils import hash_password, check_password
from datetime import datetime
import json
from utils import login_required
import os
import io
from utils import get_logged_in_user_id, login_required
from base64 import b64encode


user_bp = Blueprint('user_bp', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        imagem = request.files['file']
        if imagem:
            caminho_imagem = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho_imagem)
            with open(caminho_imagem, 'rb') as file:
                blob = file.read()
            
            # Convertendo a imagem para binário
            imagem_blob = blob


        session = next(get_db_session())
        if session.query(Usuarios).filter((Usuarios.username == username) | (Usuarios.email == email)).first():
            session.close()
            return jsonify({'error': 'User already exists'}), 400

        hashed_password = hash_password(password)
        novo_usuario = Usuarios(username=username, email=email, senha=hashed_password, nome=nome, data_nascimento=data_nascimento, ctt=ctt, cpf=cpf, identificador=identificador, dependentes=dependentes, admissao=data_admissao, imagem=imagem_blob)
        session.add(novo_usuario)
        session.commit()
        session.close()
        
    return render_template('pag_adm.html')
@login_required
@user_bp.route('/perfil', methods=['GET'])
def get_perfil():
    session = next(get_db_session())
    usuario_id = get_logged_in_user_id()

    usuario = session.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if usuario:
        # Codifica a imagem em base64
        imagem_base64 = b64encode(usuario.imagem).decode('utf-8') if usuario.imagem else None
        return jsonify({
            "email": usuario.email,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "data_nascimento": usuario.data_nascimento.strftime('%Y-%m-%d'),
            "identificador": usuario.identificador,
            "imagem": imagem_base64,
            "ctt": usuario.ctt
        })
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

@user_bp.route('/atualizar_perfil', methods=['GET','POST'])
def atualizar_perfil():
    if request.method == 'POST':
        
        data = request.form
        nome = data['nome_alterar']
        email = data['email_alterar']
        ctt = data['ctt_alterar']
        password = data['senha_alterar']
        imagem = request.files['file_alterar']
        


        session = next(get_db_session())
        

        usuario_id = get_logged_in_user_id()
        usuario = session.query(Usuarios).filter(Usuarios.id == usuario_id).first()

        if nome:
            usuario.nome=nome
        
        if email:
            usuario.email=email
        if password!='':
            hashed_password = hash_password(password)
            usuario.senha=hashed_password
        if ctt:
            usuario.ctt=ctt
        
        if imagem:
            caminho_imagem = os.path.join(UPLOAD_FOLDER, imagem.filename)
            imagem.save(caminho_imagem)
            with open(caminho_imagem, 'rb') as file:
                blob = file.read()
            
            # Convertendo a imagem para binário
            imagem_blob = blob
            usuario.imagem=imagem_blob
        
    if usuario.identificador==1:
        session.commit()
        session.close()
        return render_template('pag_adm.html')

    elif usuario.identificador==2:
        session.commit()
        session.close()
        return render_template('pag_condomino.html')
    else:
        session.commit()
        session.close()
        return render_template('pag_portaria.html')


@user_bp.route('/', methods=['GET'])
def obter_usuarios():
    session = next(get_db_session())
    users = session.query(Usuarios).all()
    session.close()
    return jsonify([{'id': user.id, 'name': user.nome, 'email': user.email, 'dependentes': json.loads(user.dependentes), 'contato': user.ctt, 'cpf':user.cpf, 'identificador':user.identificador,'username':user.username,'dataNascimento':user.data_nascimento,'admissao':user.admissao} for user in users])

@login_required
@user_bp.route('/alterar', methods=['POST'])
def atualizar_usuario():
    data = request.form
    user_id = data.get('id')
    novo_nome = data['nome']
    novo_username = data['username']
    novo_email = data['email']
    novo_cpf = data['cpf']
    novo_data_nascimento = data['data_nascimento']
    novo_contato = data['ctt']
    nova_senha = data['senha']
    novo_identificador = int(data['identificador'])
    novo_email = data.get('email')

    dependentes = []
    # Coleta informações de dependentes
    for i in range(1, 10):  # Define o limite máximo de dependentes
        nome_dependente = request.form.get(f'dependente_nome_{i}', '')
        cpf_dependente = request.form.get(f'dependente_cpf_{i}', '')

        # Se algum dos campos estiver vazio, interrompe a coleta
        if not nome_dependente or not cpf_dependente:
            break
        dependentes.append({'nome': nome_dependente, 'cpf': cpf_dependente})
    novos_dependentes = json.dumps(dependentes)

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
    if novo_nome:
        usuario.nome = novo_nome
    if novo_username:
        usuario.username = novo_username
    if novo_cpf:
        usuario.cpf = novo_cpf
    if novo_data_nascimento:
        usuario.data_nascimento = datetime.strptime(novo_data_nascimento, "%Y-%m-%d")
    usuario.identificador=novo_identificador
    session.commit()
    session.close()
    return render_template('pag_adm.html')

@login_required
@user_bp.route('/<int:user_id>', methods=['GET'])
def obter_usuario_por_id(user_id):
    session = next(get_db_session())

    usuario = session.query(Usuarios).filter(Usuarios.id == int(user_id)).first()
    session.close()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify({
        'id': usuario.id,
        'name': usuario.nome,
        'email': usuario.email,
        'dependentes': json.loads(usuario.dependentes),
        'contato': usuario.ctt,
        'cpf': usuario.cpf,
        'identificador': usuario.identificador,
        'username': usuario.username,
        'dataNascimento': usuario.data_nascimento,
        'admissao':usuario.admissao
    }), 200

@login_required
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
    return render_template('pag_adm.html')

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
            session['user_id'] = user.id
            session['username'] = username
            session['logged_in'] = True
            if user.identificador==1:
                return render_template('pag_adm.html')
            elif user.identificador==3:
                return render_template('pag_portaria.html')
            else:
                return render_template('pag_condomino.html')
        else:
            return jsonify({'error': 'Invalid username or password'}), 400

    return render_template('login.html')
@login_required
@user_bp.route('/administracao', methods=['GET', 'POST'])
def administracao():
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

    return render_template('pag_adm.html')

@user_bp.route('/condominos', methods=['GET'])
def obter_condominos():
    session = next(get_db_session())
    users = session.query(Usuarios).filter(Usuarios.identificador == 2).all()
    session.close()
    return jsonify([{'id': user.id, 'name': user.nome, 'username': user.username} for user in users])

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Limpa todas as informações da sessão
    return redirect('/usuario/login')  # Redireciona para a tela de login
