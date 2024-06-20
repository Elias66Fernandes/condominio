from flask import Blueprint, request, jsonify, render_template
from models import Agendamento, Usuarios
from database import get_db_session
from datetime import datetime
from utils import get_logged_in_user_id, login_required
import pytz
booking_bp = Blueprint('booking_bp', __name__)
@login_required
@booking_bp.route('/', methods=['POST'])
def criar_agendamento():
    data = request.form
    espaco_id = int(data['espaco_id'])
    usuario_id = get_logged_in_user_id()

    data_inicio = datetime.strptime(data['data_inicio'], "%Y-%m-%dT%H:%M")
    data_fim = datetime.strptime(data['data_fim'], "%Y-%m-%dT%H:%M")

    if not espaco_id or not usuario_id or not data_inicio or not data_fim:
        return jsonify({'error': 'Espaço ID, Usuário ID e datas são obrigatórios'}), 400

    session = next(get_db_session())
    novo_agendamento = Agendamento(espaco_id=espaco_id, usuarios_id=usuario_id, data_inicio=data_inicio, data_fim=data_fim)
    session.add(novo_agendamento)
    session.commit()
    session.close()
    usuario = session.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if usuario.identificador==1:
        return render_template("pag_adm.html")
    else:
        return render_template("pag_condomino.html")
@login_required
@booking_bp.route('/', methods=['GET'])
def get_agendamentos():
    session = next(get_db_session())
    agendamentos = session.query(Agendamento).all()
    session.close()
    return jsonify([{'id': agendamento.id, 'espaco_id': agendamento.espaco_id, 'usuario_id': agendamento.usuarios_id, 'data_inicio': agendamento.data_inicio.strftime('%Y-%m-%d %H:%M:%S'), 'data_fim': agendamento.data_fim.strftime('%Y-%m-%d %H:%M:%S')} for agendamento in agendamentos])

@booking_bp.route('/alterar', methods=['POST'])
def atualizar_agendamento():
    data = request.form

    old_espaco_id = int(data['old_espaco_id'])
    old_data_inicio = datetime.strptime(data['old_data_inicio'], "%Y-%m-%dT%H:%M")
    old_data_fim = datetime.strptime(data['old_data_fim'], "%Y-%m-%dT%H:%M")


    espaco_id = int(data['espaco_id'])
    data_inicio = datetime.strptime(data['data_inicio'], "%Y-%m-%dT%H:%M")
    data_fim = datetime.strptime(data['data_fim'], "%Y-%m-%dT%H:%M")

    session = next(get_db_session())
    agendamento = session.query(Agendamento).filter(
        Agendamento.espaco_id == old_espaco_id,
        Agendamento.data_inicio == old_data_inicio,
        Agendamento.data_fim == old_data_fim
    ).first()
    
    agendamento.espaco_id = espaco_id
    agendamento.data_inicio = data_inicio
    agendamento.data_fim = data_fim
    session.commit()
    session.close()
    '''
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
    '''
    return render_template('pag_adm.html')