from flask import Blueprint, request, jsonify
from models import Taxas
from database import get_db_session
from datetime import datetime

fee_bp = Blueprint('fee_bp', __name__)

@fee_bp.route('/', methods=['POST'])
def criar_taxa():
    data = request.form
    descricao = data.get('descricao')
    valor = float(data.get('valor'))
    vencimento = datetime.strptime(data.get('vencimento'), "%Y-%m-%d")

    if not descricao or not valor:
        return jsonify({'error': 'Descrição e valor são obrigatórios'}), 400

    session = next(get_db_session())
    nova_taxa = Taxas(descricao=descricao, valor=valor, vencimento=vencimento)
    session.add(nova_taxa)
    session.commit()
    session.close()
    return jsonify({'message': 'Taxa criada com sucesso'}), 201

@fee_bp.route('/', methods=['GET'])
def get_taxas():
    session = next(get_db_session())
    taxas = session.query(Taxas).all()
    session.close()
    return jsonify([{'id': taxa.id, 'descricao': taxa.descricao, 'valor': taxa.valor, 'vencimento': taxa.vencimento.strftime('%Y-%m-%d')} for taxa in taxas])
