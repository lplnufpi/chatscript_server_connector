import dataset
import sys

db = dataset.connect('sqlite:///produtos.db')
table = db['produto']
rows = table.find(usuario=sys.argv[1])

atrasados = [
    '*{prod}* comprado em {purchased}, data de entrega prevista para {delivery}, '
    'última localização em {loc})'.format(
        prod=row['nome'],
        purchased=row['data_compra'],
        delivery=row['previsao_entrega'],
        loc=row['localizacao']
    )
    for row in rows if row['status'] != 'Entregue'
]
entregues = [row['nome'] for row in rows if row['status'] == 'Entregue']

if atrasados:
    title = (
        'Encontrei os seguintes produtos no seu histórico com entrega '
        'em atraso: {}. Desculpe o incômodo, nossa equipe está '
        'trabalhando para que os produtos sejam entregues o mais '
        'rápido possível.'
    ).format('; '.join(atrasados))
elif entregues:
    title = 'Não existem produtos com entrega em atraso no seu histórico.'
else:
    title = 'Não foi encontrado nenhum produto no seu histórico.'

print(title)
