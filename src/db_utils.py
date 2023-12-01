from peewee import SqliteDatabase, DoesNotExist
db = SqliteDatabase("escola.db")
from models import Admin, Aluno, Professor, Curso, Turma, AlunoTurma, ProfessorTurma


tables = [Admin, Aluno, Professor, Curso, Turma, AlunoTurma, ProfessorTurma]

def criar_db():
    ''''''
    db.connect()

    # Verifica se cada tabela existe antes de criá-la
    db.create_tables(tables)

    # Exemplo de criação de um registro Admin
    try:
        admin = Admin.get(Admin.username == 'Admin')
    except DoesNotExist:
        admin = Admin.create(username='Admin', password='1234', email='admin@gmail.com')

    db.close()


