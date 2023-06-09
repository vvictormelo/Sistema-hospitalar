import sqlite3 as sq
import entities


# Implementação e criação do banco de dados
class Database:
    def conectadb(self):
        self.conn = sq.connect("hospital.db")
        self.cursor = self.conn.cursor()

    def desconectdb(self):
        self.cursor.close()
        self.conn.close()

    def criartabelas(self):
        try:
            self.conectadb()
            self.conn.execute("PRAGMA foreign_keys=on")

            # Criação da tabela do hospital
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS hospital( 
                                cnpj TEXT(13) PRIMARY KEY UNIQUE,
                                nome TEXT(20) NOT NULL,
                                rua TEXT(50) NOT NULL,
                                bairro TEXT(20) NOT NULL,
                                cidade TEXT(20) NOT NULL,
                                cep TEXT(8) NOT NULL,
                                telefone INTEGER(10) NOT NULL)"""
            )

            # Criação da tabela do medico
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS medico(
                                crm TEXT(10) PRIMARY KEY UNIQUE,
                                cpf TEXT(11) NOT NULL,
                                nome TEXT(50) NOT NULL,
                                rua TEXT(50) NOT NULL,
                                bairro TEXT(20) NOT NULL,
                                cidade TEXT(20) NOT NULL,
                                cep INTEGER(8) NOT NULL)"""
            )

            # Criação da tabela auxiliar hospital x medico
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS hosp_med(
                                cnpj REFERENCES hospital(cnpj),
                                crm REFERENCES medico(crm),
                                PRIMARY KEY (cnpj, crm)) """
            )

            # Criação da tabela auxiliar hospital x enfermeira
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS hosp_enfer(
                                cnpj REFERENCES hospital(cnpj),
                                coren REFERENCES enfermeira(coren),
                                PRIMARY KEY (cnpj, coren))"""
            )

            # Criação da tabela auxiliar medico x paciente
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS med_pac(
                                crm REFERENCES medico(crm),
                                cpf REFERENCES paciente(cpf),
                                PRIMARY KEY (crm, cpf))"""
            )

            # Criação da tabela auxiliar medico x enfermeira
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS med_enf(
                                crm REFERENCES medico(crm),
                                coren REFERENCES enfermeira(coren),
                                PRIMARY KEY (crm, coren))"""
            )

            # Criação da tabela especialidade
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS especialidade(
                                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                                documento REFERENCES medico(crm),
                                especi_desc TEXT(50) NOT NULL)"""
            )

            # Criação da tabela telefone
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS telefone(
                                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                                documento REFERENCES medico(crm),
                                tel INTEGER NOT NULL)"""
            )

            # Criação da tabela enfermeira
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS enfermeira(
                                coren TEXT(10) PRIMARY KEY UNIQUE,
                                cpf TEXT(11) NOT NULL,
                                nome TEXT(50) NOT NULL,
                                rua TEXT(50) NOT NULL,
                                bairro TEXT(20) NOT NULL,
                                cidade TEXT(20) NOT NULL,
                                cep INTEGER(8) NOT NULL)"""
            )

            # Criação da tabela paciente
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS paciente(
                                cpf TEXT(11) NOT NULL,
                                rg TEXT(10) NOT NULL,
                                nome TEXT(50) NOT NULL,
                                rua TEXT(50) NOT NULL,
                                bairro TEXT(20) NOT NULL,
                                cidade TEXT(20) NOT NULL,
                                cep TEXT(8) NOT NULL)"""
            )

            self.conn.commit()
            print("\033[1;36m\nTabelas criadas com sucesso!\033[m")

        except ConnectionError as e:
            print("Erro no banco", e)

        finally:
            self.desconectdb()


db = Database()


