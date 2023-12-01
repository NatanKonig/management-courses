from peewee import *
from datetime import datetime
from db_utils import db

class BaseModel(Model):
    criado_em = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        abstract = True

class Usuario(BaseModel):
    username = CharField(max_length=100)
    password = CharField(max_length=100)
    email = CharField(max_length=100)

class Admin(Usuario):
    pass

class Aluno(Usuario):
    matricula = IntegerField()
    nome = CharField(max_length=100)
    cpf = CharField(max_length=14)
    telefone = CharField(max_length=14)
    data_nascimento = DateField()

class Professor(Usuario):
    matricula = IntegerField()
    nome = CharField(max_length=100)
    cpf = CharField(max_length=14)
    telefone = CharField(max_length=14)
    data_nascimento = DateField()

class Curso(BaseModel):
    nome = CharField(max_length=100)
    coordenador = ForeignKeyField(Professor, backref='Curso')
    descricao = TextField()
    carga_horaria = IntegerField()
    data_inicio = DateField()

class Turma(BaseModel):
    sala = CharField(max_length=10)
    curso = ForeignKeyField(Curso, backref='Turma')
    max_alunos = IntegerField()  
    horario = CharField()

class AlunoTurma(Model):
    aluno = ForeignKeyField(Aluno, backref='AlunoTurma')
    turma = ForeignKeyField(Turma, backref='AlunoTurma')

    class Meta:
        database = db

class ProfessorTurma(Model):
    turma = ForeignKeyField(Turma, backref='ProfessorTurma')
    professor = ForeignKeyField(Professor, backref='ProfessorTurma')

    class Meta:
        database = db