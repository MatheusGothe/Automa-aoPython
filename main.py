import pandas as pd
import requests
from datetime import datetime


df = pd.read_excel('faturamentoOriginal.xlsx')

# Converter a coluna 'Data' para o formato datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')

# Função para obter a taxa de câmbio para uma data específica
def get_exchange_rate(currency, date):
    start_date = date.strftime('%Y%m%d')
    end_date = start_date  # Mesma data para obter a taxa específica do dia
    url = f'https://economia.awesomeapi.com.br/json/daily/{currency}?start_date={start_date}&end_date={end_date}'
    
    response = requests.get(url)
    data = response.json()
    print('oi')
    if response.status_code == 200 and len(data) > 0:
        return float(data[0]['bid'])
    else:
        return None

# Listas para armazenar os dados das novas colunas
exchange_rate_usd = []
exchange_rate_eur = []
revenue_usd = []
revenue_eur = []

# Obter as taxas de câmbio e calcular os faturamentos convertidos
for index, row in df.wg():
    date = row['Data']
    revenue_brl = row['Faturamento em real']
    
    # Obter as taxas de câmbio históricas
    rate_usd = get_exchange_rate('USD-BRL', date)
    rate_eur = get_exchange_rate('EUR-BRL', date)

    # Arredondar as taxas de câmbio se estiverem disponíveis
    rate_usd_rounded = round(rate_usd, 2) if rate_usd else None
    rate_eur_rounded = round(rate_eur, 2) if rate_eur else None
 
    # Calcular os faturamentos convertidos
    # Calcular os faturamentos convertidos
    revenue_in_usd = round(revenue_brl * rate_usd_rounded, 2) if rate_usd_rounded else None
    revenue_in_eur = round(revenue_brl * rate_eur_rounded, 2) if rate_eur_rounded else None
    
    # Adicionar os dados às listas
    exchange_rate_usd.append(round(rate_usd, 2) if rate_usd else None)
    exchange_rate_eur.append(round(rate_eur, 2) if rate_eur else None)
    revenue_usd.append(revenue_in_usd)
    revenue_eur.append(revenue_in_eur)

# Adicionar as novas colunas ao DataFrame
df['Taxa de Câmbio (USD)'] = exchange_rate_usd
df['Taxa de Câmbio (EUR)'] = exchange_rate_eur
df['Faturamento em USD'] = revenue_usd
df['Faturamento em EUR'] = revenue_eur

# Salvar o DataFrame atualizado em um novo arquivo .xlsx
output_file_path = 'arquivo_atualizado.xlsx'
df.to_excel(output_file_path, index=False)

print('Arquivo atualizado salvo com sucesso!')