#  Implementação do menu e chamada de métodos das entidades
class menufront:
    def __init__(self):
        super().__init__()
        self.program()

    def menu(self):
        print("\n")
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"MENU INICIAL":>22}\033[m')
        print("\033[1;36m-=\033[m" * 15)
        print("\n1 - Criar tabelas")
        print("")
        print("Hospital")
        print("2 - Criar hospital")
        print("2.1 - Excluir hospital")
        print("2.2 - Alterar hospital")
        print("")
        print("Médicos")
        print("3 - Criar médico(a)")
        print("3.1 - Deletar médico(a)")
        print("3.2 - Alterar médico(a)")
        print("")
        print("Enfermeira")
        print("4 - Criar enfermeira(o)")
        print("4.1 - Deletar enfermeira(o)")
        print("4.2 - Alterar enfermeira(o)")
        print("")
        print("Paciente")
        print("5 - Criar paciente")
        print("5.1 - Deletar paciente")
        print("5.2 - Alterar paciente")
        print("")
        print("Vínculos")
        print("6 - Vincular Hospital a Médico")
        print("6.1 - Vincular Médico(a) a Enfermeira(o)")
        print("6.2 - Vincular Hospital a Enfermeira(o)")
        print("6.3 - Vincular Médico(a) a Paciente")
        print("")
        print("Relatórios")
        print("7 - Relatório geral de médicos")
        print("7.1 - Relatório geral de pacientes")
        print("7.2 - Relatório geral de enfermeiros")
        print("7.3 - Relatório geral de hospitais")
        print("7.4 - Relatório de pacientes residentes no Centro de Aracaju")
        print("7.5 - Relatório médicos e telefones")
        print("7.6 - Relatório do corpo clínico")
        print("")
        print("8 - Sair")

    def program(self):
        print("\033[1;36m\nSEJA BEM VINDO...\033[m")

        self.acao = 0

        while self.acao != 8:
            try:
                self.menu()
                self.acao = float(input("\nInsira a ação desejada: "))
                match self.acao:
                    case 1:
                        db.criartabelas()
                    case 2:
                        self.insert_hospital()
                    case 2.1:
                        self.delete_hospital()
                    case 2.2:
                        self.update_hospital()
                    case 3:
                        self.insert_medico()
                    case 3.1:
                        self.delete_medico()
                    case 3.2:
                        self.update_medico()
                    case 4:
                        self.insert_enfermeira()
                    case 4.1:
                        self.delete_enfermeira()
                    case 4.2:
                        self.update_enfermeira()
                    case 5:
                        self.insert_paciente()
                    case 5.1:
                        self.delete_paciente()
                    case 5.2:
                        self.update_paciente()
                    case 6:
                        self.vincular_med_hosp()
                    case 6.1:
                        self.vincular_med_enf()
                    case 6.2:
                        self.vincular_hosp_enf()
                    case 6.3:
                        self.vincular_med_pac()
                    case 7:
                        self.rel_geral_medicos()
                    case 7.1:
                        self.rel_geral_pacientes()
                    case 7.2:
                        self.rel_geral_enfermeiros()
                    case 7.3:
                        self.rel_geral_hospital()
                    case 7.4:
                        self.rel_paciente_centro_aju()
                    case 7.5:
                        self.rel_medicos_telefone()
                    case 7.6:
                        self.rel_corpo_clinico()
                    case 8:
                        self.acao = 8
                        print("\nSaindo... Até logo!")
                if self.acao > 8 or self.acao < 1:
                    print("\033[1;31m\nOops...Ação inválida. Tente novamente!\n\033[m")

            except ValueError:
                print("\033[1;31m\nOops...Ação inválida. Tente novamente!\n\033[m")

    # Instanciando métodos da entidade Médico
    def insert_medico(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"CADASTRO DE MÉDICO(A)":>26}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        crm = input("CRM: ")
        cpf = input("CPF: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = input("CEP: ")

        medico = entities.Medico(crm, cpf, nome, rua, bairro, cidade, cep)
        medico.inserir_medico()

        verifi_telefone = input("\nDeseja cadastrar telefone?('Ss/Nn') ")

        if verifi_telefone in "SssimSimSIM":
            telefone = input("Telefone: ")

            med_tel = entities.Telefone(crm, telefone)
            med_tel.inserir_telefone()

        verifi_espe = input("\nDeseja cadastrar especialidade?('Ss/Nn') ")

        if verifi_espe in "SssimSimSIM":
            especialidade = input("Especialide: ")
            med_espe = entities.Especialidade(crm, especialidade)
            med_espe.inserir_especialidade()
        else:
            self.program()

    def delete_medico(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"EXCLUIR CADASTRO MEDICO":>26}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        crm = input("\nInsira o CRM do médico(a): ")

        medico = entities.Medico(crm, None, None, None, None, None, None)

        medico.buscar_medico()

        check = input("\nDeseja confirmar a exclusão? ")

        if check in "SssimSim":
            medico.deletar_medico()
        else:
            self.program()

    def update_medico(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"ALTERAR CADASTRO MEDICO":>27}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("*Insira as novas informações*")
        crm = input("CRM: ")
        cpf = input("CPF: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = int(input("CEP: "))

        medico = entities.Medico(crm, cpf, nome, rua, bairro, cidade, cep)

        medico.alterar_medico()

    # Instanciando métodos da entidade Hospital
    def insert_hospital(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"CADASTRO DE HOSPITAL":>20}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        cnpj = input("CNPJ: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = int(input("CEP: "))
        telefone = int(input("Telefone: "))

        hosp = entities.Hospital(cnpj, nome, rua, bairro, cidade, cep, telefone)

        hosp.inserir_hospital()

    def delete_hospital(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"EXCLUIR CADASTRO HOSPITAL":>26}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        cnpj = input("\nInsira o CNPJ do hospital: ")

        hosp = entities.Hospital(cnpj, None, None, None, None, None, None)

        hosp.buscar_hospital()

        check = input("\nDeseja confirmar a exclusão? ")

        if check in "SssimSim":
            hosp.deletar_hospital()
        else:
            self.program()

    def update_hospital(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"ALTERAR CADASTRO HOSPITAL":>27}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("*Insira as novas informações*")
        cnpj = input("CNPJ: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = int(input("CEP: "))
        tel = int(input("Telefone: "))

        hosp = entities.Hospital(cnpj, nome, rua, bairro, cidade, cep, tel)

        hosp.alterar_hospital()

    # Instanciando métodos da entidade Enfermeira
    def insert_enfermeira(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"CADASTRO DE ENFERMEIRA":>26}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        coren = input("COREN: ")
        cpf = input("CPF: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = input("CEP: ")

        enf = entities.Enfermeira(coren, cpf, nome, rua, bairro, cidade, cep)

        enf.inserir_enfermeira()

    def delete_enfermeira(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"EXCLUIR CADASTRO ENFERMEIRA":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        coren = input("\nInsira o COREN da enfermeira(o): ")

        enf = entities.Enfermeira(coren, None, None, None, None, None, None)

        enf.buscar_enfermeira()

        check = input("\nDeseja confirmar a exclusão? ")

        if check in "SssimSim":
            enf.deletar_enfermeira()
        else:
            self.program()

    def update_enfermeira(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"ALTERAR CADASTRO ENFERMEIRA":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("*Insira as novas informações*")
        coren = input("COREN: ")
        cpf = input("CPF: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = int(input("CEP: "))

        enf = entities.Enfermeira(coren, cpf, nome, rua, bairro, cidade, cep)

        enf.alterar_enfermeira()

    # Instanciando métodos da entidade Paciente
    def insert_paciente(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"CADASTRO DE PACIENTE":>25}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        cpf = input("CPF: ")
        rg = input("RG: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = input("CEP: ")

        pac = entities.Paciente(cpf, rg, nome, rua, bairro, cidade, cep)

        pac.inserir_paciente()

    def delete_paciente(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"EXCLUIR CADASTRO PACIENTE":>28}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        cpf = input("\nInsira o CPF do paciente: ")

        pac = entities.Paciente(cpf, None, None, None, None, None, None, None)

        pac.buscar_paciente()

        check = input("\nDeseja confirmar a exclusão? ")

        if check in "SssimSim":
            pac.deletar_paciente()
        else:
            self.program()

    def update_paciente(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"ALTERAR CADASTRO PACIENTE":>28}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("*Insira as novas informações*")
        cpf = input("CPF: ")
        rg = input("RG: ")
        nome = input("Nome: ")
        print("*Endereço*")
        rua = input("Rua: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        cep = int(input("CEP: "))

        pac = entities.Paciente(cpf, rg, nome, rua, bairro, cidade, cep)

        pac.alterar_paciente()

    # Instanciando métodos de vínculos
    def vincular_med_hosp(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"VÍNCULAR MÉDICO A HOSPITAL":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("\nHospitais cadastados:")
        entities.Hospital.listar_hospitais(self)

        print("\nMédicos cadastados:")
        entities.Medico.listar_medicos(self)

        cnpj = input("\nInsira o CNPJ do hospital: ")
        crm = input("Insira o CRM do médico: ")

        hosp_med = entities.HospMed(cnpj, crm)
        hosp_med.vinc_hospital_medicos()

    def vincular_hosp_enf(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"VÍNCULAR ENFERMEIRA A HOSPITAL":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("\nHospitais cadastados:")
        entities.Hospital.listar_hospitais(self)

        print("\nEnfermeiros cadastados:")
        entities.Enfermeira.listar_enfermeiros(self)

        cnpj = input("\nInsira o CNPJ do hospital: ")
        coren = input("Insira o COREN do enfermeiro: ")

        hosp_enf = entities.HospEnf(cnpj, coren)
        hosp_enf.vinc_hospital_medicos()

    def vincular_med_pac(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"VÍNCULAR MÉDICO A PACIENTE":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("\nMédicos cadastados:")
        entities.Medico.listar_medicos(self)

        print("\nPacientes cadastados:")
        entities.Paciente.listar_pacientes(self)

        crm = input("\nInsira o CNPJ do hospital: ")
        cpf = input("Insira o COREN do enfermeiro: ")

        med_pac = entities.MedPac(crm, cpf)
        med_pac.vinc_medicos_paciente()

    def vincular_med_enf(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"VÍNCULAR MÉDICO A ENFERMEIRO":>29}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        print("\nMédicos cadastados:")
        entities.Medico.listar_medicos(self)

        print("\nEnfermeiros cadastados:")
        entities.Enfermeira.listar_enfermeiros(self)

        crm = input("\nInsira o CRM do médico: ")
        coren = input("Insira o COREN do enfermeira: ")

        med_enf = entities.MedEnf(crm, coren)
        med_enf.vinc_medicos_enfermeiros()

    # Métodos dos relatórios
    def rel_geral_medicos(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO GERAL DE MÉDICOS":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select crm, cpf, nome, rua, bairro, cidade, cep from medico"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nMédicos cadastados:")
            for medico in db.cursor.fetchall():
                crm, cpf, nome, rua, bairro, cidade, cep = medico
                print(
                    f"""CRM: {crm} / CPF: {cpf} / Nome do Médico: {nome} / Endereço. Rua: {rua} / Bairro: {bairro} / Cidade: {cidade} / CEP: {cep}"""
                )

        except Exception as e:
            print("Erro ao buscar médicos:", e)

        finally:
            db.desconectdb()

    def rel_geral_pacientes(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO GERAL DE PACIENTES":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select cpf, rg, nome, rua, bairro, cidade, cep from paciente"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nPacientes cadastados:")
            for paciente in db.cursor.fetchall():
                cpf, rg, nome, rua, bairro, cidade, cep = paciente
                print(
                    f"""CPF: {cpf} / RG: {rg} / Nome do Paciente: {nome} / Endereço. Rua: {rua} / Bairro: {bairro} / Cidade: {cidade} / CEP: {cep}"""
                )

        except Exception as e:
            print("Erro ao buscar pacientes:", e)

        finally:
            db.desconectdb()

    def rel_geral_enfermeiros(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO GERAL DE ENFERMEIROS":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select coren, cpf, nome, rua, bairro, cidade, cep from enfermeira"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nEnfermeiros cadastados:")
            for enfermeiro in db.cursor.fetchall():
                coren, cpf, nome, rua, bairro, cidade, cep = enfermeiro
                print(
                    f"""COREN: {coren} / CPF: {cpf} / Nome do Enfermeiro: {nome} / Endereço. Rua: {rua} / Bairro: {bairro} / Cidade: {cidade} / CEP: {cep}"""
                )

        except Exception as e:
            print("Erro ao buscar enfermeiros:", e)

        finally:
            db.desconectdb()

    def rel_geral_hospital(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO GERAL DE HOSPITAIS":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select cnpj, nome, rua, bairro, cidade, cep, telefone from hospital"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nHospitais cadastados:")
            for hospital in db.cursor.fetchall():
                cnpj, nome, rua, bairro, cidade, cep, telefone = hospital
                print(
                    f"""CNPJ: {cnpj} / Nome do Hospital: {nome} / Endereço. Rua: {rua} / Bairro: {bairro} / Cidade: {cidade} / CEP: {cep} / Telefone: {telefone}"""
                )

        except Exception as e:
            print("Erro ao buscar hospital:", e)

        finally:
            db.desconectdb()

    def rel_paciente_centro_aju(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO PACIENTE NO CENTRO DE AJU":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select cpf, rg, nome, rua, bairro, cidade, cep from paciente where UPPER(bairro) = 'CENTRO' and UPPER(cidade) = 'ARACAJU' "

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nPacientes cadastados:")
            for paciente in db.cursor.fetchall():
                cpf, rg, nome, rua, bairro, cidade, cep = paciente
                print(
                    f"""CPF: {cpf} / RG: {rg} /Nome do paciente: {nome} / Endereço. Rua: {rua} / Bairro: {bairro} / Cidade: {cidade} / CEP: {cep}"""
                )

        except Exception as e:
            print("Erro ao buscar paciente:", e)

        finally:
            db.desconectdb()

    def rel_medicos_telefone(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO MÉDICOS COM TELEFONE":>30}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select crm, cpf, nome, tel from medico m join telefone t on t.documento = m.crm order by m.crm"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nMédicos cadastados:")
            for medico in db.cursor.fetchall():
                crm, cpf, nome, tel = medico
                print(
                    f"""CRM: {crm} / CPF: {cpf} / Nome do medico: {nome} / Telefone: {tel}"""
                )

        except Exception as e:
            print("Erro ao buscar medicos:", e)

        finally:
            db.desconectdb()

    def rel_corpo_clinico(self):
        print("\033[1;36m-=\033[m" * 15)
        print(f'\033[1;36m{"RELATÓRIO CORPO CLÍNICO":>27}\033[m')
        print("\033[1;36m-=\033[m" * 15)

        query = "select cnpj, nome from hospital"

        try:
            db.conectadb()
            db.cursor.execute(query)

            print("\nHospitais cadastados:")
            for hospital in db.cursor.fetchall():
                cnpj, nome = hospital
                print(f"""CNPJ: {cnpj} / Nome: {nome}""")

        except Exception as e:
            print("Erro ao buscar hospital:", e)

        finally:
            db.desconectdb()

        self.cnpj = input("\nInsira o CNPJ do hospital: ")

        query = "select h.cnpj, h.nome, m.crm, m.nome, e.coren, e.nome from hospital h join hosp_med hm on h.cnpj = hm.cnpj join  medico m on m.crm = hm.crm join hosp_enfer he on he.cnpj = h.cnpj join enfermeira e on e.coren = he.coren where h.cnpj = (?) order by h.cnpj"
        parametros = (self.cnpj,)

        try:
            db.conectadb()
            db.cursor.execute(query, parametros)

            print("\nCorpo Clínico:")

            for corpo in db.cursor.fetchall():
                h_cnpj, h_nome, m_crm, m_nome, e_coren, e_nome = corpo
                print(
                    f"""CNPJ: {h_cnpj} / Nome: {h_nome} / Médico - CRM: {m_crm} / Médico - Nome: {m_nome} / Enfermério - COREN: {e_coren} / Enfermério - Nome: {e_nome}"""
                )

        except Exception as e:
            print("Erro ao buscar corpo clínico:", e)

        finally:
            db.desconectdb()


if __name__ == "__main__":
    app = menufront()
