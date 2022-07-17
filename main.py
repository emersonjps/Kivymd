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

cursor.execute("PRAGMA foreign_keys=ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Barragem ( id INTEGER  PRIMARY KEY AUTOINCREMENT,
                                          Nome VARCHAR(60),
                                          Coordena_gps CHAR(14),
                                          status INTEGER
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

cursor.execute("""CREATE TABLE IF NOT EXISTS metaIndicador (
                                                    nome TEXT, 
                                                    valor TEXT,
                                                    id_Indicadores INTEGER,
                                                    id_Barragem INTEGER,
                                                    FOREIGN KEY ( id_Barragem ) REFERENCES Barragem(id),
                                                    FOREIGN KEY ( id_Indicadores ) REFERENCES Indicadores(id)
                                                    )
    """)

cursor.execute("INSERT INTO Barragem VALUES (NULL, 'inicio', '', 0)")
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
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Duas Unas', '54010050', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Tapacurá', '55800100', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Goitá', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Xingó', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Cachoeira Caldeirão', '55800100', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Santo Antonio do Jari', '55800100', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Coaracy Nunes', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Ferreira Gomes', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Balbina', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Sobradinho', '55800100', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Itaparica', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Pedra do Cavalo', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Moxotó', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Paulo Afonso IV', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Itapebi', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Paulo Afonso I', '532036900', 0)")
        cursor.execute("INSERT INTO Barragem VALUES (NULL, 'Paulo Afonso II', '532036900', 0)")

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

    def finaliza_avaliacao(self):

        cursor.execute("SELECT * FROM Barragem")
        resultado = cursor.fetchall()
        for valor in resultado:
            if valor[1] == barragem_selecionada[0]:
                cursor.execute(f"UPDATE Barragem SET status = 1 WHERE id = {valor[0]}")
                print(f"UPDATE Barragem SET status = 1 WHERE id = {valor[0]}")
                banco.commit()

                self.cursor = banco.cursor()

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

            cursor.execute("SELECT * FROM Barragem")
            resulatado = cursor.fetchall()

            id_barragem = 0

            print(barragem_selecionada)
            for valor in resulatado:
                if valor[1] == barragem_selecionada[0]:
                    id_barragem = valor[0]

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
        print('primeiro')
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
        print('segunfo')
        self.maximo += 5
        self.minimo += 5 
        self.cont = 0

    def antiga_pagina(self):
        self.cont = 0
        if self.maximo > 5:
            self.maximo -= 5
            self.minimo -= 5 

    def pesquisa_id(self):
        cursor.execute("SELECT * FROM Barragem")
        barragens = cursor.fetchall()
        for valor in barragens:
            if valor[0] == int(self.ids.text_pesquisa.text):
                self.ids.lb_1.text = f'  ID: {valor[0]} | NOME: {valor[1]}\n  COORDENADAS: {valor[2]}'
                self.ids.lb_2.text = ''
                self.ids.lb_3.text = ''
                self.ids.lb_4.text = ''
                self.ids.lb_5.text = ''
                self.nome1 = valor[1]
                self.nome2 = ''
                self.nome3 = ''
                self.nome4 = ''
                self.nome5 = ''

    def btn_1(self):
        barragem_selecionada[0] = self.nome1

    def btn_2(self):
        barragem_selecionada[0] = self.nome2

    def btn_3(self):
        barragem_selecionada[0] = self.nome3

    def btn_4(self):
        barragem_selecionada[0] = self.nome4

    def btn_5(self):
        barragem_selecionada[0] = self.nome5


