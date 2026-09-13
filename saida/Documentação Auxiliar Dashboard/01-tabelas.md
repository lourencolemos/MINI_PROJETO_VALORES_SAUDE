# DASHBOARD PREÇOS SAÚDE — Tabelas

Catálogo de tabelas do modelo. Cada uma com descrição, granularidade, colunas tipadas e source M resumido.

---

## BPS_20_26_LourencoFLemos

> Base histórica consolidada de compras públicas/privadas de medicamentos e dispositivos médicos, 2020–2026.
> **Tipo:** Fato · **Origem:** CSV local (`BPS_20_26_LourencoFLemos.csv`) via `Csv.Document`

### Descrição
Tabela fato do modelo — cada linha representa um registro de compra do Banco de Preços em Saúde, já consolidado a partir dos 7 arquivos anuais (2020 a 2026). Traz quem comprou (instituição), o quê (item CATMAT), de quem (fornecedor/fabricante), quando (datas de compra e inserção) e por quanto (preço unitário/total, quantidade).

### Granularidade
1 linha = 1 registro de compra de um item específico, em uma instituição, em uma data.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `ano_compra` | int64 | Atributo temporal | Redundante com `data_compra`, útil para filtro rápido |
| `nome_instituicao` | string | Atributo | Instituição compradora |
| `esfera_instituicao` | string | Atributo | Ex.: federal/estadual/municipal/privada |
| `cnpj_instituicao` | int64 | Chave de agrupamento | Usado nas medidas de contagem distinta de instituições |
| `municipio_instituicao` | string | Atributo geográfico | — |
| `uf` | string | Atributo geográfico | — |
| `data_compra` | dateTime | Chave estrangeira → `Calendario.Date` | Relacionamento ativo real do modelo |
| `data_insercao` | dateTime | Atributo temporal | Relacionada à tabela de data automática oculta (Auto Date/Time), não à `Calendario` |
| `codigo_catmat` | int64 | Chave de item | Código padronizado do produto |
| `descricao_catmat` | string | Atributo | Descrição do item |
| `unidade_fornecimento` | string | Atributo | Forma de apresentação (comprimido, frasco, etc.) |
| `generico` | string | Atributo | Indicador de genérico |
| `registro_anvisa` | int64 | Atributo | Registro sanitário |
| `modalidade_compra` | string | Atributo | Ex.: pregão, dispensa |
| `tipo_compra` | string | Atributo | — |
| `capacidade` | int64 | Atributo | Capacidade da embalagem |
| `unidade_capacidade` | string | Atributo | Unidade referente a `capacidade` |
| `unidade_fornecimento_capacidade` | string | Atributo | Renomeada no Power Query a partir de `unidade_capacidade_1` (discrepância de nome tratada na etapa "Colunas Renomeadas" do M) |
| `cnpj_fornecedor` | int64 | Chave de agrupamento | Usado na medida de contagem distinta de fornecedores |
| `fornecedor` | string | Atributo | — |
| `cnpj_fabricante` | int64 | Atributo | — |
| `fabricante` | string | Atributo | — |
| `qtd_itens_comprados` | int64 | Métrica | Base das medidas de quantidade e preço médio ponderado |
| `preco_unitario` | double | Métrica | Formatado como moeda (`es-US` no hint, exibido como `$`) |
| `preco_total` | double | Métrica | `preco_unitario × qtd_itens_comprados` |
| `arquivo_origem` | string | Atributo de auditoria | Nome do CSV anual de origem de cada linha — útil para rastrear discrepâncias por ano |

### Source M (resumo)
```m
let
    Fonte = Csv.Document(File.Contents("...BPS_20_26_LourencoFLemos.csv"),
             [Delimiter=";", Columns=26, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Cabeçalhos Promovidos" = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    #"Tipo Alterado" = Table.TransformColumnTypes(#"Cabeçalhos Promovidos", {...26 tipos...}),
    #"Colunas Renomeadas" = Table.RenameColumns(#"Tipo Alterado",
             {{"unidade_capacidade_1", "unidade_fornecimento_capacidade"}})
in
    #"Colunas Renomeadas"
```
Lê o CSV consolidado com separador `;` e encoding UTF-8, promove a primeira linha a cabeçalho, tipa as 26 colunas explicitamente e corrige um nome de coluna duplicado (`unidade_capacidade_1` → `unidade_fornecimento_capacidade`), evidência de que o CSV de origem tinha duas colunas com nomes muito parecidos.

