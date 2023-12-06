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
        admin = Admin.create(username='Admin', password='1', email='admin@gmail.com')
        aluno = Aluno.create(username='Aluno', password='1234', email='aluno@gmail.com', matricula = "202311", nome= 'Aluno', cpf='194.411.780-63', telefone='(61) 2847-8735',data_nascimento='2000-10-09',sexo='M')
        professor = Professor.create(username='Professor', password='1234', email='professor@gmail.com', matricula = "202312", nome= 'Professor', cpf='847.949.220-19', telefone='(61) 2848-8785',data_nascimento='1980-10-09',sexo='M')
        curso = Curso.create(nome="Curso de Matemática", coordenador = 1, descricao = 'É us guri', carga_horaria=250,data_inicio = '1980-10-09')
        turma = Turma.create(sala='B205', nome="Matemática 1º ANO", curso = 1, max_alunos = 30, horario = '8:00 - 12:00')

    db.close()


