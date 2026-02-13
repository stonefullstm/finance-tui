# main.py
from dao.category_dao import CategoryDAO
from dao.transaction_dao import TransactionDAO
from db.config import testar_conexao
import sys


def menu_interativo():
    """Menu interativo para operações"""
    category_dao = CategoryDAO()
    transaction_dao = TransactionDAO()

    try:
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE CATEGORIAS (Firebird-Driver)")
            print("="*50)
            print("1. Listar todas categorias")
            print("2. Buscar categoria por ID")
            print("3. Buscar categorias por nome")
            print("4. Criar nova categoria")
            print("5. Atualizar categoria")
            print("6. Remover categoria")
            print("7. Criar transação para categoria")
            print("8. Listar transações")
            print("0. Sair")
            print("-"*50)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                contatos = category_dao.get_all_categories()
                print(f"\n📋 Total: {len(contatos)} categorias")
                for c in contatos:
                    print(f"  [{c.id}] {c.name}")
            elif opcao == '4':
                print("\n➕ NOVA CATEGORIA")
                name = input("Nome: ")
                categoria = category_dao.create_category(name)
                if categoria:
                    print(f"✅ Categoria criada com ID {categoria.id}")
                else:
                    print("❌ Falha ao criar categoria")
            elif opcao == '7':
                print("\n➕ NOVA TRANSAÇÃO")
                category_id = int(input("ID da Categoria: "))
                description = input("Descrição: ")
                transaction_date = input("Data (YYYY-MM-DD): ")
                transaction_value = float(input("Valor: "))
                type = input("Tipo (income/expense): ")
                categoria = category_dao.get_category_by_id(category_id)
                if categoria:
                    transaction = transaction_dao.create_transaction(
                        {
                            "description": description,
                            "transaction_date": transaction_date,
                            "transaction_value": transaction_value,
                            "type": type,
                            "category_id": category_id
                        }
                    )
                    if transaction:
                        print(f"✅ Transação criada com ID {transaction.id}")
                    else:
                        print("❌ Falha ao criar transação")
                else:
                    print("❌ Categoria não encontrada")
            elif opcao == '8':
                transactions = transaction_dao.get_all_transactions()
                print(f"\n📋 Total de transações: {len(transactions)}")
                for t in transactions:
                    print(f"  [{t.id}] {t.description} - "
                          f"{t.transaction_date} - "
                          f"{t.transaction_value} - "
                          f"{t.type} - "
                          f"Categoria: {
                              t.category.name if t.category else 'None'}")
            elif opcao == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida!")
    finally:
        category_dao.close()
        transaction_dao.close()
        print("Conexão fechada.")


def main():
    print("Testando conexão com o banco de dados...")
    if not testar_conexao():
        print("Não foi possível estabelecer conexão. "
              "Verifique as configurações.")
        sys.exit(1)

    menu_interativo()


if __name__ == "__main__":
    main()