class Tela4(Screen):
    maximo = 8
    minimo = 0
    cont = 0
    def exibir_avaliados(self):

        cursor.execute("""
        SELECT * 
        FROM Barragem 
        INNER JOIN Apresenta ON Apresenta.id_Barragem = Barragem.id
        WHERE status = 1
        """)
        resultado = cursor.fetchall()

        print('estou na função')
        for valor in resultado:
            print(resultado.index(valor))
            index = resultado.index(valor)

            print(valor)
            if index <= self.maximo and index >= self.minimo:

                if self.cont == 0:
                    self.ids.lb1.text = f'Nome: {valor[1]}'
                    self.ids.lb9.text = f'Anotação: {valor[5]}'
                    self.ids.lb2.text = f'Erupsões: {valor[4]}' 
                if self.cont == 1: 
                    self.ids.lb3.text = f'Escorregamento: {valor[4]}'
                if self.cont == 2:
                    self.ids.lb4.text = f'Arvores: {valor[4]}'
                if self.cont == 3: 
                    self.ids.lb5.text = f'Rip-Rap: {valor[4]}'
                if self.cont == 4:
                    self.ids.lb6.text = f'Buracos: {valor[4]}'
                if self.cont == 5: 
                    self.ids.lb7.text = f'Obstrucoes: {valor[4]}'
                if self.cont == 6:
                    self.ids.lb8.text = f'Rachaduras: {valor[4]}'                   

                self.cont += 1
                if self.cont == 7: self.cont = 0


    def nova_pagina(self):
        print('segunfo')
        self.maximo += 8
        self.minimo += 8 
        self.cont = 0

    def antiga_pagina(self):
        self.cont = 0
        if self.maximo > 5:
            self.maximo -= 8
            self.minimo -= 8 

subIndece = ['', '', '', 0]
contadorIndicador = [0]
class TelaAvalia(Screen):

    def refresh(self):
        self.ids.nome_barragem.text = barragem_selecionada[0]
        
        cursor.execute(f"SELECT id FROM Barragem WHERE Nome = '{barragem_selecionada[0]}' ")
        resultado = cursor.fetchall()
        print(resultado[0][0])
        subIndece[3] = resultado[0][0]


#Funções de ecolha da situação
#-------------------------------------------------
    def NA(self):
        self.ids.situacao.text = "SITUAÇÃO: ( NA )"
        subIndece[0] = 'NA'
        print(subIndece[0])

    def NE(self):
        self.ids.situacao.text = "SITUAÇÃO: ( NE )"
        subIndece[0] = 'NE'
        print(subIndece[0])

    def PV(self):
        self.ids.situacao.text = "SITUAÇÃO: ( PV )"
        subIndece[0] = 'PV'
        print(subIndece[0])

    def DS(self):
        self.ids.situacao.text = "SITUAÇÃO: ( DS )"
        subIndece[0] = 'DS'
        print(subIndece[0])   

    def DI(self):
        self.ids.situacao.text = "SITUAÇÃO: ( DI )"
        subIndece[0] = 'DI'
        print(subIndece[0])

    def PC(self):
        self.ids.situacao.text = "SITUAÇÃO: ( PC )"
        subIndece[0] = 'PC'
        print(subIndece[0])
                
    def AU(self):
        self.ids.situacao.text = "SITUAÇÃO: ( AU )"
        subIndece[0] = 'AU'
        print(subIndece[0])
                
    def NI(self):
        self.ids.situacao.text = "SITUAÇÃO: ( NI )"
        subIndece[0] = 'NI'
        print(subIndece[0])
#---------------------------------------------------              
#---------------------------------------------------              


#Funções de escolha da magnetude
#---------------------------------------------------                
    def I(self):
        self.ids.magnetude.text = "MAGNETUDE: ( I )"
        subIndece[1] = 'I'
        print(subIndece[1])

    def P(self):
        self.ids.magnetude.text = "MAGNETUDE: ( P )"
        subIndece[1] = 'P'
        print(subIndece[1])
                
    def T(self):
        self.ids.magnetude.text = "MAGNETUDE: ( T )"
        subIndece[1] = 'T'
        print(subIndece[1])
                
    def G(self):
        self.ids.magnetude.text = "MAGNETUDE: ( G )"
        subIndece[1] = 'G'
        print(subIndece[1])
#---------------------------------------------------              
#---------------------------------------------------              

#Funções de escolha da magnetude
#---------------------------------------------------                
    def _0(self):
        self.ids.np.text = "NP: ( 0 )"
        subIndece[2] = '0'
        print(subIndece[2])

    def _1(self):
        self.ids.np.text = "NP: ( 1 )"
        subIndece[2] = '1'
        print(subIndece[2])
                
    def _2(self):
        self.ids.np.text = "NP: ( 2 )"
        subIndece[2] = '2'
        print(subIndece[2])
                
    def _3(self):
        self.ids.np.text = "NP: ( 3 )"
        subIndece[2] = 'G'
        print(subIndece[2])
