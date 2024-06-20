from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date, JSON, LargeBinary, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    ctt = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    identificador = Column(Integer, nullable=False)
    dependentes = Column(JSON, nullable=True)
    admissao = Column(Date, nullable=True)
    imagem = Column(LargeBinary, nullable=True)


class EspacosComuns(Base):
    __tablename__ = 'espacoscomuns'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

class Visitantes(Base):
    __tablename__ = 'visitantes'
    id = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    pessoas = Column(JSON, nullable=False)
    data = Column(Date, nullable=False)

class Taxas(Base):
    __tablename__ = 'taxas'
    id = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    valor = Column(Double, nullable=False)
    data_venc = Column(Date, nullable=False)
    data_cadastro=Column(Date, nullable=False)
    boleto = Column(LargeBinary, nullable=False)

class Reclamacoes(Base):
    __tablename__ = 'reclamacoes'
    id = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    data_boleto=Column(Date, nullable=False)
    texto_reclamacao = Column(String, nullable=False)
    status = Column(Integer, nullable=False)


class Agendamento(Base):
    __tablename__ = 'agendamento'
    id = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    espaco_id = Column(Integer, ForeignKey('espacoscomuns.id'))

class Notificacao(Base):
    __tablename__ = 'notificacoes'
    id = Column(Integer, primary_key=True)
    usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    mensagem = Column(Text, nullable=False)
    data = Column(Date, nullable=False)

class Documentacoes2(Base):
    __tablename__ = 'documentacoes2'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    assunto = Column(String, nullable=False)
    documento = Column(LargeBinary, nullable=False)
    data = Column(Date, nullable=False) 


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
