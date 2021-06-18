import re

Email = '''

Aviso de vencimento de fatura

Prezado(a) NOVA S R M ADMINISTRACAO DE RECURSOS E FINANCAS S/A,

Em anexo encontra-se a sua fatura/boleto para pagamento. Lembramos que sua fatura/boleto também foi postada para entrega pelos Correios. Você poderá efetuar o pagamento pelo boleto postado ou ainda pela versão digital anexa.

Caso já tenha recebido esta fatura/boleto anteriormente, ou já tenha efetuado o pagamento, favor desconsiderar este.

Boleto referente ao mês 07/2020, com vencimento em 21/07/2020 - Título nº 32007437 - Arquivo em anexo.

Cordialmente,

America Net

Este e-mail foi enviado pelo sistema automático da America Net. Favor não respondê-lo, por não ser um e-mail monitorado.  

'''

patternVenc = re.compile(r'vencimento em\s(\d\d.\d\d.\d\d\d\d)')
matches = patternVenc.finditer(Email)

patternBoleto = re.compile(r'referente ao mês\s(\d\d\/\d\d\d\d)')
matches2 = patternBoleto.finditer(Email)

patternNum = re.compile(r'Título nº\s([0-9]+)')
matches3 = patternNum.finditer(Email)

for match in matches:
    print(match.group(1))

for match in matches2:
    print(match.group(1))

for match in matches3:
    print(match.group(1))