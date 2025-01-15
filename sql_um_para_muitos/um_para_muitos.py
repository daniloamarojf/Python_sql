import sqlite3 # Biblioteca para trabalhar com bancos de dados SQlite
from prettytable import PrettyTable # Biblioteca para exibir tabelas formatadas
# importar o módulo pathlib para trabalar com caminhos relativos ou abstratos
from pathlib  import Path
import os


os.system('cls')
# Conexão com o banco de dados (arquivo será criado senão existir)

# Caminno relativo
db_path = Path('BD') / 'bd_rel_1_n.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Criação da tabela 'Clientes' (Tabela principal)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para o cliente
    nome TEXT NOR NULL,                           -- Nome do cliente
    email TEXT UNIQUE NOT NULL,                   -- Email único
    telefone TEXT,                                -- Telefone do cliente
    cidade TEXT                                   -- Cidade onde mora
)
''')

# Criação da tabela 'Pedidos' (Tabela relacionada)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para o pedido
    id_cliente INTEGER NOT NULL,                  -- Relacionamento com a tbela clientes
    produto TEXT NOT NULL,                        -- Nome do produto pedido
    quantidade INTEGER NOT NULL,                  -- Quantidade do produto
    data TEXT NOT NULL,                           -- Data do pedido
    valor_total REAL NOT NULL,                    -- Valor total do pedido
    FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente) -- Chave estrangeira
)
''')

# Função para verificar se um cliente existe no banco de dados


def cliente_existe(id_cliente):
    cursor.execute(
        'SELECT 1 FROM Clientes WHERE id_cliente = ?', (id_cliente,))
    
    return cursor.fetchone() is not None
    
# Função para inserir dados na tabela Clientes


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
    
# Função para inserir dados na tabela Pedidos    
    
    
def inserir_pedido():
    # listando os clientes
    cursor.execute(''' 
    SELECT * from clientes
    ''')
    resultados = cursor.fetchall()
    
    # Não posso fazer pedidos sem clientes
    if not resultados:
        print('-' *70)
        print('Nenhum cliente encontrado. Cadastre um cliente primeiro')
        print('-'* 70)
        return
    
    # Criar e formatar a tabela para exibição
    tabela = PrettyTable(['id_cliente', 'Nome', 'Email', 'Telefone', 'Cidade'])
    for linha in resultados:
        tabela.add_row(linha)
    print(tabela)
    
    try: 
        # Garantir que o ID seja um número inteiro
        id_cliente = int(input('Digite o ID do cliente: '))
        
        # Verificar se o cliente existe antes de prosseguir
        if not cliente_existe(id_cliente):
            print('-' * 70)
            print(f'Erro: Cliente com ID {id_cliente} não encontrado!')
            print('Por favor, cadastre o cliente primeiro.')
            print('-' * 70)
            # Retorna ao menu se o cliente não existir
            return
        
        # Solicitar os dados do pedido
        produto = input('Digite o nome do produto: ')
        quantidade = int(input('Digite a quantidade: '))
        # ISO 8601 (YYYY-MM-DD)
        data = input('Digite a data do pedido (YYYY-MM-DD): ')
        valor_total = float(input('Digite o valor total: '))
        
        # Inserindo o pedido no banco de dados
        cursor.execute(''' 
        INSERT INTO Pedidos (id_cliente, produto, quantidade, data, valor_total)
        VALUES (?,?,?,?,?)
        ''', (id_cliente, produto, quantidade, data, valor_total))
        conn.commit()
        print('Pedido inserido com sucesso!')
    except ValueError:
        print('-'*70)
        print('Erro: ID do cliente deve ser um número inteiro.')
        print('-'*70)
        
        
# Função para realizar uma consulta com JOIN e exibir resultados          
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
    
    # Criar e formatar a tabela para exibição
    tabela = PrettyTable(
        ['Nome', 'Email', 'Cidade', 'Produto', 'Quantidadde', 'Valor Total'])
    for linha in resultados:
        tabela.add_row(linha)
    print(tabela)
    
    
# Função para alterar Pedido 
# Função para alterar um pedido existente
def alterar_pedido():
    try:
        # Solicitar o ID do Pedido
        id_pedido = int(input('Digite o ID do pedido que deseja alterar: '))
        
        # Verificar se o pedido existe
        cursor.execute(
            'SELECT * FROM Pedidos WHERE id_pedido = ?', (id_pedido,))
        pedido = cursor.fetchone()
        
        if not pedido:
            print('-'* 70)
            print(f'Erro: Pedido com ID {id_pedido} não encontrado!')
            print('-'*70)
            return
        
        # Exibir os dados atuais do pedido
        print('-'*70)
        print('Dados atuais do pedido: ')
        print(f'Produto: {pedido[2]}')
        print(f'Quantidade: {pedido[3]}')
        print(f'Data: {pedido[4]}')
        print(f'Valor total: {pedido[5]}')
        print('-'*70)
        
        # Solicitar novos dados do pedido
        produto = input(
            'Digite o novo nome do produto (ou pressione Enter para manter o atual): ') or pedido[2]
        quantidade = input(
            'Digite a nova quantidade (ou pressione Enter para manter a atual): ') or pedido[3]
        data = input(
            'Digite a nova data (YYYY-MM-DD) (ou pressione Enter para manter a atual): ') or pedido[4]
        valor_total = input(
            'Digite o novo valor total (ou pressione Enter para manter o atual): ') or pedido[5]
        
        # Atualizar os dados do pedido
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
        
# Menu interativo        
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
        alterar_pedido()
    elif opcao == '5':
        print('Saindo ...')
        break
    else:
        print('-'*70)
        print('Opção inválida. Tente novamente.')
        print('-'*70)
        
        
# Fechar a conexão com o abnco de dados        
conn.close()
        
        
        
        