# Relatório de Tratamento — BPS 2020-2026
Gerado em: 08/09/2026 19:54
Arquivos encontrados: ['2020.csv', '2021.csv', '2022.csv', '2023.csv', '2024.csv', '2025.csv', '2026.csv']

📄 Processando 2020.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 84819
  valores nulos/vazios encontrados em: {'unidade_fornecimento': np.int64(6), 'generico': np.int64(47684), 'registro_anvisa': np.int64(47684), 'capacidade': np.int64(53437), 'unidade_capacidade': unidade_capacidade    53437
unidade_capacidade        6
dtype: int64}
  linhas finais após tratamento: 84819

📄 Processando 2021.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 83622
  valores nulos/vazios encontrados em: {'nome_instituicao': np.int64(8), 'unidade_fornecimento': np.int64(4), 'generico': np.int64(45199), 'registro_anvisa': np.int64(45199), 'capacidade': np.int64(53401), 'unidade_capacidade': unidade_capacidade    53401
unidade_capacidade        4
dtype: int64}
  linhas finais após tratamento: 83622

📄 Processando 2022.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 88991
  valores nulos/vazios encontrados em: {'data_insercao': np.int64(120), 'unidade_fornecimento': np.int64(4), 'generico': np.int64(49013), 'registro_anvisa': np.int64(49013), 'capacidade': np.int64(57645), 'unidade_capacidade': unidade_capacidade    57645
unidade_capacidade        4
dtype: int64}
  linhas finais após tratamento: 88991

📄 Processando 2023.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 31992
  valores nulos/vazios encontrados em: {'nome_instituicao': np.int64(13), 'data_insercao': np.int64(716), 'generico': np.int64(14587), 'registro_anvisa': np.int64(14587), 'capacidade': np.int64(19821), 'unidade_capacidade': np.int64(19821)}
  linhas finais após tratamento: 31992

📄 Processando 2024.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 26258
  valores nulos/vazios encontrados em: {'nome_instituicao': np.int64(77), 'data_insercao': np.int64(1292), 'unidade_fornecimento': np.int64(3), 'generico': np.int64(8674), 'registro_anvisa': np.int64(8674), 'capacidade': np.int64(16708), 'unidade_capacidade': unidade_capacidade    16708
unidade_capacidade        3
dtype: int64}
  🔁 16 linha(s) totalmente duplicada(s) -> serão removidas
  linhas finais após tratamento: 26242

📄 Processando 2025.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 26215
  valores nulos/vazios encontrados em: {'nome_instituicao': np.int64(59), 'unidade_fornecimento': np.int64(8), 'generico': np.int64(6712), 'registro_anvisa': np.int64(6712), 'capacidade': np.int64(16539), 'unidade_capacidade': unidade_capacidade    16539
unidade_capacidade        8
dtype: int64}
  🔁 1 linha(s) totalmente duplicada(s) -> serão removidas
  linhas finais após tratamento: 26214

📄 Processando 2026.csv
  encoding detectado: utf-8 | separador: ';'
  linhas lidas: 819
  valores nulos/vazios encontrados em: {'generico': np.int64(168), 'registro_anvisa': np.int64(168), 'capacidade': np.int64(484), 'unidade_capacidade': np.int64(484)}
  🔁 2 linha(s) totalmente duplicada(s) -> serão removidas
  linhas finais após tratamento: 817

## Consolidação final
Total de linhas consolidadas: 342697
Total de colunas: 26
Colunas finais: ['ano_compra', 'nome_instituicao', 'esfera_instituicao', 'cnpj_instituicao', 'municipio_instituicao', 'uf', 'data_compra', 'data_insercao', 'codigo_catmat', 'descricao_catmat', 'unidade_fornecimento', 'generico', 'registro_anvisa', 'modalidade_compra', 'tipo_compra', 'capacidade', 'unidade_capacidade', 'unidade_capacidade', 'cnpj_fornecedor', 'fornecedor', 'cnpj_fabricante', 'fabricante', 'qtd_itens_comprados', 'preco_unitario', 'preco_total', 'arquivo_origem']

✅ Base consolidada salva em: ./saida\BPS_20_26_LourencoFLemos.csv