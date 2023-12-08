from peewee import *
from datetime import datetime
from db_utils import db

class BaseModel(Model):
    criado_em = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        abstract = True

class Usuario(BaseModel):
    username = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)

class Admin(Usuario):
    pass

class Aluno(Usuario):
    matricula = IntegerField()
    nome = CharField(max_length=100)
    cpf = CharField(max_length=14)
    telefone = CharField(max_length=14)
    data_nascimento = DateField()
    sexo = CharField(max_length=1)

class Professor(Usuario):
    matricula = IntegerField()
    nome = CharField(max_length=100)
    cpf = CharField(max_length=14)
    telefone = CharField(max_length=14)
    data_nascimento = DateField()
    sexo = CharField(max_length=1)

class Curso(BaseModel):
    nome = CharField(max_length=100)
    coordenador = ForeignKeyField(Professor, backref='curso')
    descricao = TextField()
    carga_horaria = IntegerField()
    data_inicio = DateField()

class Turma(BaseModel):
    sala = CharField(max_length=10)
    curso = ForeignKeyField(Curso, backref='turma')
    max_alunos = IntegerField()  
    horario = CharField()

class AlunoTurma(BaseModel):
    aluno = ForeignKeyField(Aluno, backref='turmas')
    turma = ForeignKeyField(Turma, backref='alunos')

class ProfessorTurma(BaseModel):
    turma = ForeignKeyField(Turma, backref='professores')
    professor = ForeignKeyField(Professor, backref='turmas')