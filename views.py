from datetime import date, timedelta
from models import Conta, Historico, Tipos, engine, Bancos, Status
from sqlmodel import select, Session

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()

        if results:
            print('Já existe uma conta nesse banco.')
            return
        
        session.add(conta)
        session.commit()
        return conta

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results
    
def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()
        if Conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo.')
        conta.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError('Saldo insulficiente.')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()
        
        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        # TODO: Validar se a conta está ativa.
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError('Saldo insulficiente.')
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico
    
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()

        total = 0

        for conta in contas:
            total += conta.valor
        return float(total)

def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(Historico.data >= data_inicio, Historico.data <= data_fim)
        results =  session.exec(statement).all()
        return results

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        contas = session.exec(statement).all()

        bancos = [conta.banco.value for conta in contas]
        total = [conta.valor for conta in contas]

        import matplotlib.pyplot as plt

        plt.bar(bancos, total)
        plt.show()

        
# Criando contas
#conta = Conta(valor=100, banco=Bancos.SANTANDER)
#criar_conta(conta)

# Listando contas
#print(listar_contas())
        
# Transferindo Saldo
# transferir_saldo(1,2,30)
    
# Verificando Historico
#historico = Historico(conta_id=1, tipo=Tipos.ENTRADA, valor=10, data=date.today())
#movimentar_dinheiro(historico)
            
# Verificando todas as contas
# print(total_contas())
    
# Buscar historico
#x = buscar_historico_entre_datas(date.today() - timedelta(days = 1), date.today() + timedelta(days=1))
#print(x)

# Criando Gráfico
# criar_grafico_por_conta()