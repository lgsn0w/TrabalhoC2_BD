import cx_Oracle
import pandas as pd

db_usuario = 'labdatabase'
db_senha = 'labDatabase2022'
db_dsn = 'localhost:1521/xe'

class Doador:
    def __init__(self, cpf, nome, tipo_sanguineo, telefone, endereco):
        self.cpf = cpf
        self.nome = nome
        self.tipo_sanguineo = tipo_sanguineo
        self.telefone = telefone
        self.endereco = endereco

    def get_cpf(self):
        return self.cpf

    def get_nome(self):
        return self.nome

    def get_tipo_sanguineo(self):
        return self.tipo_sanguineo

    def get_telefone(self):
        return self.telefone

    def get_endereco(self):
        return self.endereco

    def set_cpf(self, cpf):
        self.cpf = cpf

    def set_nome(self, nome):
        self.nome = nome

    def set_tipo_sanguineo(self, tipo_sanguineo):
        self.tipo_sanguineo = tipo_sanguineo

    def set_telefone(self, telefone):
        self.telefone = telefone

    def set_endereco(self, endereco):
        self.endereco = endereco

    def to_string(self):
        return f"CPF: {self.cpf}, Nome: {self.nome}, Tipo Sanguíneo: {self.tipo_sanguineo}, Telefone: {self.telefone}, Endereço: {self.endereco}"

class BancoDeSangue:
    def __init__(self, cnpj, razao_social, nome_fantasia):
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia

    def get_cnpj(self):
        return self.cnpj

    def get_razao_social(self):
        return self.razao_social

    def get_nome_fantasia(self):
        return self.nome_fantasia

    def set_cnpj(self, cnpj):
        self.cnpj = cnpj

    def set_razao_social(self, razao_social):
        self.razao_social = razao_social

    def set_nome_fantasia(self, nome_fantasia):
        self.nome_fantasia = nome_fantasia

    def to_string(self):
        return f"CNPJ: {self.cnpj}, Razão Social: {self.razao_social}, Nome Fantasia: {self.nome_fantasia}"

class Doacao:
    def __init__(self, codigo_doacao, cpf_doador, cnpj_banco_sangue, data_doacao, quantidade_unidades):
        self.codigo_doacao = codigo_doacao
        self.cpf_doador = cpf_doador
        self.cnpj_banco_sangue = cnpj_banco_sangue
        self.data_doacao = data_doacao
        self.quantidade_unidades = quantidade_unidades

    def get_codigo_doacao(self):
        return self.codigo_doacao

    def get_cpf_doador(self):
        return self.cpf_doador

    def get_cnpj_banco_sangue(self):
        return self.cnpj_banco_sangue

    def get_data_doacao(self):
        return self.data_doacao

    def get_quantidade_unidades(self):
        return self.quantidade_unidades

    def set_codigo_doacao(self, codigo_doacao):
        self.codigo_doacao = codigo_doacao

    def set_cpf_doador(self, cpf_doador):
        self.cpf_doador = cpf_doador

    def set_cnpj_banco_sangue(self, cnpj_banco_sangue):
        self.cnpj_banco_sangue = cnpj_banco_sangue

    def set_data_doacao(self, data_doacao):
        self.data_doacao = data_doacao

    def set_quantidade_unidades(self, quantidade_unidades):
        self.quantidade_unidades = quantidade_unidades

    def to_string(self):
        return f"Código: {self.codigo_doacao}, CPF Doador: {self.cpf_doador}, CNPJ Banco de Sangue: {self.cnpj_banco_sangue}, Data: {self.data_doacao}, Quantidade: {self.quantidade_unidades} ml"

