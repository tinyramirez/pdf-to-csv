import os
import tabula
import pandas as pd
import numpy as np

dir_string = '/Users/Documents/PDFs/'
report = 'report.pdf'

initial_df= pd.read_csv(os.path.join(dir_string, 'report.csv'), dtype={
    'Sua cota': np.str,
    'Unidades': np.str,
    'recebidos': np.str,
    'Valor devido': np.str
})

def get_sua_cota(percentage):
    if percentage:
        return str(percentage) + "%"
    return ''

def get_money(money):
    if money:
        return 'RUS$ ' + str(money)
    return ''

initial_df = initial_df.rename({'Titulo & Compositores': 'Obra', 'Exploração': 'Territorio de Exploração',
                           'Renda': 'Tipo de Renda', 'catálogo': 'Número de catálogo',
                           'do período': 'Recebimentos do período', 'recebidos': 'Valores Recebidos',
                            'Sua cota': 'Sua Cota %', 'Valor devido': 'Valor Devido'}, axis=1)

final_df = initial_df[(initial_df['Número de catálogo'] != 'catálogo')]
final_df['Obra'] = final_df['Obra'].replace('De Sousa & Rezende', np.NaN)
final_df = final_df.fillna(method='ffill')
final_df = final_df[final_df['Fonte de Renda'].notna()]

final_df['Sua Cota %'] = final_df['Sua Cota %'].apply(lambda x: get_sua_cota(x))
final_df['Valores Recebidos'] = final_df['Valores Recebidos'].apply(lambda x: get_money(x))
final_df['Valor Devido'] = final_df['Valor Devido'].apply(lambda x: get_money(x))
 
final_df = final_df[['Obra','Territorio de Exploração', 'Fonte de Renda',
                    'Tipo de Renda', 'Unidades', 'Valores Recebidos',
                    'Sua Cota %', 'Valor Devido', 'Recebimentos do período']]

final_df['Fonte de Renda'] = final_df.groupby(['Obra','Territorio de Exploração',
                                      'Unidades', 'Valores Recebidos', 'Sua Cota %',
                                      'Valor Devido', 'Recebimentos do período'])['Fonte de Renda'].transform(lambda x: ' '.join(x))
final_df['Tipo de Renda'] = final_df.groupby(['Obra','Territorio de Exploração',
                                      'Unidades', 'Valores Recebidos', 'Sua Cota %',
                                      'Valor Devido', 'Recebimentos do período'])['Tipo de Renda'].transform(lambda x: ' '.join(x))

final_df = final_df[['Obra', 'Territorio de Exploração', 'Fonte de Renda', 'Tipo de Renda',
                  'Unidades', 'Valores Recebidos', 'Sua Cota %', 'Valor Devido', 'Recebimentos do período']].drop_duplicates()

final_df.to_csv(os.path.join(dir_string, 'report - Final.csv'), index=False)
print('DONE')