#---------------------------------------------------              
#---------------------------------------------------   

    def proximo(self):
        try:
            cursor.execute("SELECT * FROM Indicadores")
            listaIndicador = cursor.fetchall()

            if  subIndece[0] == '' or subIndece[1] == '' or subIndece[2] == '':
                if  subIndece[0] == '':     self.ids.statusSituacao.text = 'Falta preencher!'
                else:                       self.ids.statusSituacao.text = ''
                if subIndece[1] == '':      self.ids.statusMagnetude.text = 'Falta preencher!'
                else:                       self.ids.statusMagnetude.text = ''
                if subIndece[2] == '':      self.ids.statusNp.text = 'Falta preencher!'
                else:                       self.ids.statusNp.text = ''

            elif listaIndicador[contadorIndicador[0]][1] == self.ids.indicador.text:
                cursor.execute(f"""
                SELECT * 
                FROM metaIndicador 
                WHERE id_indicadores = {contadorIndicador[0] + 2}
                """)
                resultado = cursor.fetchall()
                if resultado != []:
                    contadorIndicador[0] += 1
                    print(resultado)
                    self.ids.indicador.text = listaIndicador[contadorIndicador[0]][1]
                    self.ids.quantidade.text = f"{contadorIndicador[0] + 1}/7"

                    self.ids.situacao.text = f'SITUAÇÃO: ( {resultado[0][1]} )'
                    self.ids.magnetude.text = f'MAGNETUDE: ( {resultado[1][1]} )'  
                    self.ids.np.text = f'NP: ( {resultado[2][1]} )'
                    subIndece[0] = f'{resultado[0][1]}'
                    subIndece[1] = f'{resultado[1][1]}'
                    subIndece[2] = f'{resultado[2][1]}'

                else: 
                    cursor.execute(f"INSERT INTO metaIndicador VALUES ('SITUAÇÃO', '{subIndece[0]}', {int(listaIndicador[contadorIndicador[0]][0])}, {int(subIndece[3])})")
                    cursor.execute(f"INSERT INTO metaIndicador VALUES ('MAGNETUDE', '{subIndece[1]}', {int(listaIndicador[contadorIndicador[0]][0])}, {int(subIndece[3])})")
                    cursor.execute(f"INSERT INTO metaIndicador VALUES ('NP', '{subIndece[2]}', {int(listaIndicador[contadorIndicador[0]][0])}, {int(subIndece[3])})")

                    banco.commit()

                    contadorIndicador[0] += 1
                    self.ids.indicador.text = listaIndicador[contadorIndicador[0]][1]
                    
                    self.ids.quantidade.text = f"{contadorIndicador[0] + 1}/7"

                    self.ids.situacao.text = 'SITUAÇÃO: ( )'
                    self.ids.magnetude.text = 'MAGNETUDE: ( )'  
                    self.ids.np.text = 'NP: ( )'
                    subIndece[0] = ''
                    subIndece[1] = ''
                    subIndece[2] = ''
                    self.ids.statusSituacao.text = ''
                    self.ids.statusMagnetude.text = ''
                    self.ids.statusNp.text = ''
        except:
            pass

    def voltar(self):
        try:
            # consulda o banco para comparações de indicadores 
            cursor.execute("SELECT * FROM Indicadores")
            listaIndicador = cursor.fetchall()

            # mantem o array no range de indicadores
            if contadorIndicador[0] >= 7: contadorIndicador[0] = 6

            cursor.execute(f"""
            SELECT * 
            FROM metaIndicador 
            WHERE id_indicadores = {contadorIndicador[0]}
            """)
            resultado = cursor.fetchall()
            print(resultado)
            self.ids.situacao.text = f'SITUAÇÃO: ( {resultado[0][1]} )'
            self.ids.magnetude.text = f'MAGNETUDE: ( {resultado[1][1]} )'  
            self.ids.np.text = f'NP: ( {resultado[2][1]} )'



            if listaIndicador[contadorIndicador[0]][1] == self.ids.indicador.text and self.ids.indicador.text != 'Erupsões':
                contadorIndicador[0] -= 1   

                # adiciona o texto novo do indicador e seu número
                self.ids.indicador.text = listaIndicador[contadorIndicador[0]][1]
                self.ids.quantidade.text = f"{contadorIndicador[0] + 1}/7"

                subIndece[0] = f'{resultado[0][1]}'
                subIndece[1] = f'{resultado[1][1]}'
                subIndece[2] = f'{resultado[2][1]}'

        except:
            pass

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
                self.ids.result.text = '                 Cadastrado com sucesso'
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