# from dao.category_dao import CategoryDAO
# from dao.transaction_dao import TransactionDAO
# import json


# # Abre o arquivo JSON para leitura
# def main():
#     with open("/home/carlos/Downloads/sheetjson.json", "r", encoding="utf-8") as arquivo:
#         # Carrega o conteúdo do arquivo
#         dados = json.load(arquivo)
#     # Exibe os dados carregados
#     for transaction in dados:
#         with TransactionDAO() as dao:
#             with CategoryDAO() as category_dao:
#                 category = None
#                 if transaction["Categoria"]:
#                     category = category_dao.get_category_by_name(
#                         transaction["Categoria"]
#                     )
#                     if not category:
#                         category = category_dao.create_category(transaction["Categoria"])
#             dia, mes, ano = transaction["Data"].split("/")
#             dao.create_transaction(
#                 {
#                     "transaction_date": f"{ano}-{mes}-{dia}",
#                     "description": transaction["Descrição"],
#                     "transaction_value": float(transaction["Valor"]),
#                     "type": transaction["Tipo"],
#                     "category_id": category.id if category else None,
#                 }
#             )