class Relatorio:
    def __init__(self, usuario, senha, dsn):
        self.conexao = cx_Oracle.connect(user=usuario, password=senha, dsn=dsn)
        self.cursor = self.conexao.cursor()

    def get_record_count(self, entity):
        self.cursor.execute(f"SELECT COUNT(1) FROM {entity}")
        result = self.cursor.fetchone()
        return result[0]

    def insert_doador(self, doador):
        if self.is_cpf_exists(doador.cpf):
            raise Exception("CPF already exists. Cannot add duplicate record.")

        inserir_query = "INSERT INTO DOADORES (CPF, NOME, TIPO_SANGUINEO, TELEFONE, ENDERECO) VALUES (:1, :2, :3, :4, :5)"
        dados = (doador.cpf, doador.nome, doador.tipo_sanguineo, doador.telefone, doador.endereco)
        self.cursor.execute(inserir_query, dados)
        self.conexao.commit()

    def update_doador(self, cpf, dados):
        if not self.is_cpf_exists(cpf):
            raise Exception("CPF does not exist. Cannot update non-existing record.")

        atualizar_query = "UPDATE DOADORES SET CPF = :1, NOME = :2, TIPO_SANGUINEO = :3, TELEFONE = :4, ENDERECO = :5 WHERE CPF = :6"
        dados_com_id = dados + (cpf,)
        self.cursor.execute(atualizar_query, dados_com_id)
        self.conexao.commit()

    def delete_doador(self, cpf):
        if not self.is_cpf_exists(cpf):
            raise Exception("CPF does not exist. Cannot delete non-existing record.")

        deletar_query = "DELETE FROM DOADORES WHERE CPF = :1"
        self.cursor.execute(deletar_query, (cpf,))
        self.conexao.commit()

    def is_cpf_exists(self, cpf):
        self.cursor.execute("SELECT COUNT(*) FROM DOADORES WHERE CPF = :1", (cpf,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def get_doadores(self):
        self.cursor.execute("SELECT * FROM DOADORES")
        resultado = self.cursor.fetchall()
        doadores = []
        for row in resultado:
            cpf, nome, tipo_sanguineo, telefone, endereco = row
            doador = Doador(cpf, nome, tipo_sanguineo, telefone, endereco)
            doadores.append(doador)
        return doadores

    def insert_banco_de_sangue(self, banco_de_sangue):
        inserir_query = "INSERT INTO BANCOS_SANGUE (CNPJ, RAZAO_SOCIAL, NOME_FANTASIA) VALUES (:1, :2, :3)"
        dados = (banco_de_sangue.cnpj, banco_de_sangue.razao_social, banco_de_sangue.nome_fantasia)
        self.cursor.execute(inserir_query, dados)
        self.conexao.commit()

    def delete_banco_de_sangue(self, cnpj):
        deletar_query = "DELETE FROM BANCOS_SANGUE WHERE CNPJ = :1"
        self.cursor.execute(deletar_query, (cnpj,))
        self.conexao.commit()

    def update_banco_de_sangue(self, cnpj, dados):
        atualizar_query = "UPDATE BANCOS_SANGUE SET CNPJ = :1, RAZAO_SOCIAL = :2, NOME_FANTASIA = :3 WHERE CNPJ = :4"
        dados_com_id = dados + (cnpj,)
        self.cursor.execute(atualizar_query, dados_com_id)
        self.conexao.commit()

    def get_bancos_de_sangue(self):
        self.cursor.execute("SELECT * FROM BANCOS_SANGUE")
        resultado = self.cursor.fetchall()
        bancos = []
        for row in resultado:
            cnpj, razao_social, nome_fantasia = row
            banco = BancoDeSangue(cnpj, razao_social, nome_fantasia)
            bancos.append(banco)
        return bancos

    def insert_doacao(self, doacao):
        inserir_query = "INSERT INTO DOACOES (CODIGO_DOACAO, CPF_DOADOR, CNPJ_BANCO_SANGUE, DATA_DOACAO, QUANTIDADE_UNIDADES) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5)"
        dados = (doacao.codigo_doacao, doacao.cpf_doador, doacao.cnpj_banco_sangue, doacao.data_doacao, doacao.quantidade_unidades)
        self.cursor.execute(inserir_query, dados)
        self.conexao.commit()

    def delete_doacao(self, codigo_doacao):
        deletar_query = "DELETE FROM DOACOES WHERE CODIGO_DOACAO = :1"
        self.cursor.execute(deletar_query, (codigo_doacao,))
        self.conexao.commit()

    def update_doacao(self, codigo_doacao, dados):
        atualizar_query = "UPDATE DOACOES SET CPF_DOADOR = :1, CNPJ_BANCO_SANGUE = :2, DATA_DOACAO = TO_DATE(:3, 'YYYY-MM-DD'), QUANTIDADE_UNIDADES = :4 WHERE CODIGO_DOACAO = :5"
        dados_com_id = dados + (codigo_doacao,)
        self.cursor.execute(atualizar_query, dados_com_id)
        self.conexao.commit()

    def get_doacoes(self):
        self.cursor.execute("SELECT * FROM DOACOES")
        resultado = self.cursor.fetchall()
        doacoes = []
        for row in resultado:
            codigo_doacao, cpf_doador, cnpj_banco_sangue, data_doacao, quantidade_unidades = row
            doacao = Doacao(codigo_doacao, cpf_doador, cnpj_banco_sangue, data_doacao, quantidade_unidades)
            doacoes.append(doacao)
        return doacoes

    def close_connection(self):
        self.cursor.close()
        self.conexao.close()

def menu_doadores(relatorio):
    while True:
        print("#" * 30)
        print("#         Menu de Doadores           #")
        print("#                                    #")
        print("# 1. Adicionar Doador                #")
        print("# 2. Remover Doador                  #")
        print("# 3. Listar Doadores                 #")
        print("# 4. Atualizar Doador                #")
        print("# 5. Voltar ao Menu Principal        #")
        print("#" * 30)

        choice = int(input("Escolha uma opcao: "))

        if choice == 1:
            cpf = input("CPF: ")
            nome = input("Nome: ")
            tipo_sanguineo = input("Tipo Sanguineo: ")
            telefone = input("Telefone: ")
            endereco = input("Endereco: ")
            doador = Doador(cpf, nome, tipo_sanguineo, telefone, endereco)
            relatorio.insert_doador(doador)
            print("Doador adicionado com sucesso.")
        elif choice == 2:
            cpf = input("CPF do doador a ser removido: ")
            relatorio.delete_doador(cpf)
            print("Doador removido com sucesso.")
        elif choice == 3:
            doadores = relatorio.get_doadores()
            if doadores:
                print("Lista de Doadores:")
                for doador in doadores:
                    print(f"CPF: {doador.cpf}, Nome: {doador.nome}, Tipo Sanguineo: {doador.tipo_sanguineo}, Telefone: {doador.telefone}, Endereco: {doador.endereco}")
            else:
                print("Nenhum doador encontrado.")
        elif choice == 4:
            cpf = input("CPF do doador a ser atualizado: ")
            nome = input("Nome: ")
            tipo_sanguineo = input("Tipo Sanguineo: ")
            telefone = input("Telefone: ")
            endereco = input("Endereco: ")
            doador_data = (cpf, nome, tipo_sanguineo, telefone, endereco)
            relatorio.update_doador(cpf, doador_data)
            print("Doador atualizado com sucesso.")
        elif choice == 5:
            break
        else:
            print("Opcao invalida")

def menu_bancos_de_sangue(relatorio):
    while True:
        print("#" * 30)
        print("#    Menu de Bancos de Sangue        #")
        print("#                                    #")
        print("# 1. Adicionar Banco de Sangue       #")
        print("# 2. Remover Banco de Sangue         #")
        print("# 3. Listar Bancos de Sangue         #")
        print("# 4. Atualizar Banco de Sangue       #")
        print("# 5. Voltar ao Menu Principal        #")
        print("#" * 30)

        choice = int(input("Escolha uma opcao: "))

        if choice == 1:
            cnpj = input("Digite o CNPJ: ")
            razao_social = input("Digite a Razao Social: ")
            nome_fantasia = input("Digite o Nome Fantasia: ")
            banco_de_sangue = BancoDeSangue(cnpj, razao_social, nome_fantasia)
            relatorio.insert_banco_de_sangue(banco_de_sangue)
            print("Banco de Sangue adicionado com sucesso.")
        elif choice == 2:
            cnpj = input("Digite o CNPJ do Banco de Sangue a ser removido: ")
            relatorio.delete_banco_de_sangue(cnpj)
            print("Banco de Sangue removido com sucesso.")
        elif choice == 3:
            bancos = relatorio.get_bancos_de_sangue()
            if bancos:
                print("Lista de Bancos de Sangue:")
                for banco in bancos:
                    print(f"CNPJ: {banco.cnpj}, Razao Social: {banco.razao_social}, Nome Fantasia: {banco.nome_fantasia}")
            else:
                print("Nenhum banco de sangue encontrado.")
        elif choice == 4:
            cnpj = input("Digite o CNPJ do Banco de Sangue a ser atualizado: ")
            razao_social = input("Digite a Razao Social: ")
            nome_fantasia = input("Digite o Nome Fantasia: ")
            banco_data = (cnpj, razao_social, nome_fantasia)
            relatorio.update_banco_de_sangue(cnpj, banco_data)
            print("Banco de Sangue atualizado com sucesso.")
        elif choice == 5:
            break
        else:
            print("Opcao invalida")

def menu_doacoes(relatorio):
    while True:
        print("#" * 30)
        print("#         Menu de Doacoes            #")
        print("#                                    #")
        print("# 1. Adicionar Doacao                #")
        print("# 2. Remover Doacao                  #")
        print("# 3. Listar Doacoes                  #")
        print("# 4. Atualizar Doacao                #")
        print("# 5. Voltar ao Menu Principal        #")
        print("#" * 30)

        choice = input("Escolha uma opcao: ")

        if choice == "1":
            codigo_doacao = int(input("Codigo de Doacao: "))
            cpf_doador = input("CPF do Doador: ")
            cnpj_banco_sangue = input("CNPJ do Banco de Sangue: ")
            data_doacao = input("Data da Doacao (YYYY-MM-DD): ")
            quantidade_unidades = int(input("Quantidade de Unidades (ml): "))
            doacao = Doacao(codigo_doacao, cpf_doador, cnpj_banco_sangue, data_doacao, quantidade_unidades)
            relatorio.insert_doacao(doacao)
            print("Doacao adicionada com sucesso.")
        elif choice == "2":
            codigo_doacao = int(input("Codigo da Doacao a ser removida: "))
            relatorio.delete_doacao(codigo_doacao)
            print("Doacao removida com sucesso.")
        elif choice == "3":
            doacoes = relatorio.get_doacoes()
            if doacoes:
                print("Lista de Doacoes:")
                for doacao in doacoes:
                    print(f"Codigo de Doacao: {doacao.codigo_doacao}, CPF do Doador: {doacao.cpf_doador}, CNPJ do Banco de Sangue: {doacao.cnpj_banco_sangue}, Data: {doacao.data_doacao}, Quantidade de Unidades: {doacao.quantidade_unidades} ml")
            else:
                print("Nenhuma doacao encontrada.")
        elif choice == "4":
            codigo_doacao = int(input("Codigo da Doacao a ser atualizada: "))
            cpf_doador = input("CPF do Doador: ")
            cnpj_banco_sangue = input("CNPJ do Banco de Sangue: ")
            data_doacao = input("Data da Doacao (YYYY-MM-DD): ")
            quantidade_unidades = int(input("Quantidade de Unidades (ml): "))
            doacao_data = (cpf_doador, cnpj_banco_sangue, data_doacao, quantidade_unidades)
            relatorio.update_doacao(codigo_doacao, doacao_data)
            print("Doacao atualizada com sucesso.")
        elif choice == "5":
            break
        else:
            print("Opcao invalida")


def display_splash_screen(relatorio):
    total_doadores = relatorio.get_record_count("DOADORES")
    total_bancos_sangue = relatorio.get_record_count("BANCOS_SANGUE")
    total_doacoes = relatorio.get_record_count("DOACOES")
    print("#####################################################################")
    print("#              Laboratório de Doações de Sangue                     #")
    print("#                                                                   #")
    print("#          Bem-vindo ao Sistema de Gerenciamento                    #")
    print("#           de Doadores, Bancos de Sangue e Doações                 #")
    print("#                                                                   #")
    print("#   Este sistema permite o gerenciamento de doadores, bancos        #")
    print("#  de sangue e doações de sangue.                                   #")
    print("#                                                                   #")
    print("#                                                                   #")
    print("#                                                                   #")
    print("#CRIADO POR: LUCAS GABRIEL DAS NEVES MOURA                          #")
    print("#CRIADO POR: GUILHERME OLIVEIRA GUIMARÃES                           #")
    print("#CRIADO POR: EWERTON BORTOLOZO NUNES JUNIOR                         #")
    print("#CRIADO POR: RAFAELA DE AGUIAR ROCHA                                #")
    print("#CRIADO POR: GUILHERME MOREIRA RIBEIRO                              #")
    print("#                                                                   #")
    print("#DISCIPLINA: BANCO DE DADOS 2023/2                                  #")
    print("#                                                                   #")
    print("#PROFESSOR: HOWARD ROATTI                                           #")
    print("#####################################################################")
    print("")
    print("")
    print("")
    print("---------------------------------------------------------------------")
    print(f"\n    TOTAL DOADORES NO SISTEMA: {total_doadores}                 ")
    print(f"\n    TOTAL DE BANCOS DE SANGUE NO SISTEMA: {total_bancos_sangue} ")
    print(f"\n    TOTAL DOACOES NO SISTEMA: {total_doacoes}                   \n")
    print("---------------------------------------------------------------------")
    print("")
    print("")
    print("")


def main():
    relatorio = Relatorio(db_usuario, db_senha, db_dsn)
   
    display_splash_screen(relatorio)

    while True:
        print("######################################")
        print("#    Menu Principal (Laboratorio)    #")
        print("#                                    #")
        print("# 1. Menu de Doadores                #")
        print("# 2. Menu de Bancos de Sangue        #")
        print("# 3. Menu de Doacoes                 #")
        print("# 4. Sair                            #")
        print("######################################")

        choice = int(input("Escolha uma opcao:"))

        if choice == 1:
            menu_doadores(relatorio)
        elif choice == 2:
            menu_bancos_de_sangue(relatorio)
        elif choice == 3:
            menu_doacoes(relatorio)
        elif choice == 4:
            relatorio.close_connection()
            break
        else:
            print("Opcao invalida")

if __name__ == "__main__":
    main()
