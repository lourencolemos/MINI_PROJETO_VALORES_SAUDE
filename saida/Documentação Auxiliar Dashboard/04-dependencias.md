# DASHBOARD PREÇOS SAÚDE — Dependências

Grafo de dependências entre medidas. Útil para entender o impacto de mudanças e priorizar refator.

---

## Árvores por medida-raiz

Medidas-raiz são as que não são usadas por nenhuma outra. Das 9 medidas, 5 são raízes; as outras 4 aparecem como dependências dentro dessas árvores.

### Variação de Preco Unitario
```
Variação de Preco Unitario
├─ Maior Preco Unitario
│  └─ BPS_20_26_LourencoFLemos[preco_unitario]
└─ Menor Preco Unitario
   └─ BPS_20_26_LourencoFLemos[preco_unitario]
```

### Preco Unitario Medio Ponderado
```
Preco Unitario Medio Ponderado
├─ Valor Total Comprado
│  └─ BPS_20_26_LourencoFLemos[preco_total]
└─ Quantidade Total Comprada
   └─ BPS_20_26_LourencoFLemos[qtd_itens_comprados]
```

### Demais raízes (sem dependências internas)
```
Quantidade de Compras Realizadas   → BPS_20_26_LourencoFLemos (linhas)
Quantidade de Instituicoes Compradoras → BPS_20_26_LourencoFLemos[cnpj_instituicao]
Quantidade de Fornecedores         → BPS_20_26_LourencoFLemos[cnpj_fornecedor]
```

---

## Reverse — quem depende das medidas-base

### Valor Total Comprado (base)

**Usada por:**
- `Preco Unitario Medio Ponderado`

**Implicação:** mudar `Valor Total Comprado` (ex.: trocar a coluna somada) afeta diretamente o KPI de preço médio ponderado.

### Quantidade Total Comprada (base)

**Usada por:**
- `Preco Unitario Medio Ponderado`

**Implicação:** mesma observação acima — qualquer alteração no critério de quantidade muda o preço médio ponderado.

### Maior Preco Unitario (base)

**Usada por:**
- `Variação de Preco Unitario`

**Implicação:** afeta só a medida de variação; não impacta os KPIs principais de valor/quantidade.

### Menor Preco Unitario (base)

**Usada por:**
- `Variação de Preco Unitario`

**Implicação:** mesma observação acima.

---

## Tabelas mais referenciadas

1. `BPS_20_26_LourencoFLemos` — referenciada por 9 de 9 medidas (100%). É o centro de gravidade do modelo.
2. `Calendario` — 0 medidas referenciam suas colunas diretamente; ela participa do modelo apenas via relacionamento (usada como eixo de filtro/eixo temporal nos visuais, não em DAX).

---

## Como usar essa info

- **Antes de mexer em `Valor Total Comprado` ou `Quantidade Total Comprada`**: você impacta o KPI de preço médio ponderado — confira o efeito antes de publicar.
- **Antes de mexer em `Menor`/`Maior Preco Unitario`**: impacto restrito à medida de variação, mais seguro para ajustar.
- **Para onboarding**: o modelo é enxuto — uma fato, uma dimensão de tempo e 9 medidas praticamente independentes entre si, exceto pelos dois pares acima.

---