import smtplib
import email.message

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

import sqlite3

banco = sqlite3.connect('barragem.db')
cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS barragem (nome text, coord interger, tipo text)")
cursor.execute("CREATE TABLE IF NOT EXISTS user (nome text, senha text)")

cursor.execute("INSERT INTO barragem VALUES ('Duas Unas', 540100100, 'Rejeitos')")
cursor.execute("INSERT INTO barragem VALUES ('Tapacura', 54250130, 'Enrocamento')")

banco.commit()

userAdmin = ''#'admin@compesa.com'
pwsAdmin = ''#'admin'

class TelaGerenciadora(ScreenManager):
    pass

class Tela1(Screen):
    pass

class Tela2(Screen):
    pass    

# Tela do banco de dados
class Tela3(Screen):

    cont = 0
    flag = True
    def selectDB(self):
        cursor.execute("SELECT * FROM barragem")
        nome = cursor.fetchall()
        self.ids.nome.text = f'Nome: {nome[self.cont][0]}'
        self.ids.idade.text = f'Coor: {str(nome[self.cont][1])}'
        self.ids.email.text = f'Tipo: {nome[self.cont][2]}'
        self.cont = self.cont + 1
        print(self.cont)
        if (self.flag):
            self.flag = self.flag = False
            self.cont = 1
        else: 
            self.flag = self.flag = True
            self.cont = 0

    def fecharDB(self):
        banco.close()
        self.ids.lbl_db_stats.text = '    Banco fechado!'

class ContentNavigationDrawer(BoxLayout):
    pass

class LoginCard(MDCard):
    def fechar(self):
        self.parent.remove_widget(self)


codigo = '123teste'
class SenhaCard(MDCard):

    def enviar_cod(self):
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

    def confimar_cod(self):
        if ( self.ids.codigo.text == codigo):
            self.ids.result_novaSenha.text = 'Confirmado'

    def altera_senha(self):
        pass

        # # verifica no banco todos os usúarios
        # cursor.execute('SELECT * FROM user')
        # resultado = cursor.fetchall()

        # # verifica um por um se é igual ao digitado
        # for value in resultado:
        #     pass


    def fechar(self):
        self.parent.remove_widget(self)



class CadastrarCard(MDCard):

    sql = ''

    def teste(self):
        print('teste')
    
    def fechar(self):
        self.parent.remove_widget(self)
    
    def new_user(self, email, senha, confsenha):

        # verifica no banco todos os usúarios
        cursor.execute('SELECT * FROM user')
        resultado = cursor.fetchall()

        # verifica um por um se é igual ao digitado
        for value in resultado:

            if (email == value[1]):           
                self.ids.result.text = 'Usuário já existente'
                return
            else:
                # Válida de se é um email contendo @ e se as senha conheecidem
                if ( senha == confsenha and '@' in email):

                    print('cadastrado!')
                    self.ids.result.text = 'Cadastrado com sucesso'
                    print(email)
                    print(senha)

                    self.slq = f"INSERT INTO user VALUES ( NULL,'{email}', '{senha}')"

                    cursor.execute(self.slq)
                    banco.commit()

                else: 
                    self.ids.result.text = 'Algo está errado!'

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