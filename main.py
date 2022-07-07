from operator import indexOf
import smtplib
import email.message

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

import sqlite3

banco = sqlite3.connect('barragem.db')
cursor = banco.cursor()

cursor.execute("PRAGMA foreign_keys=ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Barragem ( id INTEGER  PRIMARY KEY AUTOINCREMENT,
                                          Nome VARCHAR(60),
                                          Coordena_gps CHAR(14)
                                          )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Indicadores (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        indicador VARCHAR(30)
                                        )    
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Apresenta (  
                                            Avaliacao VARCHAR(40),
                                            Observacao VARCHAR(40),
                                            id_Barragem INTEGER,
                                            id_Indicadores INTEGER,
                                            FOREIGN KEY ( id_Barragem ) REFERENCES Barragem(id),
                                            FOREIGN KEY ( id_Indicadores ) REFERENCES Indicadores(id)
                                          )
    """)

cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    nome text, 
                                                    senha text
                                                    )
    """)

cursor.execute("INSERT INTO Barragem VALUES (NULL, 'inicio', '')")
cursor.execute("SELECT * FROM Barragem")
check_select = cursor.fetchall()
for valor in check_select:
    
    if valor[1] == 'iniciado':
        cursor.execute("DELETE FROM Barragem WHERE Nome = 'inicio'")
    
    if valor[0] == 1 and valor[1] == 'inicio':
        cursor.execute("UPDATE Barragem SET Nome = 'iniciado' WHERE id = 1")

        #inserido primeiro usuario sendo admin
        cursor.execute("INSERT INTO user VALUES ( NULL,'admin@compesa.com', 'admin')")

        # inserindo indicares
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Erupsões')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Escorregamento')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Arvores')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Rip-Rap')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Buracos')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Obstrucoes')")
        cursor.execute("INSERT INTO Indicadores VALUES (NULL, 'Rachaduras')")

        # Inserindo barragens
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Duas Unas', '54010050')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Tapacurá', '55800100')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")

        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Tapacurá', '55800100')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Tapacurá', '55800100')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Tapacurá', '55800100')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900')")



banco.commit()

indicadores = ['Erupsões', 'Escorregamento', 'Arvores', 'Rip-Rap', 'Buracos', 'Obstrucoes', 'Rachaduras']
notas = ['0', '0', '0', '0', '0', '0', '0']
barragem_selecionada = ['(SELECIONAR BARRAGEM)']

class TelaGerenciadora(ScreenManager):
    pass

class Tela1(Screen):
    pass

class Tela2(Screen):
    flag_indicador = 0

    def selecina_barragem(self):
        self.ids.barragens.text = barragem_selecionada[0]

    def altera_indicador(self, flag):
        if (flag == 1):
            #passa para a esquerda
            if(self.flag_indicador > 0):
                self.flag_indicador -= 1
                self.ids.indicador.text = indicadores[self.flag_indicador]
                if (self.flag_indicador == 0): self.flag_indicador = 0

        elif (flag == 2):
            # passa para a direira
            if(self.flag_indicador < 6):
                self.flag_indicador += 1
                print(indicadores[self.flag_indicador])
                self.ids.indicador.text = indicadores[self.flag_indicador]
                if (self.flag_indicador == 6): self.flag_indicador = 6

    flag_nota = 0
    def altera_nota(self, flag):
        if (flag == 1):
            #passa para a esquerda
            if(self.flag_nota > 0):
                self.flag_nota -= 1
                self.ids.contador.text = str(self.flag_nota)
                if (self.flag_nota == 0): self.flag_nota = 0

        elif (flag == 2):
            # passa para a direira
            if(self.flag_nota < 5):
                self.flag_nota += 1
                self.ids.contador.text = str(self.flag_nota)
                if (self.flag_nota == 5): self.flag_nota = 5

    def guarda_valor(self):
        try:
            nota = self.ids.contador.text
            anotacao = self.ids.anotacao.text

            id_barragem = 3

            id_indicador = 0
            if self.ids.indicador.text == 'Erupsões': id_indicador = 1
            if self.ids.indicador.text == 'Escorregamento': id_indicador = 2
            if self.ids.indicador.text == 'Arvores': id_indicador = 3
            if self.ids.indicador.text == 'Rip-Rap': id_indicador = 4
            if self.ids.indicador.text == 'Buracos': id_indicador = 5
            if self.ids.indicador.text == 'Obstrucoes': id_indicador = 6
            if self.ids.indicador.text == 'Rachaduras': id_indicador = 7

            print(f"INSERT INTO Apresenta VALUES ('{nota}', '{anotacao}', {id_barragem}, {id_indicador}), ")
            cursor.execute(f"INSERT INTO Apresenta VALUES ('{nota}', '{anotacao}', {id_barragem}, {id_indicador}) ")
            banco.commit()
        except:
            self.ids.barragens.text = 'ERRO: Banco de dados'

