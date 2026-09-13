# DASHBOARD PREÇOS SAÚDE — Relacionamentos

Mapa visual + lista detalhada de relacionamentos entre tabelas.

---

## Diagrama

```
   ┌──────────────┐        N:1        ┌──────────────────────────┐
   │  Calendario  │◄──────────────────│ BPS_20_26_LourencoFLemos  │
   │   (dimensão) │  data_compra      │          (fato)           │
   └──────────────┘                   └──────────────────────────┘

   MEDIDAS (tabela de medidas, sem relacionamentos — hospeda só DAX)
```

---

## Tabela detalhada

| # | From | To | Cardinalidade | Direção | Ativo | Notas |
|---|---|---|---|---|---|---|
| 1 | `BPS_20_26_LourencoFLemos.data_compra` | `Calendario.Date` | N:1 | Single | ✓ | Único relacionamento "de negócio" do modelo |

> Além deste, existem 2 relacionamentos automáticos ligando `BPS_20_26_LourencoFLemos.data_insercao` e `Calendario.Date` a tabelas ocultas `LocalDateTable_*` (geradas pelo recurso Auto Date/Time). Eles foram **excluídos** desta tabela por não fazerem parte do modelo intencional — detalhes em [00 · Overview](00-overview.md).

---

## Análise rápida

O modelo tem uma estrutura mínima: uma fato (`BPS_20_26_LourencoFLemos`) e uma dimensão de tempo (`Calendario`), ligadas por um único relacionamento N:1 ativo e de sentido único (`data_compra` → `Calendario.Date`). Não há dimensões de instituição, fornecedor ou produto separadas — esses atributos vivem como colunas diretamente na tabela fato. A tabela `MEDIDAS` não participa de nenhum relacionamento, como esperado de uma tabela de medidas.

---