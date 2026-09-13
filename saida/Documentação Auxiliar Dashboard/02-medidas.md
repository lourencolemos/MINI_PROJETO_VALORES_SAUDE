# DASHBOARD PREÇOS SAÚDE — Medidas

Catálogo de todas as medidas DAX do modelo, hospedadas na tabela `MEDIDAS`. Nenhuma tem `displayFolder` definido, então as 9 aparecem em um único grupo.

---

## Sem pasta

9 medidas · cobrem os 6 KPIs obrigatórios do desafio (valor total, quantidade total, número de registros, instituições, fornecedores, preço médio ponderado) mais 3 medidas de apoio para análise de dispersão de preço (mínimo, máximo, variação).

### Valor Total Comprado

`MEDIDAS.'Valor Total Comprado'` · formato moeda `R$ #,0.00`

**O que faz:**
Soma o valor total gasto em todas as compras do filtro atual — é o KPI "Valor total registrado" pedido no desafio.

**DAX:**
```dax
Valor Total Comprado = SUM(BPS_20_26_LourencoFLemos[preco_total])
```

**Como funciona:**
Soma direta da coluna `preco_total`, já pré-calculada na base (`preco_unitario × qtd_itens_comprados` por linha). Não há `CALCULATE` nem modificador de filtro — respeita o contexto de filtro vindo dos slicers e da tabela do visual.

**Usa:** `BPS_20_26_LourencoFLemos[preco_total]`
**É usada por:** `Preco Unitario Medio Ponderado`

---

### Quantidade Total Comprada

`MEDIDAS.'Quantidade Total Comprada'` · formato `#,0.00`

**O que faz:**
Soma a quantidade de itens comprados — KPI "Quantidade total de itens comprados".

**DAX:**
```dax
Quantidade Total Comprada = SUM(BPS_20_26_LourencoFLemos[qtd_itens_comprados])
```

**Como funciona:**
Soma direta, mesma lógica da medida anterior.

**Usa:** `BPS_20_26_LourencoFLemos[qtd_itens_comprados]`
**É usada por:** `Preco Unitario Medio Ponderado`

---

### Quantidade de Compras Realizadas

`MEDIDAS.'Quantidade de Compras Realizadas'` · formato inteiro

**O que faz:**
Conta quantos registros de compra existem no filtro atual — KPI "Número de registros de compra".

**DAX:**
```dax
Quantidade de Compras Realizadas = COUNTROWS(BPS_20_26_LourencoFLemos)
```

**Como funciona:**
`COUNTROWS` conta as linhas visíveis da tabela fato sob o contexto de filtro corrente — não distingue duplicidade nem agrega nenhuma coluna, só conta registros.

**Usa:** `BPS_20_26_LourencoFLemos` (linhas)
**É usada por:** nenhuma outra medida (raiz)

---

### Quantidade de Instituicoes Compradoras

`MEDIDAS.'Quantidade de Instituicoes Compradoras'` · formato inteiro

**O que faz:**
Conta quantas instituições diferentes aparecem nas compras filtradas — KPI "Instituições compradoras".

**DAX:**
```dax
Quantidade de Instituicoes Compradoras = DISTINCTCOUNT(BPS_20_26_LourencoFLemos[cnpj_instituicao])
```

**Como funciona:**
`DISTINCTCOUNT` conta valores únicos de `cnpj_instituicao`. Usar o CNPJ (em vez do nome) é a escolha correta aqui, pois evita contar duas vezes instituições com nome escrito de forma diferente entre anos.

**Usa:** `BPS_20_26_LourencoFLemos[cnpj_instituicao]`
**É usada por:** nenhuma outra medida (raiz)

---

### Quantidade de Fornecedores

`MEDIDAS.'Quantidade de Fornecedores'` · formato inteiro

**O que faz:**
Conta fornecedores distintos — KPI "Fornecedores".

**DAX:**
```dax
Quantidade de Fornecedores = DISTINCTCOUNT(BPS_20_26_LourencoFLemos[cnpj_fornecedor])
```

**Como funciona:**
Mesma lógica da medida anterior, aplicada a `cnpj_fornecedor`.

**Usa:** `BPS_20_26_LourencoFLemos[cnpj_fornecedor]`
**É usada por:** nenhuma outra medida (raiz)

---

### Menor Preco Unitario

`MEDIDAS.'Menor Preco Unitario'` · formato moeda

**O que faz:**
Retorna o menor preço unitário encontrado no filtro atual — usada como apoio para calcular a dispersão de preço.

**DAX:**
```dax
Menor Preco Unitario = MIN(BPS_20_26_LourencoFLemos[preco_unitario])
```

**Como funciona:**
`MIN` percorre a coluna `preco_unitario` sob o contexto de filtro e retorna o menor valor — útil combinada com um filtro de item (`codigo_catmat`) para achar o menor preço pago por aquele item específico.

**Usa:** `BPS_20_26_LourencoFLemos[preco_unitario]`
**É usada por:** `Variação de Preco Unitario`

---

### Maior Preco Unitario

`MEDIDAS.'Maior Preco Unitario'` · formato moeda

**O que faz:**
Retorna o maior preço unitário no filtro atual — par da medida anterior.

**DAX:**
```dax
Maior Preco Unitario = MAX(BPS_20_26_LourencoFLemos[preco_unitario])
```

**Como funciona:**
`MAX` equivalente ao `MIN` acima, na direção oposta.

**Usa:** `BPS_20_26_LourencoFLemos[preco_unitario]`
**É usada por:** `Variação de Preco Unitario`

---

### Variação de Preco Unitario

`MEDIDAS.'Variação de Preco Unitario'` · formato moeda

**O que faz:**
Mostra a diferença entre o maior e o menor preço unitário pago pelo mesmo item/filtro — evidencia dispersão de preço, ponto central da Sprint 5 do desafio.

**DAX:**
```dax
Variação de Preco Unitario =
[Maior Preco Unitario] - [Menor Preco Unitario]
```

**Como funciona:**
Subtração simples entre duas outras medidas. Não tem `CALCULATE`, então herda o mesmo contexto de filtro de ambas — funciona melhor quando o visual já está filtrado por um `codigo_catmat` específico; sem esse filtro, compara o menor/maior preço entre itens completamente diferentes, o que tem pouco significado prático (vale registrar essa ressalva no README, seção de limitações).

**Usa:** `Maior Preco Unitario`, `Menor Preco Unitario`
**É usada por:** nenhuma outra medida (raiz)

---

### Preco Unitario Medio Ponderado

`MEDIDAS.'Preco Unitario Medio Ponderado'` · formato moeda

**O que faz:**
Calcula o preço médio ponderado pela quantidade — o KPI "Preço unitário médio ponderado" pedido no desafio, e a forma correta de calcular esse indicador (em vez de tirar a média simples dos preços unitários).

**DAX:**
```dax
Preco Unitario Medio Ponderado =
DIVIDE([Valor Total Comprado], [Quantidade Total Comprada], 0)
```

**Como funciona:**
`DIVIDE` faz `Valor Total Comprado ÷ Quantidade Total Comprada`, com `0` como resultado alternativo caso o denominador seja zero (evita erro de divisão por zero quando o filtro não retorna nenhuma linha). Como ambas as medidas usadas somam antes de dividir, o resultado é ponderado pela quantidade — exatamente o que o enunciado pede, com a ressalva de que ele "deve ser interpretado com cautela quando os filtros incluem produtos diferentes".

**Usa:** `Valor Total Comprado`, `Quantidade Total Comprada`
**É usada por:** nenhuma outra medida (raiz)

---