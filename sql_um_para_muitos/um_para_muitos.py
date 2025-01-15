import sqlite3
from prettytable import PrettyTable

from pathlib  import Path
import os


os.system('cls')



db_path = Path('DB') / 'db_rel_1_n.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF EXISTS Clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para o cliente
    nome TEXT NOR NULL,                           -- Nome do cliente
    email TEXT UNIQUE NOT NULL,                   -- Email único
    telefone TEXT,                                -- Telefone do cliente
    cidade TEXT                                   -- Cidade onde mora
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Pedidos (
    id_pedido INTERGER PRIMARY KEY AUTOINCREMENT, -- ID único para o pedido
    id_cliente INTEGER NOT NULL,                  -- Relacionamento com a tbela clientes
    produto TEXT NOT NULL,                        -- Nome do produto pedido
    quantidade INTEGER NOT NULL,                  -- Quantidade do produto
    data TEXT NOT NULL,                           -- Data do pedido
    valor_total REAL NOT NULL,                    -- Valor total do pedido
    FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente) -- Chave estrangeira
)
''')




def cliente_existe(id_cliente):
    cursor.execute(
        'SELECT 1 FROM Cliente WHERE id_cliente = ?', (id_cliente))
    
    return cursor.fetchone() is not None
    



def inserir_cliente():
    nome = input('Digite o nome do cliente: ')
    email = input('Digite o email do cliente: ')
    telefone = input('Digite o telefone do cliente: ')
    cidade = input('Digite a cidade do cliente: ')
    cursor.execute(''' 
    INSERT INTO Clientes (nome, email, telefone, cidade)
    VALUES (?, ?, ?, ?)
    ''', (nome, email, telefone, cidade))
    conn.commit()
    print('Cliente inserido com sucesso!')
    
    
    
    
def inserir_pedido():
    cursor.execute(''' 
    SELECT * from clientes
    ''')
    resultados = cursor.fetchall()
    
    
    if not resultados:
        print('-' *70)
        print('Nenhum cliente encontrado. Cadastre um cliente primeiro')
        print('-'* 70)
        return
    
    
    
    tabela = PrettyTable(['id_cliente', 'Nome', 'Email', 'Telefone', 'Cidade'])
    for linha in resultados:
        tabela.add_row(linha)
    print(tabela)
    
    try: 
        
        id_cliente = int(input('Digite o ID do cliente: '))
        
        
        if not cliente_existe(id_cliente):
            print('-' * 70)
            print(f'Erro: Cliente com ID {id_cliente} não encontrado!')
            print('Por favor, cadastre o cliente primeiro.')
            print('-' * 70)
            
            return
        
        
        produto = input('Digite o nome do produto: ')
        quantidade = int(input('Digite a quantidade: '))
        
        data = input('Digite a data do pedido (YYYY-MM-DD): ')
        valor_total = float(input('Digite o valor total: '))
        
        
        cursor.execute(''' 
        INSERT INTO Pedidos (id_cliente, produto, quantidade, data, valor_total)
        VALUES (?,?,?,?,?,)
        ''', (id_cliente, produto, quantidade, data, valor_total))
        conn.commit()
        print('Pedido inserido com sucesso!')
    except ValueError:
        print('-'*70)
        print('Erro: ID do cliente deve ser um número inteiro.')
        print('-'*70)
        
        
        
def consultar_pedidos():
    cursor.execute('''
    SELECT
        Clientes.nome, Clientes.email, Clientes.cidade, -- Campos da tabela clientes
        Pedidos.produto, Pedidos.quantidade, Pedidos.valor_total  -- Campos da tabela consultar_pedidos
    FROM
        Clientes     
    JOIN
        Pedidos ON Clientes.id_cliente = Pedidos.id_cliente
    ''')
    resultados = cursor.fetchall()
    
    
    tabela = PrettyTable(
        ['Nome', 'Email', 'Cidade', 'Produto', 'Quantidadde', 'Valor Total'])
    for linha in resultados:
        tabela.add_row(linha)
    print(tabela)
    
    
    
    
def alterar_pedido():
    try:
        
        id_pedido = int(input('Digite o ID do pedido que deseja alterar: '))
        
        
        cursor.execute(
            'SELECT * FROM Pedidos WHERE id_pedido = ?', (id_pedido,))
        pedido = cursor.fetchone()
        
        if not pedido:
            print('-'* 70)
            print(f'Erro: Pedido com ID {id_pedido} não encontrado!')
            print('-'*70)
            return
        
        
        print('-'*70)
        print('Dados atuais do pedido: ')
        print(f'Produto: {pedido[2]}')
        print(f'Quantidade: {pedido[3]}')
        print(f'Data: {pedido[4]}')
        print(f'Valor total: {pedido[5]}')
        print('-'*70)
        
        
        produto = input(
            'Digite o novo nome do produto (ou pressione Enter para manter o atual): ') or pedido[2]
        quantidade = input(
            'Digite a nova quantidade (ou pressione Enter para manter a atual): ') or pedido[3]
        data = input(
            'Digite a nova data (YYYY-MM-DD) (ou pressione Enter para manter a atual): ') or pedido[4]
        valor_total = input(
            'Digite o novo valor total (ou pressione Enter para manter o atual): ') or pedido[5]
        
        
        cursor.execute('''
        UPDATE Pedidos
        SET produto = ?, quantidade = ?, data = ?, valor_total = ?
        WHERE id_pedido = ?
        ''', (produto, int(quantidade), data, float(valor_total), id_pedido))
        conn.commit()
        print('Pedido atualizado com sucesso!')
    except ValueError:
        print(''*70)
        print('Erro: Entrada inválida.')
        print('-'*70)
        
        
while True:
    print('\nMenu:')
    print('1. Inserir Clientes')
    print('2. Inserir Pedidos')
    print('3. Consultar Pedidos')
    print('4. Alterar Pedidos')
    print('5. Sair')
    opcao = input('Escolha uma opção: ')
    
    if opcao =='1':
        inserir_cliente()
    elif opcao == '2':
        inserir_pedido()
    elif opcao == '3':
        consultar_pedidos()
    elif opcao == '4':
        alterar_pedido
    elif opcao == '5':
        print('Saindo ...')
        break
    else:
        print('-'*70)
        print('Opção inválida. Tente novamente.')
        print('-'*70)
        
        
        
conn.close()
        
        
        
        