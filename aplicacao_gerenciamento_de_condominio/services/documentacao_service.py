from flask import Blueprint, request, jsonify, session, flash, render_template, redirect, send_file, make_response, abort

from models import Documentacoes2
from database import get_db_session
from utils import hash_password, check_password
from datetime import datetime
import json
from utils import login_required
import os
import io
from utils import get_logged_in_user_id, login_required
from base64 import b64encode

documentacao_bp = Blueprint('documentacao_bp', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@documentacao_bp.route('/', methods=['GET','POST'])
def registro_documentacao():
    if request.method == 'POST':
        data = request.form
        nome_documento = data['titulo_doc']
        assunto_documento = data['assunto_doc']
        data_doc = datetime.strptime(data['data_doc'], "%Y-%m-%d")
        documento = request.files['file']
        documento = documento.read()
        session = next(get_db_session())

        novo_documento = Documentacoes2(nome=nome_documento,assunto=assunto_documento,documento=documento,data=data_doc)
        session.add(novo_documento)
        session.commit()
        session.close()
        
    return render_template('pag_adm.html')

@documentacao_bp.route('/documento', methods=['GET'])
def get_documentacoes():
    session = next(get_db_session())
    documentacoes = session.query(Documentacoes2).all()
    session.close()
    return jsonify([{'id': documentacao.id, 'nome': documentacao.nome, 'assunto_documento': documentacao.assunto, 'data': documentacao.data.strftime('%Y-%m-%d')} for documentacao in documentacoes])

@documentacao_bp.route('/download/<int:doc_id>', methods=['GET'])
def download_documento(doc_id):
    session = next(get_db_session())
    doc = session.query(Documentacoes2).filter(Documentacoes2.id == doc_id).first()
    file_entry = doc.documento
    session.close()
    if file_entry:
        # Reconstruct the file based on the file_hash (this is a placeholder, adjust based on your actual storage mechanism)
        file_data = io.BytesIO(file_entry)
        file_data.seek(0)
        response = send_file(
            file_data, 
            as_attachment=True, 
            download_name=f"{doc.nome}.pdf",
            mimetype='application/pdf'
        )
        return response
    else:
        return abort(404, description="File not found")

@documentacao_bp.route('/<int:user_id>', methods=['GET'])
def obter_documento_por_id(user_id):
    session = next(get_db_session())

    documentacao = session.query(Documentacoes2).filter(Documentacoes2.id == int(user_id)).first()
    session.close()

    if not documentacao:
        return jsonify({'error': 'Documentacao não encontrado'}), 404

    return jsonify({
        'id': documentacao.id,
        'name': documentacao.nome,
        'assunto': documentacao.assunto,
        'data': documentacao.data,
    }), 200

@documentacao_bp.route('/atualizar', methods=['POST'])
def atualizar_documento():

    data = request.form
    user_id = data.get('ID_doc')

    novo_nome = data['titulo_doc']
    novo_assunto = data['assunto_doc']
    novo_data = datetime.strptime(data['data_doc'], "%Y-%m-%d")

    documento = request.files['file']
    documento = documento.read()
    session = next(get_db_session())

    documentacao = session.query(Documentacoes2).filter(Documentacoes2.id == int(user_id)).first()

    if not documentacao:
        return jsonify({'error': 'Documentacao não encontrado'}), 404

    if documento:
        documentacao.documento=documento
    documentacao.nome=novo_nome
    documentacao.assunto=novo_assunto
    documentacao.data=novo_data
    session.commit()
    session.close()
    return render_template('pag_adm.html')

@documentacao_bp.route('/delete/<int:doc_id>', methods=['POST'])
def excluir_usuario(doc_id):
    session = next(get_db_session())
    usuario = session.query(Documentacoes2).filter(Documentacoes2.id == doc_id).first()

    if not usuario:
        session.close()
        return jsonify({'error': 'Usuário não encontrado'}), 404

    session.delete(usuario)
    session.commit()
    session.close()
    return render_template('pag_adm.html')