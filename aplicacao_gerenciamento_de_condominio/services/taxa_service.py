from flask import Blueprint, request, jsonify, send_file, abort, make_response, render_template
from models import Taxas, Reclamacoes,Usuarios
from database import get_db_session
from datetime import datetime, date
import hashlib
from utils import get_logged_in_user_id


fee_bp = Blueprint('fee_bp', __name__)

@fee_bp.route('/', methods=['POST'])
def criar_taxa():
    data = request.form
    boleto = request.files['boleto']
    valor = float(data.get('valor'))
    vencimento = datetime.strptime(data.get('data_venc'), "%Y-%m-%d")
    data_cadastro = date.today()
    usuarios_id = float(data.get('nome_username'))
    boleto = boleto.read()


    session = next(get_db_session())
    nova_taxa = Taxas(boleto=boleto, valor=valor, data_venc=vencimento, data_cadastro=data_cadastro, usuarios_id=usuarios_id)
    session.add(nova_taxa)
    session.commit()
    session.close()
    return render_template('pag_adm.html')

@fee_bp.route('/', methods=['GET'])
def get_taxas():
    session = next(get_db_session())
    taxas = session.query(Taxas).all()
    session.close()
    return jsonify([{'id': taxa.id, 'valor': taxa.valor, 'vencimento': taxa.data_venc.strftime('%Y-%m-%d')} for taxa in taxas])

@fee_bp.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    session = next(get_db_session())
    file_entry = session.query(Taxas).filter_by(boleto=file_hash).first()
    session.close()
    if file_entry:
        # Reconstruct the file based on the file_hash (this is a placeholder, adjust based on your actual storage mechanism)
        return make_response(f"File with hash {file_hash} would be downloaded here.", 200)
    else:
        return abort(404, description="File not found")

@fee_bp.route('/download_ultimo', methods=['GET'])
def download_latest_boleto():
    usuario_id = get_logged_in_user_id()

    session = next(get_db_session())
    try:
        # Query to find the most recent boleto by data_venc
        file_entry = (session.query(Taxas)
                      .filter_by(usuarios_id=usuario_id)
                      .order_by(Taxas.data_venc.desc())
                      .first())
        
        if file_entry:
            response = make_response(file_entry.boleto)
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = f'attachment; filename=boleto_{file_entry.id}.pdf'
            return response
        else:
            return abort(404, description="Boleto not found")
    except Exception as e:
        session.rollback()
        abort(500, description=f"Internal server error: {e}")
    finally:
        session.close()

@fee_bp.route('/reclamacao', methods=['POST'])
def cadastro_reclamacao():
    data = request.form
    descricao = data['descricao']
    usuario_id = get_logged_in_user_id()

    data_boleto = datetime.strptime(data.get('data_boleto'), "%Y-%m-%d")
    session = next(get_db_session())
    nova_reclamacao = Reclamacoes(usuarios_id=usuario_id,data_boleto=data_boleto,texto_reclamacao=descricao,status=0)
    session.add(nova_reclamacao)
    session.commit()
    session.close()
    return render_template("pag_condomino.html")

@fee_bp.route('/atualizar_status', methods=['POST'])
def atualizar_status_reclamacao():
    try:
        data = request.form
        reclamacao_id = data['id']
        novo_status = int(data['status'])

        session = next(get_db_session())
        reclamacao = session.query(Reclamacoes).filter_by(id=reclamacao_id).first()

        if reclamacao is None:
            return jsonify({'error': 'Reclamação não encontrada'}), 404

        reclamacao.status = novo_status
        session.commit()
        session.close()

        return jsonify({'message': 'Status atualizado com sucesso'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500


@fee_bp.route('/reclamacao', methods=['GET'])
def reclamacoes():
    session = next(get_db_session())
    reclamacoes = session.query(Reclamacoes).all()
    users = [session.query(Usuarios).filter(Usuarios.id == reclamacao.usuarios_id).first() for reclamacao in reclamacoes]
    session.close()
    retorno = []
    
    for reclamacao in reclamacoes:
        dados = {}
        dados['id']=reclamacao.id
        try:
            usuario = session.query(Usuarios).filter(Usuarios.id == reclamacao.usuarios_id).first()
            dados['nome']=usuario.nome
            dados['email']=usuario.email
        except:
            dados['nome']="excluido"
            dados['email']="excluido"
        dados['texto_reclamacao']=reclamacao.texto_reclamacao
        dados['status']=reclamacao.status
        dados['data_boleto']=reclamacao.data_boleto
        retorno.append(dados)
    #return jsonify([{'id': user.id, 'name': user.nome, 'email': user.email, 'dependentes': json.loads(user.dependentes), 'contato': user.ctt, 'cpf':user.cpf, 'identificador':user.identificador,'username':user.username,'dataNascimento':user.data_nascimento,'admissao':user.admissao} for reclamacao in reclamacoes])
    return jsonify(retorno)
    