---

## Calendario

> Dimensão de tempo customizada, cobrindo todo o período de 2020 a 2026.
> **Tipo:** Dimensão · **Origem:** Calculada por DAX (não vem de arquivo externo)

### Descrição
Tabela calendário gerada por fórmula DAX, criada para servir como dimensão de tempo "oficial" do modelo — é ela que se relaciona com `data_compra`, permitindo montar a análise de evolução anual pedida no desafio.

### Granularidade
1 linha = 1 dia, de 01/01/2020 a 31/12/2026.

### Colunas

| Coluna | Tipo | Papel | Notas |
|---|---|---|---|
| `Date` | date | Chave primária | Relaciona com `BPS_20_26_LourencoFLemos.data_compra` |
| `Ano` | int (inferido) | Atributo | `YEAR([Date])` |
| `MesNumero` | int (inferido) | Atributo | `MONTH([Date])`, usado para ordenar `Mes` |
| `Mes` | string (inferido) | Atributo | Nome do mês por extenso |
| `MesAno` | string (inferido) | Atributo | `MM/yyyy` |
| `Trimestre` | string (inferido) | Atributo | `T1`–`T4` |
| `Dia` | int (inferido) | Atributo | `DAY([Date])` |
| `DiaSemana` | string (inferido) | Atributo | Nome do dia da semana |
| `NumeroSemana` | int (inferido) | Atributo | `WEEKNUM([Date])` |
| `AnoMes` | int (inferido) | Atributo | `AAAAMM`, útil para ordenação numérica |

### Source M (resumo)
```dax
ADDCOLUMNS(
    CALENDAR(DATE(2020,1,1), DATE(2026,12,31)),
    "Ano", YEAR([Date]),
    "MesNumero", MONTH([Date]),
    "Mes", FORMAT([Date], "MMMM"),
    "MesAno", FORMAT([Date], "MM/yyyy"),
    "Trimestre", "T" & FORMAT([Date], "Q"),
    "Dia", DAY([Date]),
    "DiaSemana", FORMAT([Date], "dddd"),
    "NumeroSemana", WEEKNUM([Date]),
    "AnoMes", YEAR([Date]) * 100 + MONTH([Date])
)
```

> **Observação:** nenhuma medida do modelo referencia diretamente as colunas de `Calendario` (nem em `filter context` explícito) — ela é usada apenas via relacionamento com `data_compra` para permitir os filtros/eixos temporais nos visuais do relatório.

---

## MEDIDAS

> Tabela "prateleira" sem dados próprios, criada só para organizar as 9 medidas DAX do modelo.
> **Tipo:** Tabela de medidas · **Origem:** Tabela vazia gerada via M (`Table.FromRows` de uma lista serializada, depois removida)

### Descrição
Padrão comum em modelos Power BI: uma tabela sem colunas visíveis, cujo único propósito é hospedar medidas para deixá-las separadas das tabelas de dados no painel de campos.

### Granularidade
Não aplicável — tabela sem linhas de dados relevantes (0 colunas úteis).

### Medidas hospedadas
Todas as 9 medidas do modelo, sem `displayFolder` definido → agrupadas como "Sem pasta" em [02 · Medidas](02-medidas.md).

### Source M (resumo)
```m
let
    Fonte = Table.FromRows(Json.Document(Binary.Decompress(...)), ...),
    #"Tipo Alterado" = Table.TransformColumnTypes(Fonte, {{"Coluna 1", type text}}),
    #"Colunas Removidas" = Table.RemoveColumns(#"Tipo Alterado", {"Coluna 1"})
in
    #"Colunas Removidas"
```
Cria uma tabela vazia (remove a única coluna logo em seguida) — comportamento padrão do Power BI Desktop quando você clica em "Nova tabela de medidas".

---

*Tabelas `LocalDateTable_*` e `DateTableTemplate_*` (auto-geradas pelo Auto Date/Time) foram excluídas deste catálogo — ver aviso em [00 · Overview](00-overview.md).*