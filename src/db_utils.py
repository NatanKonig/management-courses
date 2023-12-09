from peewee import *
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
        aluno = Aluno.create(username='Aluno', password='1', email='aluno@gmail.com', matricula = "202311", nome= 'Aluno', cpf='194.411.780-63',
                              telefone='(61) 2847-8735',data_nascimento='2000-10-09',sexo='M')
        aluno1 = Aluno.create(username='OutroAluno', password='senha123', email='outroaluno@gmail.com', matricula='202312', nome='Outro Aluno', cpf='123.456.789-01', 
                              telefone='(62) 9876-5432', data_nascimento='1998-05-15', sexo='F')
        aluno2 = Aluno.create(username='NovoAluno', password='senhasecreta', email='novoaluno@gmail.com', matricula='202313', nome='Novo Aluno', cpf='987.654.321-09', 
                              telefone='(55) 1234-5678', data_nascimento='1995-12-20', sexo='M')
        professor = Professor.create(username='Professor', password='1234', email='professor@gmail.com', matricula = "202321", nome= 'Professor', 
                                     cpf='847.949.220-19', telefone='(61) 2848-8785',data_nascimento='1980-10-09',sexo='M')
        professor1 = Professor.create(username='OutroProfessor', password='senha456', email='outroprofessor@gmail.com', matricula='202322', nome='Outro Professor', 
                                      cpf='567.890.123-45', telefone='(62) 8765-4321', data_nascimento='1975-08-25', sexo='F')
        professor2 = Professor.create(username='NovoProfessor', password='senhasegura', email='novoprofessor@gmail.com', matricula='202323', nome='Novo Professor', 
                                      cpf='234.567.890-12', telefone='(55) 8765-4321', data_nascimento='1988-03-15', sexo='M')
        curso = Curso.create(nome="Curso de Matemática", coordenador = 1, descricao = 'É us guri', carga_horaria=250, data_inicio = '1980-10-09')
        curso1 = Curso.create(nome="Curso de Informatica", coordenador=2, descricao='Explorando o mudo da programação', carga_horaria=200, data_inicio='1990-05-20')
        curso2 = Curso.create(nome="Curso de Ciências da Computação", coordenador=3, descricao='Explorando o mundo da computação', carga_horaria=300, data_inicio='2005-09-15')
        turma = Turma.create(sala='B205', curso = 1, max_alunos = 30, horario = '8:00 - 12:00')
        turma1 = Turma.create(sala='C301', curso=2, max_alunos=25, horario='14:00 - 18:00')
        turma2 = Turma.create(sala='A102', curso=3, max_alunos=20, horario='10:00 - 14:00')
        alunoturma = AlunoTurma.create(aluno_id=1, turma_id=1)
        aluno_turma2 = AlunoTurma.create(aluno_id=2, turma_id=2)
        aluno_turma3 = AlunoTurma.create(aluno_id=3, turma_id=1)
        aluno_turma4 = AlunoTurma.create(aluno_id=1, turma_id=2)
        professorturma = ProfessorTurma.create(professor_id=1,turma_id=1)
        professor_turma2 = ProfessorTurma.create(professor_id=2, turma_id=2)
        professor_turma3 = ProfessorTurma.create(professor_id=3, turma_id=1)

    db.close()

def update_aluno(username, password, email, telefone, usuario):
    # Atualize o usuário
    Aluno.update(
        username=username,
        password=password,
        email=email,
        telefone=telefone
    ).where(Aluno.id == usuario.id).execute()

def listar(tipo):
    lista = []
    if tipo == 'aluno':
        lista = Aluno.select()
    elif tipo == 'professor':
        lista = Professor.select()
    elif tipo == 'curso':
        lista = Curso.select()
    elif tipo == 'turma':
        lista = Turma.select()
    
    return lista

def login(username, password):
    # Tenta autenticar como Admin
    admin_user = Admin.select().where((Admin.username == username) & (Admin.password == password)).first()
    if admin_user:
        print("Login como Admin bem-sucedido")
        return admin_user, 'admin'

    # Tenta autenticar como Aluno
    aluno_user = Aluno.select().where((Aluno.username == username) & (Aluno.password == password)).first()
    if aluno_user:
        print("Login como Aluno bem-sucedido")
        return aluno_user, 'aluno'

    # Tenta autenticar como Professor
    professor_user = Professor.select().where((Professor.username == username) & (Professor.password == password)).first()
    if professor_user:
        print("Login como Professor bem-sucedido")
        return professor_user, 'professor'

    # Se nenhum usuário foi autenticado, retorna None
    print("Falha na autenticação")
    return None, None

def criar_matricula(tipo):
    from datetime import datetime
    m = ''
    m += f'{datetime.now().year}'

    if tipo == 'aluno':
        m += '1'
        m += f'{Aluno.select(fn.Max(Aluno.id)).scalar() + 1}'
    elif tipo == 'professor':
        m += '2'
        m += f'{Professor.select(fn.Max(Professor.id)).scalar() + 1}'

    return m

def contar_alunos_matriculados_na_turma(turma_id):
    # Contar o número de registros na tabela de associação AlunoTurma para a turma específica
    quantidade_alunos = AlunoTurma.select().where(AlunoTurma.turma == turma_id).count()
    return quantidade_alunos

