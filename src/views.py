from tkinter import *
from tkinter import ttk
from controllers import center, coletar_dados_login, login, telas_controle, listar, obter_valores_cadastro_aluno
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

        username, password = coletar_dados_login(self.txtUsuario, self.txtSenha)
        usuario, tipo_usuario = login(username, password)
        
        if usuario and tipo_usuario:
            self.aviso_label.config(text="Login bem-sucedido", foreground='green')
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


        # Adicione um Label para exibir mensagens de aviso
        self.aviso_label = ttk.Label(self.frame1, text="", font=('verdana', 11, 'bold'), foreground='red')
        self.aviso_label.place(relx=0.5, rely=0.7, anchor="center")

        # Botão Criar
        self.btnCriar = ttk.Button(self.frame1, text='Criar', command=self.criar_registro)
        self.btnCriar.place(relx=0.4, rely=0.75)

    def criar_registro(self):
        valores = obter_valores_cadastro_aluno(self)
        # Faça algo com os valores, como criar um registro no banco de dados
        # ou exibir os valores em algum lugar
        self.aviso_label.config(text="Registro criado com sucesso", foreground='green')
        self.aviso_label.place(relx=0.5, rely=0.9, anchor="center")

    

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
        self.btnCastrar_Professor = ttk.Button(self.frame2,text='Castrar Professor')
        self.btnCastrar_Professor.place(relx=0.525, rely=0.05, relheight=0.15, relwidth=0.3)

        # Button para cadastrar novos cursos no sistema
        self.btnCastrar_Curso = ttk.Button(self.frame2,text='Castrar Curso')
        self.btnCastrar_Curso.place(relx=0.15, rely=0.35, relheight=0.15, relwidth=0.3)

        # Button para cadastrar novos turma no sistema
        self.btnCastrar_Turma = ttk.Button(self.frame2,text='Castrar Turma')
        self.btnCastrar_Turma.place(relx=0.525, rely=0.35, relheight=0.15, relwidth=0.3)
    

Aplicacao()