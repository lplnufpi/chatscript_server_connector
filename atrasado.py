import dataset
import sys

db = dataset.connect('sqlite:///produtos.db')
table = db['produto']
# rows = table.find(usuario=sys.argv[1])
rows = [r for r in table.find(usuario=0)]

atrasados = [
    '*{prod}* comprado em {purchased} (com data de entrega prevista para'
    ' {delivery} e última localização em {loc})'.format(
        prod=row['nome'],
        purchased=row['data_compra'],
        delivery=row['previsao_entrega'],
        loc=row['localizacao']
    )
    for row in rows if row['status'] == 'Atrasado'
]

entregues = [
    '*{prod}* comprado em {purchased} (com entrega concluída em {delivery})'.format(
        prod=row['nome'],
        purchased=row['data_compra'],
        delivery=row['previsao_entrega'],
        loc=row['localizacao']
    )
    for row in rows if row['status'] == 'Entregue'
]
normal = [
    '*{prod}* comprado em {purchased} (que deverá chegar em'
    ' {delivery} e última localização em {loc})'.format(
        prod=row['nome'],
        purchased=row['data_compra'],
        delivery=row['previsao_entrega'],
        loc=row['localizacao']
    )
    for row in rows if row['status'] == 'A caminho'
]

title = (
    'O produto {atrasado} está com entrega *em atraso*, lamentamos o ocorrido '
    'e estamos trabalhando para concluír rapidamente a entrega. \n\nTambém '
    'encontrei o produto {normal}, e o produto {entregue}.'
).format(
    atrasado=''.join(atrasados),
    normal=''.join(normal),
    entregue=''.join(entregues)
)

# if atrasados:
#     title = title + (
#         'Produtos no seu histórico entrega *em atraso*: {}. Desculpe o '
#         'incômodo, nossa equipe está trabalhando para que os produtos sejam '
#         'entregues o mais rápido possível.'
#     ).format('; '.join(atrasados))
# if normal:
#     title = title + (
#         'Os seguintes produtos no seu histórico com entrega '
#         '*em andamento*: {}. Desculpe o incômodo, nossa equipe está '
#         'trabalhando para que os produtos sejam entregues o mais '
#         'rápido possível.'
#     )
# if entregues:
#     title = title + 'Não existem produtos com entrega em atraso no seu histórico.'
# if not rows:
#     title = 'Não foi encontrado nenhum produto no seu histórico.'

print(title)
