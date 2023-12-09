from tkinter import *
from tkinter import ttk
from controllers import (center, login, telas_controle, listar, obter_valores_cadastro_aluno, obter_valores_cadastro_professor, 
                         obter_valores_cadastro_curso, obter_valores_cadastro_turma, listar_turmas_faz_parte, usuario, obter_mudancas_perfil_aluno,
                         pegar_turma_selecionada)
from db_utils import (listar_cursos, att_aluno_user, buscar_turma, listar_professores, listar_turma, buscar_turma_selecionada, buscar_curso_sobre,
                      buscar_alunos_sobre, delete_aluno, delete_professor, matricular_aluno_na_turma, matricular_coordenador_na_turma, buscar_curso_nome)
from tkcalendar import DateEntry

class Aplicacao():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()

    def tela(self):
        self.root.title("Sigaa 0.2")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('400x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)

    def widgets_frame1(self):

        # Label e Entry Usuario
        self.lblUsuario = ttk.Label(self.frame1, text='Usuário:', font=('verdana', 11, 'bold'))
        self.lblUsuario.place(relx=0.03, rely=0.12)

        self.txtUsuario = ttk.Entry(self.frame1)
        self.txtUsuario.place(relx=0.25, rely=0.1, relwidth=0.7)


        # Label e Entry Senha
        self.lblSenha = ttk.Label(self.frame1, text='Senha:', font=('verdana', 11, 'bold'))
        self.lblSenha.place(relx=0.03, rely=0.32)

        self.txtSenha = ttk.Entry(self.frame1, show="•")
        self.txtSenha.place(relx=0.25, rely=0.3, relwidth=0.7)

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.7, anchor="center")

        # Botão Login
        self.btnLogin = ttk.Button(self.frame1, text='Login', command=self.realizar_login)
        self.btnLogin.place(relx=0.4, rely=0.5)
    
    def realizar_login(self):
        global usuario
        # Obtenha os valores dos widgets txtUsuario e txtSenha
        username = self.txtUsuario.get()
        password = self.txtSenha.get()
        
        usuario, tipo_usuario = login(username, password)

        if usuario and tipo_usuario:
            self.root.destroy() 
            telas_controle(tipo_usuario)
        else:
            self.aviso_label.config(text="Falha na autenticação", foreground='red')