# Tela do banco de dados
class Tela3(Screen):

    barragem_selecionada

    maximo = 5
    minimo = 0
    cont = 0 
    nome1 = ''
    nome2 = ''
    nome3 = ''
    nome4 = ''
    nome5 = ''

    def carrega_selecao(self):
        try:
            cursor.execute("SELECT * FROM Barragem")
            lista_barragem = cursor.fetchall()

            for valor in lista_barragem:
                
                index = lista_barragem.index(valor)
                if index <= self.maximo and index >= self.minimo:

                    if self.cont == 0: self.cont += 1

                    elif self.cont == 1:
                        self.nome1 = valor[1]
                        self.ids.lb_1.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
                        self.cont += 1

                    elif self.cont == 2:
                        self.nome2 = valor[1]
                        self.ids.lb_2.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
                        self.cont += 1

                    elif self.cont == 3:
                        self.nome3 = valor[1]
                        self.ids.lb_3.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
                        self.cont += 1
                    
                    elif self.cont == 4:
                        self.nome4 = valor[1]
                        self.ids.lb_4.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
                        self.cont += 1

                    elif self.cont == 5:
                        self.nome5 = valor[1]
                        self.ids.lb_5.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
        except:
            print('Erro na seleção')

    def nova_pagina(self):
        self.maximo += 5
        self.minimo += 5 
        self.cont = 0

    def antiga_pagina(self):
        self.cont = 0
        if self.maximo > 5:
            self.maximo -= 5
            self.minimo -= 5 

    def btn_1(self):
        barragem_selecionada[0] = self.nome1

    def btn_2(self):
        barragem_selecionada[0] = self.nome2

    def btn_3(self):
        barragem_selecionada[0] = self.nome2

    def btn_4(self):
        barragem_selecionada[0] = self.nome2

    def btn_5(self):
        barragem_selecionada[0] = self.nome2
    
    

class ContentNavigationDrawer(BoxLayout):
    pass

class LoginCard(MDCard):
    def fechar(self):
        self.parent.remove_widget(self)

codigo = '123teste'
class SenhaCard(MDCard):

    def enviar_cod(self):
        try:
            corpo_email = f"""
            <p>Teste de envio de email</p>
            <p>numero será gerado aleatoriamente</p>
            <p>{codigo}</p>
            """

            msg = email.message.Message()
            msg['Subject'] = "Assunto"
            msg['From'] = 'freelancedesenvolvedor@gmail.com'
            msg['To'] = self.ids.enviar_cod.text
            password = 'zuiymsakzkewbixf' 
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(corpo_email )

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado')
            self.ids.result_novaSenha.text = 'Enviado'
        except:
            pass

    def confimar_cod(self):
        if ( self.ids.codigo.text == codigo):
            self.ids.result_novaSenha.text = 'Confirmado'

    def altera_senha(self):
        pass




    def fechar(self):
        self.parent.remove_widget(self)

class CadastrarCard(MDCard):

    def teste(self):
        print('teste')
    
    def fechar(self):
        self.parent.remove_widget(self)
    
    def new_user(self, email, senha, confsenha):

        # verifica no banco todos os usúarios
        cursor.execute('SELECT * FROM user')
        resultado = cursor.fetchall()
        print(f'email: {email}, senha: {senha}, confSenha: {confsenha}')

        # verifica um por um se é igual ao digitado
        for value in resultado:
            print(value[1])
            if (email == value[1]):           
                self.ids.result.text = 'Usuário já existente'
                return
            else:
                print('cadastrado!')
                self.ids.result.text = 'Cadastrado com sucesso'
                print(email)
                print(senha)

                self.slq = f"INSERT INTO user VALUES ( NULL,'{email}', '{senha}')"

                cursor.execute(self.slq)
                banco.commit()

class TelaLogin(FloatLayout):
    
    def abrir_card(self):
        self.add_widget(SenhaCard())

    def cadastrar_card(self):
        self.add_widget(CadastrarCard())


    def valida_user(self):

        # verifica no banco todos os usúarios
        cursor.execute('SELECT * FROM user')
        resultado = cursor.fetchall()

        # verifica um por um se é igual ao digitado
        for value in resultado:
            if (
                self.ids.email.text == value[1] and
                self.ids.senha.text == value[2]
            ):           
                self.add_widget(LoginCard())


class MeuAplicativo(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '500'
        self.theme_cls.accent_palette = 'Blue'
        return Builder.load_file('abr.kv')

if __name__ == "__main__":
    MeuAplicativo().run()