def matricular_aluno_na_turma(aluno_id, curso_id):
    # Obter todas as turmas para o curso especificado
    turmas_curso = Turma.select().where(Turma.curso == curso_id)

    # Filtrar turmas com vagas disponíveis
    turmas_disponiveis = [turma for turma in turmas_curso if contar_alunos_matriculados_na_turma(turma.id) < turma.max_alunos]

    # Verificar se há turmas disponíveis
    if turmas_disponiveis:
        # Matricular o aluno na primeira turma disponível
        turma = turmas_disponiveis[0]
        # Criar um registro na tabela de associação AlunoTurma
        AlunoTurma.create(aluno=aluno_id, turma=turma.id)
        return True

def criar_registro_aluno(username, password, email, nome, cpf, telefone, data_nascimento, sexo, curso_id):
    # Verificar se há turmas disponíveis para matrícula no curso específico
    turmas_curso = Turma.select().where(Turma.curso == curso_id)
    turmas_disponiveis = [turma for turma in turmas_curso if contar_alunos_matriculados_na_turma(turma.id) < turma.max_alunos]

    if turmas_disponiveis:
        # Crie uma instância do modelo Aluno
        aluno = Aluno.create(
            username=username,
            password=password,
            email=email,
            matricula=criar_matricula('aluno'),
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            data_nascimento=data_nascimento,
            sexo=sexo
        )

        # Salve o objeto no banco de dados
        aluno.save()

        return aluno
    else:
        return None  # Não há turmas disponíveis para matrícula no curso específico

def criar_registro_professor(username, password, email, nome, cpf, telefone, data_nascimento, sexo):
    # Crie uma instância do modelo Professor
    professor = Professor.create(
        username=username,
        password=password,
        email=email,
        matricula=criar_matricula('professor'),
        nome=nome,
        cpf=cpf,
        telefone=telefone,
        data_nascimento=data_nascimento,
        sexo=sexo
    )

    # Salve o objeto no banco de dados
    professor.save()

def listar_cursos():
    cursos = Curso.select(Curso.id, Curso.nome).order_by(Curso.id)
    l = []
    for curso in cursos:
        l.append(f'{curso.id} {curso.nome}')

    return l

def att_aluno_user(usuario):
    aluno_user = Aluno.select().where(Aluno.id == usuario.id).first()
    return aluno_user

def buscar_turma(sala, curso, horario):
    try:
        print(f"Antes de buscar_turma: {sala}, {curso}, {horario}")
        turma = Turma.select().where(
            (Turma.sala == sala) &
            (Turma.curso == curso) &
            (Turma.horario == horario)
        ).get()
        print("Depois de buscar_turma:", turma)
        return turma
    except Turma.DoesNotExist:
        print("Turma não encontrada.")
        return None
    
def buscar_curso(curso_id):

    curso = Curso.select().where(
        Curso.id == curso_id
        )
    return curso

    
def buscar_curso_nome(curso_id):

    curso = Curso.get(Curso.id == curso_id)
    return curso.nome

def criar_registro_turma(sala, curso, max_alunos, horario, coordenador):
    # Crie a turma
    turma = Turma.create(
        sala=sala,
        curso=curso,
        max_alunos=max_alunos,
        horario=horario,
    )

    # Salve o objeto no banco de dados
    turma.save()

    # Matricule o coordenador na turma
    matricular_coordenador_na_turma(coordenador, turma.id)

    # Se a turma foi criada com sucesso, retorne o objeto turma
    return turma


def criar_registro_curso(nome, coordenador, descricao, carga_horaria, data_inicio):
    # Crie uma instância do modelo Curso
    curso = Curso.create(
        nome=nome,
        coordenador=coordenador,
        descricao=descricao,
        carga_horaria=carga_horaria,
        data_inicio=data_inicio
    )
    # Salve o objeto no banco de dados
    curso.save()

def listar_professores():
    professores = Professor.select(Professor.id, Professor.nome).order_by(Professor.id)
    l = []
    for professor in professores:
        l.append(f'{professor.id} {professor.nome}')

    return l

def matricular_coordenador_na_turma(coordenador, turma_id):
    professorturma = ProfessorTurma.create(
        professor_id=coordenador,
        turma_id=turma_id)

    professorturma.save()

    # Se a matrícula foi bem-sucedida, retorne True
    return True

def listar_turma(user):
    # Seleciona as turmas associadas ao aluno
    faz_turmas = AlunoTurma.select(AlunoTurma.turma_id).where(AlunoTurma.aluno_id == user.id)
    turmas = []
    # Lista informações sobre as turmas
    for turma_associada in faz_turmas:
        # Obtém informações da turma
        turma = Turma.get(Turma.id == turma_associada.turma_id)
        turmas.append(f'{turma.id} {turma.curso.nome}')

        # Exibe algumas informações sobre a turma (substitua isso pelos campos desejados)
    return turmas


def buscar_turma_selecionada(turma_id):
    turma = Turma.select().where(Turma.id == turma_id)
    for i in turma:
        return i.id, i.curso
    
def buscar_curso_sobre(curso_id):

    curso = Curso.select().where(
        Curso.id == curso_id
        )
    for i in curso:
        return i.descricao
    
def buscar_alunos_sobre(turma_id):
    alunos = []
    # Selecione os alunos associados à turma
    alunosturma = AlunoTurma.select().where(
        AlunoTurma.turma_id == turma_id
    )

    # Para cada relação AlunoTurma, obtenha os dados do aluno
    for alunoturma in alunosturma:
        aluno = Aluno.get(Aluno.id == alunoturma.aluno_id)
        # Adicione os dados do aluno à lista
        alunos.append([aluno.matricula, aluno.nome])

    return alunos

def delete_aluno(self):
    id = self.split(' ')[0]
    Aluno.delete().where(Aluno.id == id).execute()

def delete_professor(self):
    id = self.split(' ')[0]
    Professor.delete().where(Professor.id == id).execute()