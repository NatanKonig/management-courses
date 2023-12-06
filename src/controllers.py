from peewee import *
from db_utils import db
from models import Admin, Aluno, Professor, Curso, Turma, AlunoTurma, ProfessorTurma


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


def coletar_dados_login(txtUsuario, txtSenha):
    return txtUsuario.get(), txtSenha.get()


def login(username, password):
    # Tenta autenticar como Admin
    admin_user = Admin.select().where((Admin.username == username) & (Admin.password == password)).first()
    if admin_user:
        return admin_user, 'admin'

    # Tenta autenticar como Aluno
    aluno_user = Aluno.select().where((Aluno.username == username) & (Aluno.password == password)).first()
    if aluno_user:
        return aluno_user, 'aluno'

    # Tenta autenticar como Professor
    professor_user = Professor.select().where((Professor.username == username) & (Professor.password == password)).first()
    if professor_user:
        return professor_user, 'professor'

    # Se nenhum usuário foi autenticado, retorna None
    return None, None


def telas_controle(tipo_usuario):
    from views import Tela_admin 

    if tipo_usuario == 'admin':
        Tela_admin()

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

    criar_registro_aluno(username, password, email, nome, cpf, telefone, data_nascimento, sexo)


def criar_registro_aluno(username, password, email, nome, cpf, telefone, data_nascimento, sexo):
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
        sexo = sexo
    )

    # Salve o objeto no banco de dados
    aluno.save()