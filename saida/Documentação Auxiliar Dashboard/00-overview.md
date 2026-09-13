# DASHBOARD PREÇOS SAÚDE — Overview

> **Modelo de compras públicas de saúde (BPS 2020–2026) com KPIs de valor, volume e dispersão de preço unitário.**
> Documentação gerada por Claude + `/pbi-doc` em 13 set 2026

**Arquivo:** `DASHBOARD PREÇOS SAÚDE.SemanticModel`

---

## Métricas

| Métrica | Valor |
|---|---|
| Tabelas reais | **3** (excluindo auto-date geradas) |
| Medidas | **9** |
| Relacionamentos | **1** (real) — mais 2 auto-gerados por Auto Date/Time, ver aviso abaixo |
| Colunas totais | **36** |
| Tamanho do modelo | **~28 KB** (soma dos arquivos `.tmdl`) |

---

## Inventário de tabelas

| Tabela | Tipo | Colunas | Medidas | Source |
|---|---|---|---|---|
| `BPS_20_26_LourencoFLemos` | Fato | 26 | 0 | CSV local, modo import |
| `Calendario` | Dimensão | 10 | 0 | Calculada (DAX `CALENDAR` + `ADDCOLUMNS`) |
| `MEDIDAS` | Tabela de medidas | 0 | 9 | Tabela vazia, só hospeda DAX |

> **Tipo:** Fato (1+ por modelo) · Dimensão (descreve fato) · Medidas (só hospeda DAX) · Aux (parameter table, calculated, etc.)

---

## Fontes de dados

- **CSV consolidado (BPS 2020–2026)** — `BPS_20_26_LourencoFLemos`, importado via `Csv.Document`, delimitador `;`, 26 colunas, encoding UTF-8 (65001).
- **Calendário customizado** — tabela `Calendario` gerada inteiramente por DAX (`CALENDAR(DATE(2020,1,1), DATE(2026,12,31))` + colunas derivadas de ano/mês/trimestre/dia), sem fonte externa.

> ⚠️ **Path pessoal detectado.** A partição de `BPS_20_26_LourencoFLemos` referencia um caminho local fixo:
> `C:\Users\Usuário\Downloads\MINI PROJETO PREÇOS SAÚDE\saida\BPS_20_26_LourencoFLemos.csv`
> Isso significa que o `.pbip` só atualiza em máquinas com esse caminho exato. Para publicar/entregar o projeto, considere trocar por um **parâmetro de pasta** (Power Query → Gerenciar Parâmetros) antes de subir ao GitHub, ou deixar claro no README que o caminho precisa ser ajustado por quem for reproduzir.
>
> ⚠️ **Dois padrões de data coexistindo.** O modelo tem `Auto Date/Time` ligado, o que gerou 2 tabelas ocultas (`LocalDateTable_*`) — uma para `BPS_20_26_LourencoFLemos[data_insercao]` e outra para `Calendario[Date]`. Ao mesmo tempo, existe uma tabela `Calendario` explícita e customizada, usada no relacionamento real com `BPS_20_26_LourencoFLemos[data_compra]`. Ou seja: `data_compra` usa o calendário customizado (bom para relatórios), enquanto `data_insercao` usa a hierarquia automática oculta do Power BI. Essas tabelas ocultas foram **excluídas** desta documentação (não fazem parte do modelo intencional) — para avaliar se isso é um problema de modelagem, rode uma revisão de qualidade do modelo.

---

## Configurações relevantes do modelo

- **Idioma/cultura:** pt-BR
- **Compatibility level:** 1606
- **Auto Date/Time:** Ligado (`__PBI_TimeIntelligenceEnabled = 1`) — gera as 2 tabelas ocultas mencionadas acima
- **Modo de armazenamento:** Import, em todas as tabelas
- **Ordem de query:** `BPS_20_26_LourencoFLemos` → `MEDIDAS`

---