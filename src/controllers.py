from peewee import *
from db_utils import (db, update_aluno, listar, login, criar_matricula, contar_alunos_matriculados_na_turma,
                      matricular_aluno_na_turma, criar_registro_aluno, criar_registro_professor,criar_registro_turma,
                      criar_registro_curso,matricular_coordenador_na_turma)
from models import Admin, Aluno, Professor, Curso, Turma, AlunoTurma, ProfessorTurma

usuario = None

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def telas_controle(tipo_usuario):
    from views import Tela_admin, Tela_aluno, Tela_professor

    if tipo_usuario == 'admin':
        Tela_admin()
    elif tipo_usuario == 'aluno':
        Tela_aluno()
    elif tipo_usuario == 'professor':
        Tela_professor()

def formatar_para_banco(dateentry_data):
    from datetime import datetime
    # Converte a data do formato do DateEntry para o formato do banco de dados
    return datetime.strptime(dateentry_data, "%d/%m/%Y").strftime("%Y-%m-%d")

def obter_valores_cadastro_aluno(self):
    username = self.txtUsername.get()
    nome = self.txtNome.get()
    telefone = self.txtTelefone.get()
    email = self.txtEmail.get()
    cpf = self.txtCPF.get()
    password = cpf
    data_nascimento = self.txtData_nasc.get()
    sexo = self.txtSexo.get()
    curso_id = self.txtCursos.get()
    curso_id = curso_id.split()
    curso_id = int(curso_id[0])

    # Criar registro de aluno
    aluno = criar_registro_aluno(username, password, email, nome, cpf, telefone, data_nascimento, sexo, curso_id)

    # Verificar se o aluno foi criado com sucesso
    if aluno is not None:
        # Tentar matricular o aluno em uma turma
        aluno_matriculado = matricular_aluno_na_turma(aluno.id, curso_id)
        if aluno_matriculado:
            self.aviso_label.config(text="Aluno registrado e matriculado com sucesso", foreground='green')
        else:
            self.aviso_label.config(text="Erro: Não há turmas disponíveis ou aluno já matriculado", foreground='red')
    else:
        self.aviso_label.config(text="Erro: Não há turmas disponíveis para matrícula", foreground='red')

def obter_valores_cadastro_professor(self):
    from peewee import IdentityField
    username = self.txtUsername.get()
    nome = self.txtNome.get()
    telefone = self.txtTelefone.get()
    email = self.txtEmail.get()
    cpf = self.txtCPF.get()
    password = cpf
    data_nascimento = self.txtData_nasc.get()
    sexo = self.txtSexo.get()

    try:
        # Adicione um Label para exibir mensagens de aviso
        criar_registro_professor(username,password, email, nome, cpf, telefone, data_nascimento, sexo)
        self.aviso_label.config(text="Registro criado com sucesso", foreground='green')
    except IntegrityError:
        self.aviso_label.config(text="Erro: Usuário ou e-mail já existente", foreground='red')

def obter_valores_cadastro_curso(self):
    nome = self.txtNome.get()
    coordenador = self.txtCoordenador.get()
    coordenador = coordenador.split()
    coordenador = int(coordenador[0]) 
    descricao = self.txtDescricao.get()
    carga_horaria = self.txtCarga_horaria.get()
    data_inicio = self.txtData_inicio.get()
    criar_registro_curso(nome, coordenador, descricao, int(carga_horaria), formatar_para_banco(data_inicio))

def obter_valores_cadastro_turma(self):
    sala = self.txtSala.get()
    curso = self.txtCurso.get()
    curso = curso.split()
    curso = int(curso[0])
    max_alunos = self.txtMax_alunos.get()
    horario = self.txtHorario.get()
    coordenador_id = self.txtCoordenador.get()  # Assumindo que você tem o ID do coordenador
    coordenador_id = coordenador_id.split()
    coordenador_id = int(coordenador_id[0])

    # Criar registro de turma
    turma_criada = criar_registro_turma(sala, curso, max_alunos, horario, coordenador_id)

    # Verificar se a turma foi criada com sucesso
    if turma_criada:
        # Tentar matricular o coordenador na turma
        self.aviso_label.config(text="Turma registrada com sucesso", foreground='green')
    else:
        self.aviso_label.config(text="Erro: Não foi possível criar a turma", foreground='red')

def listar_turmas_faz_parte(usuario):
    turmas = AlunoTurma.select(AlunoTurma.turma_id).where(AlunoTurma.aluno_id == usuario.id)
    turmas_list = []

    for turma in turmas:
        turma_obj = Turma.get_or_none(Turma.id == turma.turma_id)
        if turma_obj:
            turmas_list.append(turma_obj)

    return turmas_list

def obter_mudancas_perfil_aluno(self, usuario):
    username = self.txtUsername_user.get()
    password = self.txtPassword_user.get()
    email = self.txtEmail_user.get()
    telefone = self.txtTelefone_user.get()
    
    update_aluno(username, password, email, telefone, usuario)

def pegar_turma_selecionada(self):
    turma = self.txtTurmas.get()
    turma = turma.split()
    turma = int(turma[0])
    
    turma_seleciona = pegar_turma_selecionada(turma)
    
    return turma_seleciona

