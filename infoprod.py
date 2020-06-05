import dataset
import sys

db = dataset.connect('sqlite:///produtos.db')

nome = ' '.join(sys.argv[1:]).strip()
nome_lower = nome.lower()
result = db.query(
    'SELECT * FROM produto WHERE LOWER(nome) LIKE "%{}%"'.format(nome_lower)
)

if not result:
    print('O produto "{}" não foi encontrado'.format(nome))
else:
    for row in result:
        text = (
            'O produto "{prod}" foi comprado em {purchased}, tem data de '
            'entrega prevista para {delivery}, e encontra-se atualmente '
            'em {loc}.'
        ).format(
            prod=row['nome'],
            purchased=row['data_compra'],
            delivery=row['previsao_entrega'],
            loc=row['localizacao']
        )
        print(text)