class Lista_de_alunos():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.scrol()  # Chame o método para criar a barra de rolagem
        self.lista()
        self.listar_alunos()
        self.root.mainloop()

    def tela(self):
        self.root.title("Lista de Alunos")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('1000x500')
        self.root.resizable(False, False)
        center(self.root)

    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.root)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.root, columns=('email', 'matricula', 'nome', 'cpf', 'telefone'), show='headings', selectmode="extended",
                                     yscrollcommand=self.listaScroll.set)
        self.listaCli.pack(expand=True, fill="both")
        

        self.listaCli.heading('email', text='Email')
        self.listaCli.heading('matricula', text='Matricula')
        self.listaCli.heading('nome', text='Nome')
        self.listaCli.heading('cpf', text='CPF')
        self.listaCli.heading('telefone', text='Telefone')
        
        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)
        
        # Chame o método para preencher a lista
        self.listar_alunos()

    def listar_alunos(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar do controlador
        alunos = listar('aluno')

        # Preencha a lista com os resultados da consulta
        for aluno in alunos:
            self.listaCli.insert('', END, values=(aluno.email, aluno.matricula, aluno.nome, aluno.cpf, aluno.telefone))

class Lista_de_professores():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.scrol()
        self.lista()
        self.listar_professores()
        self.root.mainloop()

    def tela(self):
        self.root.title("Lista de Professores")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('1000x500')
        self.root.resizable(False, False)
        center(self.root)
    
    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.root)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.root, columns=('email', 'matricula', 'nome', 'cpf', 'telefone'), show='headings', selectmode="extended",
                                     yscrollcommand=self.listaScroll.set)
        self.listaCli.pack(expand=True, fill="both")
        

        self.listaCli.heading('email', text='Email')
        self.listaCli.heading('matricula', text='Matricula')
        self.listaCli.heading('nome', text='Nome')
        self.listaCli.heading('cpf', text='CPF')
        self.listaCli.heading('telefone', text='Telefone')
        
        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)
        
    def listar_professores(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_professores do controlador
        professores = listar('professor')

        # Preencha a lista com os resultados da consulta
        for professor in professores:
            self.listaCli.insert('', END, values=(professor.email, professor.matricula, professor.nome, professor.cpf, professor.telefone))

class Lista_de_cursos():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.scrol()
        self.lista()
        self.listar_cursos()
        self.root.mainloop()

    def tela(self):
        self.root.title("Lista de Cursos")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('1000x500')
        self.root.resizable(False, False)
        center(self.root)
    
    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.root)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.root, columns=('nome', 'coordenador', 'descricao', 'carga_horaria', 'data_inicio'), show='headings', selectmode="extended",
                                     yscrollcommand=self.listaScroll.set)
        self.listaCli.pack(expand=True, fill="both")
        
        self.listaCli.heading('nome', text='Nome')
        self.listaCli.heading('coordenador', text='Coordenador')
        self.listaCli.heading('descricao', text='Descrição')
        self.listaCli.heading('carga_horaria', text='Carga Horária')
        self.listaCli.heading('data_inicio', text='Data de Início')
        
        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)
        
    def listar_cursos(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_cursos do controlador
        cursos = listar('curso')

        # Preencha a lista com os resultados da consulta
        for curso in cursos:
            self.listaCli.insert('', END, values=(curso.nome, curso.coordenador.nome, curso.descricao, curso.carga_horaria, curso.data_inicio))

class Lista_de_turmas():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.scrol()
        self.lista()
        self.listar_turmas()
        self.root.mainloop()

    def tela(self):
        self.root.title("Lista de Turmas")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('1000x500')
        self.root.resizable(False, False)
        center(self.root)
    
    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.root)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.root, columns=('sala', 'curso', 'max_alunos', 'horario'), show='headings', selectmode="extended",
                                     yscrollcommand=self.listaScroll.set)
        self.listaCli.pack(expand=True, fill="both")
        
        self.listaCli.heading('sala', text='Sala')
        self.listaCli.heading('curso', text='Curso')
        self.listaCli.heading('max_alunos', text='Máximo de Alunos')
        self.listaCli.heading('horario', text='Horário')
        
        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)
        
    def listar_turmas(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_turmas do controlador
        turmas = listar('turma')

        # Preencha a lista com os resultados da consulta
        for turma in turmas:
            self.listaCli.insert('', END, values=(turma.sala, turma.curso.nome, turma.max_alunos, turma.horario))

class Cadatrar_aluno():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Cadastar Aluno")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)
    
    def widgets_frame1(self):
        # Label e Entry Username
        self.lblUsername = ttk.Label(self.frame1, text='Username:', font=('verdana', 11, 'bold'))
        self.lblUsername.place(relx=0.03, rely=0.01)

        self.txtUsername = ttk.Entry(self.frame1)
        self.txtUsername.place(relx=0.25, rely=0, relwidth=0.7)

        # Label e Entry Nome
        self.lblNome = ttk.Label(self.frame1, text='Nome:', font=('verdana', 11, 'bold'))
        self.lblNome.place(relx=0.03, rely=0.11)

        self.txtNome = ttk.Entry(self.frame1)
        self.txtNome.place(relx=0.25, rely=0.1, relwidth=0.7)

        # Label e Entry Telefone
        self.lblTelefone = ttk.Label(self.frame1, text='Telefone:', font=('verdana', 11, 'bold'))
        self.lblTelefone.place(relx=0.03, rely=0.21)

        self.txtTelefone = ttk.Entry(self.frame1)
        self.txtTelefone.place(relx=0.25, rely=0.2, relwidth=0.7)

        # Label e Entry Email
        self.lblEmail = ttk.Label(self.frame1, text='Email:', font=('verdana', 11, 'bold'))
        self.lblEmail.place(relx=0.03, rely=0.31)

        self.txtEmail = ttk.Entry(self.frame1)
        self.txtEmail.place(relx=0.25, rely=0.3, relwidth=0.7)

        # Label e Entry CPF
        self.lblCPF = ttk.Label(self.frame1, text='CPF:', font=('verdana', 11, 'bold'))
        self.lblCPF.place(relx=0.03, rely=0.41)

        self.txtCPF = ttk.Entry(self.frame1)
        self.txtCPF.place(relx=0.25, rely=0.4, relwidth=0.7)

        # Label e Entry Data_nasc
        self.lblData_nasc = ttk.Label(self.frame1, text='Data Nascimento:', font=('verdana', 11, 'bold'))
        self.lblData_nasc.place(relx=0.03, rely=0.51)

        self.txtData_nasc = DateEntry(self.frame1, date_pattern="dd/mm/yyyy")
        self.txtData_nasc.place(relx=0.37, rely=0.5, relwidth=0.57)

        # Label e Cobobox Sexo
        sexo = ['M','F']
        self.lblSexo = ttk.Label(self.frame1, text='Sexo:', font=('verdana', 11, 'bold'))
        self.lblSexo.place(relx=0.03, rely=0.61)

        self.txtSexo = ttk.Combobox(self.frame1, values=sexo, state="readonly")
        self.txtSexo.place(relx=0.25, rely=0.6, relwidth=0.7)
        self.txtSexo.current(0)

        # Turma
        cursos = listar_cursos()
        self.lblCursos = ttk.Label(self.frame1, text='Cursos:', font=('verdana', 11, 'bold'))
        self.lblCursos.place(relx=0.03, rely=0.71)

        self.txtCursos = ttk.Combobox(self.frame1, values=cursos, state='readonly')
        self.txtCursos.place(relx=0.25, rely=0.7, relwidth=0.7)


        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

        # Botão Criar
        self.btnCriar = ttk.Button(self.frame1, text='Criar', command=self.criar_registro)
        self.btnCriar.place(relx=0.4, rely=0.8)

    def criar_registro(self):
        valores = obter_valores_cadastro_aluno(self)
        # Faça algo com os valores, como criar um registro no banco de dados
        # ou exibir os valores em algum lugar

class Cadastrar_professor():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()

    def tela(self):
        self.root.title("Cadastrar Professor")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)

    def widgets_frame1(self):
        # Label e Entry Username
        self.lblUsername = ttk.Label(self.frame1, text='Username:', font=('verdana', 11, 'bold'))
        self.lblUsername.place(relx=0.03, rely=0.01)

        self.txtUsername = ttk.Entry(self.frame1)
        self.txtUsername.place(relx=0.25, rely=0, relwidth=0.7)

        # Label e Entry Nome
        self.lblNome = ttk.Label(self.frame1, text='Nome:', font=('verdana', 11, 'bold'))
        self.lblNome.place(relx=0.03, rely=0.11)

        self.txtNome = ttk.Entry(self.frame1)
        self.txtNome.place(relx=0.25, rely=0.1, relwidth=0.7)

        # Label e Entry Telefone
        self.lblTelefone = ttk.Label(self.frame1, text='Telefone:', font=('verdana', 11, 'bold'))
        self.lblTelefone.place(relx=0.03, rely=0.21)

        self.txtTelefone = ttk.Entry(self.frame1)
        self.txtTelefone.place(relx=0.25, rely=0.2, relwidth=0.7)

        # Label e Entry Email
        self.lblEmail = ttk.Label(self.frame1, text='Email:', font=('verdana', 11, 'bold'))
        self.lblEmail.place(relx=0.03, rely=0.31)

        self.txtEmail = ttk.Entry(self.frame1)
        self.txtEmail.place(relx=0.25, rely=0.3, relwidth=0.7)

        # Label e Entry CPF
        self.lblCPF = ttk.Label(self.frame1, text='CPF:', font=('verdana', 11, 'bold'))
        self.lblCPF.place(relx=0.03, rely=0.41)

        self.txtCPF = ttk.Entry(self.frame1)
        self.txtCPF.place(relx=0.25, rely=0.4, relwidth=0.7)

        # Label e Entry Data_nasc
        self.lblData_nasc = ttk.Label(self.frame1, text='Data Nascimento:', font=('verdana', 11, 'bold'))
        self.lblData_nasc.place(relx=0.03, rely=0.51)

        self.txtData_nasc = DateEntry(self.frame1, date_pattern="dd/mm/yyyy")
        self.txtData_nasc.place(relx=0.37, rely=0.5, relwidth=0.57)

        # Label e Cobobox Sexo
        sexo = ['M','F']
        self.lblSexo = ttk.Label(self.frame1, text='Sexo:', font=('verdana', 11, 'bold'))
        self.lblSexo.place(relx=0.03, rely=0.61)

        self.txtSexo = ttk.Combobox(self.frame1, values=sexo, state="readonly")
        self.txtSexo.place(relx=0.25, rely=0.6, relwidth=0.7)
        self.txtSexo.current(0)

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

        # Botão Criar
        self.btnCriar = ttk.Button(self.frame1, text='Criar', command=self.criar_registro)
        self.btnCriar.place(relx=0.4, rely=0.75)

    def criar_registro(self):
        # Obtenha os valores do formulário
        valores = obter_valores_cadastro_professor(self)

class Cadastar_curso():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()

    def tela(self):
        self.root.title("Cadastrar Curso")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)

    def widgets_frame1(self):
        # Entry e Label do nome do curso
        self.lblNome = ttk.Label(self.frame1, text='Nome:', font=('verdana', 11, 'bold'))
        self.lblNome.place(relx=0.03, rely=0.01)

        self.txtNome = ttk.Entry(self.frame1)
        self.txtNome.place(relx=0.3, rely=0, relwidth=0.65)

        # Combobox e Label dos cordenadores
        self.lblCoordenador = ttk.Label(self.frame1, text='Coordenador:', font=('verdana', 11, 'bold'))
        self.lblCoordenador.place(relx=0.03, rely=0.11)
        Coordenador = listar_professores()
        self.txtCoordenador = ttk.Combobox(self.frame1, values= Coordenador, state="readonly" )
        self.txtCoordenador.place(relx=0.3, rely=0.1, relwidth=0.65)
        self.txtCoordenador.current(0)

        # Entry e Label do Descrição do curso
        self.lblDescricao = ttk.Label(self.frame1, text='Descrição:', font=('verdana', 11, 'bold'))
        self.lblDescricao.place(relx=0.03, rely=0.21)

        self.txtDescricao = ttk.Entry(self.frame1)
        self.txtDescricao.place(relx=0.3, rely=0.2, relwidth=0.65)  

        # Entry e Label do Carga horaria do curso
        self.lblCarga_horaria = ttk.Label(self.frame1, text='Carga horaria:', font=('verdana', 11, 'bold'))
        self.lblCarga_horaria.place(relx=0.03, rely=0.31)

        self.txtCarga_horaria = ttk.Entry(self.frame1)
        self.txtCarga_horaria.place(relx=0.3, rely=0.3, relwidth=0.65)

        # Entry e Label Data de inicio
        self.lblData_inicio = ttk.Label(self.frame1, text='Carga horaria:', font=('verdana', 11, 'bold'))
        self.lblData_inicio.place(relx=0.03, rely=0.41)

        # botão para a criação
        self.txtData_inicio = DateEntry(self.frame1, date_pattern="dd/mm/yyyy")
        self.txtData_inicio.place(relx=0.35, rely=0.4, relwidth=0.57)

        self.btnCriar = ttk.Button(self.frame1, text='Criar', command=self.criar_registro)
        self.btnCriar.place(relx=0.4, rely=0.65)

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def criar_registro(self):
        # Obtenha os valores do formulário
        valores = obter_valores_cadastro_curso(self)

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label.config(text="Registro criado com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Cadastar_turma():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()

    def tela(self):
        self.root.title("Cadastrar Turma")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.1, relheight=0.9, relwidth=0.9)

    def widgets_frame1(self):
        # Entry e Label do Sala do curso
        self.lblSala = ttk.Label(self.frame1, text='Sala:', font=('verdana', 11, 'bold'))
        self.lblSala.place(relx=0.03, rely=0.01)

        self.txtSala = ttk.Entry(self.frame1)
        self.txtSala.place(relx=0.3, rely=0, relwidth=0.65)

        # Combobox e Label dos Cursos
        self.lblCurso = ttk.Label(self.frame1, text='Curso:', font=('verdana', 11, 'bold'))
        self.lblCurso.place(relx=0.03, rely=0.11)
        curso = listar_cursos()
        self.txtCurso = ttk.Combobox(self.frame1, values= curso, state="readonly" )
        self.txtCurso.place(relx=0.3, rely=0.1, relwidth=0.65)
        self.txtCurso.current(0)

        # Entry e Label do Max alunos do curso
        self.lblMax_alunos = ttk.Label(self.frame1, text='Max alunos:', font=('verdana', 11, 'bold'))
        self.lblMax_alunos.place(relx=0.03, rely=0.21)

        self.txtMax_alunos = ttk.Entry(self.frame1)
        self.txtMax_alunos.place(relx=0.3, rely=0.2, relwidth=0.65)  

        # Entry e Label do Horario do curso
        self.lblHorario = ttk.Label(self.frame1, text='Horario:', font=('verdana', 11, 'bold'))
        self.lblHorario.place(relx=0.03, rely=0.31)

        self.txtHorario = ttk.Entry(self.frame1)
        self.txtHorario.place(relx=0.3, rely=0.3, relwidth=0.65)

        self.lblCoordenador = ttk.Label(self.frame1, text='Coordenador:', font=('verdana', 11, 'bold'))
        self.lblCoordenador.place(relx=0.03, rely=0.41)
        Coordenador = listar_professores()
        self.txtCoordenador = ttk.Combobox(self.frame1, values= Coordenador, state="readonly" )
        self.txtCoordenador.place(relx=0.3, rely=0.4, relwidth=0.65)
        self.txtCoordenador.current(0)

        # botão para a criação
        self.btnCriar = ttk.Button(self.frame1, text='Criar', command=self.criar_registro)
        self.btnCriar.place(relx=0.4, rely=0.65)

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def criar_registro(self):
        # Obtenha os valores do formulário
        obter_valores_cadastro_turma(self)

        # Se não houver conflito, exiba a mensagem de sucesso
        self.aviso_label.config(text="Registro criado com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Editar_perfil():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Editar perfil")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)

    def widgets_frame1(self):
        #mostar o username para o aluno
        self.lblUsername = ttk.Label(self.frame1, text='Username:', font=('verdana', 11, 'bold'))
        self.lblUsername.place(relx=0, rely=0.01)

        self.txtUsername_user = ttk.Entry(self.frame1)
        self.txtUsername_user.place(relx=0.35, rely=0, relwidth=0.65)
        self.txtUsername_user.insert(0,usuario.username)

        #mostar o password para o aluno
        self.lblPassword = ttk.Label(self.frame1, text='Password:', font=('verdana', 11, 'bold'))
        self.lblPassword.place(relx=0, rely=0.21)

        self.txtPassword_user = ttk.Entry(self.frame1)
        self.txtPassword_user.place(relx=0.35, rely=0.2, relwidth=0.65) 
        self.txtPassword_user.insert(0,usuario.password)
        
        #mostra o email para o aluno
        self.lblEmail = ttk.Label(self.frame1, text='Email:', font=('verdana', 11, 'bold'))
        self.lblEmail.place(relx=0, rely=0.41) 

        self.txtEmail_user = ttk.Entry(self.frame1)
        self.txtEmail_user.place(relx=0.35, rely=0.4, relwidth=0.65) 
        self.txtEmail_user.insert(0,usuario.email)

        #mostra o telefone para o aluno
        self.lblTelefone = ttk.Label(self.frame1, text='Telefone:', font=('verdana', 11, 'bold'))
        self.lblTelefone.place(relx=0,rely=0.61)

        self.txtTelefone_user = ttk.Entry(self.frame1)
        self.txtTelefone_user.place(relx=0.35,rely=0.6, relwidth=0.65)
        self.txtTelefone_user.insert(0,usuario.telefone)

        self.btnConfirmacao = ttk.Button(self.frame1, text='Confrirmar mudanças', command=self.confirmacao)
        self.btnConfirmacao.place(relx=0.35, rely=0.8)


    def confirmacao(self):

        global usuario
        usuario = att_aluno_user(usuario)
        obter_mudancas_perfil_aluno(self, usuario)
        
        usuario = att_aluno_user(usuario)

        # Feche a janela de Edição
        self.root.destroy()

        # Abra a janela de Perfil
        Perfil()

class Perfil():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Perfil")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)
    
    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets_frame1(self):
        #mostar o username para o aluno
        self.lblUsername = ttk.Label(self.frame1, text='Username:', font=('verdana', 11, 'bold'))
        self.lblUsername.place(relx=0, rely=0)

        self.lblUsername_user = ttk.Label(self.frame1, text=f'{usuario.username}', font=('verdana', 11, 'bold'))
        self.lblUsername_user.place(relx=0.35, rely=0)

        #mostar o password para o aluno
        self.lblPassword = ttk.Label(self.frame1, text='Password:', font=('verdana', 11, 'bold'))
        self.lblPassword.place(relx=0, rely=0.1)

        self.lblPassword_user = ttk.Label(self.frame1, text=f'{usuario.password}', font=('verdana', 11, 'bold'))
        self.lblPassword_user.place(relx=0.35, rely=0.1) 
        
        #mostra o email para o aluno
        self.lblEmail = ttk.Label(self.frame1, text='Email:', font=('verdana', 11, 'bold'))
        self.lblEmail.place(relx=0, rely=0.2) 

        self.lblEmail_user = ttk.Label(self.frame1, text=f'{usuario.email}', font=('verdana', 11, 'bold'))
        self.lblEmail_user.place(relx=0.35, rely=0.2) 

        #mostra a matricula para o aluno
        self.lblMatricula = ttk.Label(self.frame1, text='Matricula:', font=('verdana', 11, 'bold'))
        self.lblMatricula.place(relx=0, rely=0.3)

        self.lblMatricula_user = ttk.Label(self.frame1, text=f'{usuario.matricula}', font=('verdana', 11, 'bold'))
        self.lblMatricula_user.place(relx=0.35, rely=0.3)

        #mostra o nome para o aluno
        self.lblNome = ttk.Label(self.frame1, text='Nome:', font=('verdana', 11, 'bold'))
        self.lblNome.place(relx=0, rely=0.4)

        self.lblNome_user = ttk.Label(self.frame1, text=f'{usuario.nome}', font=('verdana', 11, 'bold'))
        self.lblNome_user.place(relx=0.35,rely=0.4)

        #mostra o cpf para o aluno
        self.lblCPF = ttk.Label(self.frame1, text='CPF:', font=('verdana', 11, 'bold'))
        self.lblCPF.place(relx=0, rely=0.5)

        self.lblCPF_user = ttk.Label(self.frame1, text=f'{usuario.cpf}', font=('verdana', 11, 'bold'))
        self.lblCPF_user.place(relx=0.35,rely=0.5)

        #mostra o telefone para o aluno
        self.lblTelefone = ttk.Label(self.frame1, text='Telefone:', font=('verdana', 11, 'bold'))
        self.lblTelefone.place(relx=0,rely=0.6)

        self.lblTelefone_user = ttk.Label(self.frame1, text=f'{usuario.telefone}', font=('verdana', 11, 'bold'))
        self.lblTelefone_user.place(relx=0.35,rely=0.6)

        #mostra a data de nascimneto para o aluno
        self.lblData_nascimento = ttk.Label(self.frame1, text='Data Nascimento:', font=('verdana', 11, 'bold'))
        self.lblData_nascimento.place(relx=0,rely=0.7)

        self.lblData_nascimento_user = ttk.Label(self.frame1, text=f'{usuario.data_nascimento}', font=('verdana', 11, 'bold'))
        self.lblData_nascimento_user.place(relx=0.35,rely=0.7)

        #mostra o sexo para o aluno
        self.lblSexo = ttk.Label(self.frame1, text='Sexo:', font=('verdana', 11, 'bold'))
        self.lblSexo.place(relx=0,rely=0.8)

        self.lblSexo_user = ttk.Label(self.frame1, text=f'{usuario.sexo}', font=('verdana', 11, 'bold'))
        self.lblSexo_user.place(relx=0.35, rely=0.8)

        self.btnEditar = ttk.Button(self.frame1, text='Editar', command=self.abrir_tela_edicao)
        self.btnEditar.place(relx=0.4, rely=0.9)

    def abrir_tela_edicao(self):
        # Crie uma instância da classe Editar_aluno, passando uma referência para a instância atual
        # Feche a janela de Perfil
        self.root.destroy()
        Editar_perfil()

class Sobre_turma():
    def __init__(self, turma=[]):
        self.turma = turma
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.scrol()
        self.lista()
        self.root.mainloop()

    def tela(self):
        self.root.title("Sobre a turma")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.3, relwidth=0.9)
        
        self.frame2 = Frame(self.root, bg = 'white')
        self.frame2.place(relx=0.05, rely=0.35, relheight=0.6, relwidth=0.9)

    def widgets_frame1(self):
        # Obtenha a lista de turmas
        turmas = listar_turma(usuario)

        # Crie um Combobox e defina as opções como as turmas obtidas
        self.txtTurmas = ttk.Combobox(self.frame1, values=turmas)
        self.txtTurmas.place(relx=0.05, rely=0)

        self.btnAtualizar = ttk.Button(self.frame1, text='Atualizar', command=self.pegar_turma)
        self.btnAtualizar.place(relx=0.7, rely=0)

        # Adicione uma StringVar para armazenar a descrição do curso
        self.descricao_var = StringVar()

        # Inicialize o Label com a descrição do curso da turma
        self.txtDescricao = ttk.Label(self.frame1, text='')
        self.txtDescricao.place(relx=0, rely=0.3)

    def pegar_turma(self):
        # Obtém o ID da turma selecionada
        turma_id = self.txtTurmas.get()
        turma_id = turma_id.split()
        turma_id = int(turma_id[0])

        self.turma_id, self.turma_curso_id = buscar_turma_selecionada(turma_id)

        # Atualiza a descrição do curso com base na turma selecionada
        if self.turma_id:
            desc_curso = buscar_curso_sobre(self.turma_curso_id)
            self.txtDescricao.config(text=f'{desc_curso}')
        
        self.listar_alunos()
    
    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.root)
        self.listaScroll.pack(side="right", fill="y")
    
    def lista(self):
        self.listaCli = ttk.Treeview(self.frame2, columns=('matricula', 'nome'), show='headings', selectmode="extended",
                                     yscrollcommand=self.listaScroll.set)
        self.listaCli.pack(expand=True, fill="both")
        
        self.listaCli.heading('matricula', text='Matricula')
        self.listaCli.heading('nome', text='Nome')
        
        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)
        
    def listar_alunos(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_alunos_da_turma do controlador
        alunos = buscar_alunos_sobre(self.turma_id)

        # Preencha a lista com os resultados da consulta
        for aluno in alunos:
            self.listaCli.insert('', END, values=(aluno[0], aluno[1]))

class Mais():
    def __init__(self,):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def tela(self):
        self.root.title("Vincular alunos e professores a turmas")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets(self):
        self.btnCadastrar_aluno = ttk.Button(self.frame1, text='Vincular aluno a turma', command=Vincular_aluno)
        self.btnCadastrar_aluno.place(relx=0.7,rely=0.3,anchor="center")
        
        self.btnCadastrar_professor = ttk.Button(self.frame1, text='Vincular professor a turma', command=Vincular_professor)
        self.btnCadastrar_professor.place(relx=0.7,rely=0.6,anchor="center")
        
        self.btnDeletar_aluno = ttk.Button(self.frame1, text='Deletar aluno', command=Deletar_aluno)
        self.btnDeletar_aluno.place(relx=0.2,rely=0.3,anchor="center")
        
        self.btnDeletar_professor = ttk.Button(self.frame1, text='Deletar professor', command=Deletar_professor)
        self.btnDeletar_professor.place(relx=0.2,rely=0.6,anchor="center")

class Vincular_aluno():
    def __init__(self,):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def tela(self):
        self.root.title("Vincular aluno")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets(self):
        
        alunos = [f'{aluno.id} {aluno.nome}' for aluno in listar('aluno')]
        cursos = listar_cursos()

        self.txtAlunoSelecionado = ttk.Combobox(self.frame1, values=alunos, state='readonly')
        self.txtAlunoSelecionado.place(relx=0.3, rely=0.1)

        self.txtCursoSelecionado = ttk.Combobox(self.frame1, values=cursos, state='readonly')
        self.txtCursoSelecionado.place(relx=0.3, rely=0.3)

        self.btnVincular_aluno = ttk.Button(self.frame1, text='Vincular aluno a turma selecionado', command= lambda: self.vincular())
        self.btnVincular_aluno.place(relx=0.5,rely=0.7,anchor="center")

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def vincular(self):
        
        aluno_id = self.txtAlunoSelecionado.get().split()[0]
        curso_id = self.txtCursoSelecionado.get().split()[0]

        matricular_aluno_na_turma(aluno_id, curso_id)

        # Se não houver conflito, exiba a mensagem de sucesso
        self.aviso_label.config(text="Aluno vinculado a turma com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Vincular_professor():
    def __init__(self,):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def tela(self):
        self.root.title("Vincular professor")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets(self):
        
        professores = [f'{aluno.id} {aluno.nome}' for aluno in listar('professor')]
        turmas = [(turma.id, turma.sala, turma.curso_id) for turma in listar('turma')]
        turmas_exibir = [f'{turma[1]} - {buscar_curso_nome(turma[2])}' for turma in turmas]

        self.txtProfessorSelecionado = ttk.Combobox(self.frame1, values=professores, state='readonly')
        self.txtProfessorSelecionado.place(relx=0.3, rely=0.1)

        self.txtTurmaSelecionado = ttk.Combobox(self.frame1, values=turmas_exibir, state='readonly')
        self.txtTurmaSelecionado.place(relx=0.3, rely=0.3)

        self.btnVincular_professor = ttk.Button(self.frame1, text='Vincular aluno a turma selecionado', command= lambda: self.vincular())
        self.btnVincular_professor.place(relx=0.5,rely=0.7,anchor="center")

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def vincular(self):

        turma_select = self.txtTurmaSelecionado.get().split(' -')
        for turma in listar('turma'):
            if turma.sala == turma_select[0].strip() and buscar_curso_nome(turma.curso_id) == turma_select[1].strip():
                turma_id = turma.id
                break

        professor_id = self.txtProfessorSelecionado.get().split()[0]

        matricular_coordenador_na_turma(professor_id, turma_id)

        # Se não houver conflito, exiba a mensagem de sucesso
        self.aviso_label.config(text="Professor vinculado a turma com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Deletar_aluno():
    def __init__(self,):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def tela(self):
        self.root.title("Deletar aluno")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets(self):
        
        alunos = [f'{aluno.id} {aluno.nome}' for aluno in listar('aluno')]

        self.txtAlunoSelecionado = ttk.Combobox(self.frame1, values=alunos, state='readonly')
        self.txtAlunoSelecionado.place(relx=0.3, rely=0.1)

        self.btnDeletar_aluno = ttk.Button(self.frame1, text='Excluir aluno selecionado', command= lambda: self.del_aluno())
        self.btnDeletar_aluno.place(relx=0.5,rely=0.5,anchor="center")

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def del_aluno(self):
        delete_aluno(self.txtAlunoSelecionado.get())

        # Se não houver conflito, exiba a mensagem de sucesso
        self.aviso_label.config(text="Aluno apagado com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Deletar_professor():
    def __init__(self,):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets()
        self.root.mainloop()

    def tela(self):
        self.root.title("Deletar professor")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
    
    def widgets(self):
        
        professores = [f'{professor.id} {professor.nome}' for professor in listar('professor')]

        self.txtProfessorSelecionado = ttk.Combobox(self.frame1, values=professores, state='readonly')
        self.txtProfessorSelecionado.place(relx=0.3, rely=0.1)

        self.btnDeletar_professor = ttk.Button(self.frame1, text='Excluir professor selecionado', command= lambda: self.del_professor())
        self.btnDeletar_professor.place(relx=0.5,rely=0.5,anchor="center")

        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    def del_professor(self):
        delete_professor(self.txtProfessorSelecionado.get())

        # Se não houver conflito, exiba a mensagem de sucesso
        self.aviso_label.config(text="Professor apagado com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

class Tela_professor():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.scrol()
        self.lista()
        self.listar_turmas()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Aluno")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('700x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0, rely=0.05, relheight=0.2, relwidth=1)

        self.frame2 = Frame(self.root)
        self.frame2.place(relx=0.03, rely=0.25, relheight=0.7, relwidth=0.94)

    def widgets_frame1(self):
        self.btnPerfil = ttk.Button(self.frame1, text='Perfil', command=Perfil)
        self.btnPerfil.place(relx=0.25, rely=0.2)

        # Corrija o botão para chamar self.Sobre_a_turma em vez de print
        self.btnVizualizar_turma = ttk.Button(self.frame1, text='Sobre a Turma', command= Sobre_turma)
        self.btnVizualizar_turma.place(relx=0.55, rely=0.2)

    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.frame2)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.frame2, columns=('sala', 'curso', 'horario'), show='headings', selectmode="extended",
                                    yscrollcommand=self.listaScroll.set, height=0)

        # Adicionando uma configuração para que o widget se expanda e preencha o frame2
        self.listaCli.pack(expand=True, fill="both")

        self.listaCli.heading('sala', text='Sala')
        self.listaCli.heading('curso', text='Curso')
        self.listaCli.heading('horario', text='Horário')

        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)

        # Adicione um evento de seleção para a Treeview
        self.listaCli.bind('<ButtonRelease-1>', self.obter_turma_selecionada)

    def listar_turmas(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_turmas do controlador
        turmas = listar_turmas_faz_parte(usuario)

        # Preencha a lista com os resultados da consulta
        for turma in turmas:
            self.listaCli.insert('', END, values=(turma.sala, turma.curso.nome, turma.horario))

        # Ajuste da altura da tabela com base no número de linhas ou defina um valor mínimo
        num_linhas = len(turmas)
        self.listaCli['height'] = num_linhas if num_linhas > 0 else 1
    def obter_turma_selecionada(self, event):
        # Lógica para obter a turma selecionada
        item_selecionado = self.listaCli.selection()
        if item_selecionado:
            turma_selecionada = self.listaCli.item(item_selecionado)['values']
            # Agora você pode usar 'turma_selecionada' para obter informações da turma
            return turma_selecionada

class Tela_aluno():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.scrol()
        self.lista()
        self.listar_turmas()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Aluno")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('700x500')
        self.root.resizable(False, False)
        center(self.root)

    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0, rely=0.05, relheight=0.2, relwidth=1)

        self.frame2 = Frame(self.root)
        self.frame2.place(relx=0.03, rely=0.25, relheight=0.7, relwidth=0.94)

    def widgets_frame1(self):
        self.btnPerfil = ttk.Button(self.frame1, text='Perfil', command=Perfil)
        self.btnPerfil.place(relx=0.25, rely=0.2)

        # Corrija o botão para chamar self.Sobre_a_turma em vez de print
        self.btnVizualizar_turma = ttk.Button(self.frame1, text='Sobre a Turma', command= Sobre_turma)
        self.btnVizualizar_turma.place(relx=0.55, rely=0.2)

    def scrol(self):
        self.listaScroll = ttk.Scrollbar(self.frame2)
        self.listaScroll.pack(side="right", fill="y")

    def lista(self):
        self.listaCli = ttk.Treeview(self.frame2, columns=('sala', 'curso', 'horario'), show='headings', selectmode="extended",
                                    yscrollcommand=self.listaScroll.set, height=0)

        # Adicionando uma configuração para que o widget se expanda e preencha o frame2
        self.listaCli.pack(expand=True, fill="both")

        self.listaCli.heading('sala', text='Sala')
        self.listaCli.heading('curso', text='Curso')
        self.listaCli.heading('horario', text='Horário')

        # Configure a barra de rolagem para controlar a visualização da lista
        self.listaCli.config(yscrollcommand=self.listaScroll.set)
        self.listaScroll.config(command=self.listaCli.yview)

        # Adicione um evento de seleção para a Treeview
        self.listaCli.bind('<ButtonRelease-1>', self.obter_turma_selecionada)

    def listar_turmas(self):
        # Limpe os itens existentes na lista
        self.listaCli.delete(*self.listaCli.get_children())

        # Chame a função listar_turmas do controlador
        turmas = listar_turmas_faz_parte(usuario)

        # Preencha a lista com os resultados da consulta
        for turma in turmas:
            self.listaCli.insert('', END, values=(turma.sala, turma.curso.nome, turma.horario))

        # Ajuste da altura da tabela com base no número de linhas ou defina um valor mínimo
        num_linhas = len(turmas)
        self.listaCli['height'] = num_linhas if num_linhas > 0 else 1

    def obter_turma_selecionada(self, event):
        # Obtenha a turma selecionada
        item_selecionado = self.listaCli.selection()
        if item_selecionado:
            turma_selecionada = self.listaCli.item(item_selecionado)['values']
            # Agora você pode usar 'turma_selecionada' para obter informações da turma
            return turma_selecionada

class Tela_admin():
    def __init__(self):
        self.root = Tk()
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.widgets_frame2()
        self.root.mainloop()
    
    def tela(self):
        self.root.title("Admin")
        self.root.option_add("*tearOff", False)
        self.root.call("source", "./theme/forest-dark.tcl")
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        center(self.root)
    
    def frames(self):
        self.frame1 = Frame(self.root)
        self.frame1.place(relx=0, rely=0.05, relheight=0.2, relwidth=1)

        self.frame2 = Frame(self.root)
        self.frame2.place(relx=0, rely=0.3, relheight=1, relwidth=1)
    
    def widgets_frame1(self):

        # Button para listar os alunos cadastrados no sistema
        self.btnListar_Alunos = ttk.Button(self.frame1, text='Listar Alunos', command=Lista_de_alunos) 
        self.btnListar_Alunos.place(relx=0.03, rely=0.2)

        # Button para listar os professores cadastrados no sistema
        self.btnListar_Professores = ttk.Button(self.frame1, text='Listar Professores', command=Lista_de_professores) 
        self.btnListar_Professores.place(relx=0.25, rely=0.2)

        # Button para listar os cursos cadastrados no sistema
        self.btnListar_Cursos = ttk.Button(self.frame1, text='Listar Cursos', command=Lista_de_cursos) 
        self.btnListar_Cursos.place(relx=0.525, rely=0.2)

        # Button para listar os turmas cadastrados no sistema
        self.btnListar_Turmas = ttk.Button(self.frame1, text='Listar Turmas', command=Lista_de_turmas) 
        self.btnListar_Turmas.place(relx=0.75, rely=0.2)

    def widgets_frame2(self):
        # Button para cadastrar novos alunos no sistema
        self.btnCastrar_Aluno = ttk.Button(self.frame2,text='Castrar Aluno', command= Cadatrar_aluno)
        self.btnCastrar_Aluno.place(relx=0.15, rely=0.05, relheight=0.15, relwidth=0.3)

        # Button para cadastrar novos professoress no sistema
        self.btnCastrar_Professor = ttk.Button(self.frame2,text='Castrar Professor', command= Cadastrar_professor)
        self.btnCastrar_Professor.place(relx=0.525, rely=0.05, relheight=0.15, relwidth=0.3)

        # Button para cadastrar novos cursos no sistema
        self.btnCastrar_Curso = ttk.Button(self.frame2,text='Castrar Curso', command= Cadastar_curso)
        self.btnCastrar_Curso.place(relx=0.15, rely=0.35, relheight=0.15, relwidth=0.3)

        # Button para cadastrar novos turma no sistema
        self.btnCastrar_Turma = ttk.Button(self.frame2,text='Castrar Turma', command=Cadastar_turma)
        self.btnCastrar_Turma.place(relx=0.525, rely=0.35, relheight=0.15, relwidth=0.3)
        
        self.btnMais = ttk.Button(self.frame2,text='Mais', command= Mais)
        self.btnMais.place(relx=0.38,rely=0.55)
