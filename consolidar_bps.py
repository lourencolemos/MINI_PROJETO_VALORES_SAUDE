"""
consolidar_bps.py
==================
Padroniza, trata e concatena os arquivos anuais do Banco de Preços em Saúde (BPS)
de 2020 a 2026 em um único dataset histórico.

"""

import pandas as pd
import numpy as np
import re
import unicodedata
import glob
import os
from datetime import datetime

# ============================== CONFIGURAÇÃO ==============================
PASTA_ENTRADA = "./dados_brutos"        # pasta com os 7 csv baixados do portal
PASTA_SAIDA = "./saida"                 # onde salvar os arquivos finais
NOME_ALUNO = "LourencoFLemos"              # sem espaços/acentos, ex: "JoaoSilva"
ANOS_ESPERADOS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
# ============================================================================

os.makedirs(PASTA_SAIDA, exist_ok=True)
log_linhas = []


def log(msg):
    print(msg)
    log_linhas.append(msg)


def normalizar_texto(s):
    """minusculo, sem acento, sem pontuação -> para comparar nomes de coluna"""
    s = str(s).strip().lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("utf-8")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


# Dicionário de colunas oficiais do BPS (conforme dicionário de dados do Ministério
# da Saúde) -> lista de "apelidos" normalizados que podem aparecer nos arquivos brutos.
MAPA_COLUNAS = {
    "ano_compra":            ["ano_compra", "ano_da_compra", "ano"],
    "nome_instituicao":      ["nome_instituicao", "instituicao", "nome_da_instituicao"],
    "esfera_instituicao":    ["esfera_instituicao", "esfera", "esfera_da_instituicao"],
    "cnpj_instituicao":      ["cnpj_instituicao", "cnpj_da_instituicao"],
    "municipio_instituicao": ["municipio_instituicao", "municipio", "municipio_da_instituicao"],
    "uf":                    ["uf", "sigla_uf", "estado", "unidade_federativa"],
    "data_compra":           ["compra", "data_compra", "data_da_compra"],
    "data_insercao":         ["insercao", "data_insercao", "data_de_insercao"],
    "codigo_catmat":         ["codigo_br", "catmat", "codigo_catmat", "codigo_br_catmat"],
    "descricao_catmat":      ["descricao_catmat", "descricao", "descricao_do_item"],
    "unidade_fornecimento":  ["unidade_de_fornecimento", "unidade_fornecimento"],
    "generico":              ["generico"],
    "registro_anvisa":       ["anvisa", "informacoes_gerais_anvisa", "codigo_cmed", "registro_anvisa"],
    "modalidade_compra":     ["modalidade_da_compra", "modalidade_compra", "modalidade"],
    "tipo_compra":           ["tipo_de_compra", "tipo_compra"],
    "capacidade":            ["capacidade"],
    "unidade_capacidade":    ["unidade_de_fornecimento_capacidade", "unidade_fornecimento_capacidade", "unidade_medida_capacidade", "unidade_capacidade", "unidade_medida"],
    "cnpj_fornecedor":       ["cnpj_fornecedor"],
    "fornecedor":            ["fornecedor"],
    "cnpj_fabricante":       ["cnpj_fabricante"],
    "fabricante":            ["fabricante"],
    "qtd_itens_comprados":   ["qtd_itens_comprados", "quantidade", "qtd_itens", "quantidade_comprada"],
    "preco_unitario":        ["preco_unitario"],
    "preco_total":           ["preco_total", "valor_total"],
}

# inverte o dicionário para lookup rápido: apelido_normalizado -> nome_canonico
APELIDO_PARA_CANONICO = {}
for canonico, apelidos in MAPA_COLUNAS.items():
    for apelido in apelidos:
        APELIDO_PARA_CANONICO[apelido] = canonico


def detectar_encoding_e_separador(caminho):
    """Tenta abrir o csv com combinações comuns de encoding/separador usadas
    pelo governo (utf-8/latin1, vírgula/ponto-e-vírgula) e retorna a que funciona."""
    tentativas = [
        ("utf-8", ";"), ("latin1", ";"), ("cp1252", ";"),
        ("utf-8", ","), ("latin1", ","),
    ]
    for enc, sep in tentativas:
        try:
            df = pd.read_csv(caminho, encoding=enc, sep=sep, nrows=5, low_memory=False)
            if df.shape[1] > 1:  # se leu só 1 coluna, o separador provavelmente está errado
                return enc, sep
        except Exception:
            continue
    raise ValueError(f"Não consegui detectar encoding/separador para {caminho}")


def extrair_ano_do_nome(caminho):
    m = re.search(r"(20\d{2})", os.path.basename(caminho))
    return int(m.group(1)) if m else None


def mapear_colunas(df, nome_arquivo):
    """Renomeia colunas reconhecidas para o nome canônico. Reporta as não reconhecidas."""
    renomear = {}
    nao_reconhecidas = []
    for col_original in df.columns:
        chave = normalizar_texto(col_original)
        if chave in APELIDO_PARA_CANONICO:
            renomear[col_original] = APELIDO_PARA_CANONICO[chave]
        else:
            nao_reconhecidas.append(col_original)
    df = df.rename(columns=renomear)
    if nao_reconhecidas:
        log(f"  ⚠️  Colunas não mapeadas em {nome_arquivo}: {nao_reconhecidas}")
        log("      -> Revise o MAPA_COLUNAS no script e adicione o apelido correto, "
            "ou documente como coluna descartada no README.")
    return df


def limpar_valor_monetario(serie):
    """Converte string tipo '1.234,56' ou '1234.56' em float."""
    def conv(v):
        if pd.isna(v):
            return np.nan
        v = str(v).strip()
        v = v.replace("R$", "").replace(" ", "")
        # formato brasileiro: milhar com ponto, decimal com vírgula
        if re.match(r"^-?\d{1,3}(\.\d{3})*,\d+$", v):
            v = v.replace(".", "").replace(",", ".")
        elif "," in v and "." not in v:
            v = v.replace(",", ".")
        try:
            return float(v)
        except ValueError:
            return np.nan
    return serie.apply(conv)


def limpar_quantidade(serie):
    return limpar_valor_monetario(serie)  # mesma lógica de separador BR


def processar_arquivo(caminho):
    nome_arquivo = os.path.basename(caminho)
    log(f"\n📄 Processando {nome_arquivo}")

    enc, sep = detectar_encoding_e_separador(caminho)
    log(f"  encoding detectado: {enc} | separador: '{sep}'")

    df = pd.read_csv(caminho, encoding=enc, sep=sep, low_memory=False)
    linhas_originais = len(df)
    log(f"  linhas lidas: {linhas_originais}")

    df = mapear_colunas(df, nome_arquivo)

    ano_arquivo = extrair_ano_do_nome(caminho)
    if "ano_compra" not in df.columns and ano_arquivo:
        df["ano_compra"] = ano_arquivo
        log(f"  coluna 'ano_compra' ausente -> preenchida com o ano do nome do arquivo ({ano_arquivo})")
    elif "ano_compra" in df.columns and ano_arquivo:
        # sinaliza divergência entre o ano do arquivo e o valor da coluna
        divergentes = df[~df["ano_compra"].astype(str).str.strip().eq(str(ano_arquivo))]
        if len(divergentes) > 0:
            log(f"  ⚠️  {len(divergentes)} linha(s) com 'ano_compra' diferente do ano do arquivo ({ano_arquivo})")

    # tratamento de datas
    for col_data in ["data_compra", "data_insercao"]:
        if col_data in df.columns:
            df[col_data] = pd.to_datetime(df[col_data], errors="coerce", dayfirst=True)

    # tratamento de valores monetários e quantidades
    if "preco_unitario" in df.columns:
        df["preco_unitario"] = limpar_valor_monetario(df["preco_unitario"])
    if "preco_total" in df.columns:
        df["preco_total"] = limpar_valor_monetario(df["preco_total"])
    if "qtd_itens_comprados" in df.columns:
        df["qtd_itens_comprados"] = limpar_quantidade(df["qtd_itens_comprados"])

    # recalcula preco_total quando ausente/zerado mas dá pra derivar
    if {"preco_unitario", "qtd_itens_comprados", "preco_total"}.issubset(df.columns):
        precisa_recalcular = df["preco_total"].isna() & df["preco_unitario"].notna() & df["qtd_itens_comprados"].notna()
        n_recalc = precisa_recalcular.sum()
        if n_recalc > 0:
            df.loc[precisa_recalcular, "preco_total"] = (
                df.loc[precisa_recalcular, "preco_unitario"] * df.loc[precisa_recalcular, "qtd_itens_comprados"]
            )
            log(f"  ↻ {n_recalc} linha(s) com 'preco_total' recalculado (preco_unitario x quantidade)")

    # padroniza texto (remove espaços duplicados, uppercase em UF/CNPJ)
    for col in ["nome_instituicao", "municipio_instituicao", "fornecedor", "fabricante", "descricao_catmat"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
    if "uf" in df.columns:
        df["uf"] = df["uf"].astype(str).str.strip().str.upper()
    for col in ["cnpj_instituicao", "cnpj_fornecedor", "cnpj_fabricante"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[^\d]", "", regex=True)

    # nulos/vazios
    df = df.replace(r"^\s*$", np.nan, regex=True)
    nulos_por_coluna = df.isna().sum()
    colunas_com_nulos = nulos_por_coluna[nulos_por_coluna > 0]
    if len(colunas_com_nulos) > 0:
        log(f"  valores nulos/vazios encontrados em: {dict(colunas_com_nulos)}")

    # duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        log(f"  🔁 {duplicados} linha(s) totalmente duplicada(s) -> serão removidas")
        df = df.drop_duplicates()

    df["arquivo_origem"] = nome_arquivo
    log(f"  linhas finais após tratamento: {len(df)}")
    return df


def main():
    arquivos = sorted(glob.glob(os.path.join(PASTA_ENTRADA, "*.csv")))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum .csv encontrado em {PASTA_ENTRADA}. Baixe os arquivos do BPS primeiro.")

    log(f"# Relatório de Tratamento — BPS 2020-2026")
    log(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    log(f"Arquivos encontrados: {[os.path.basename(a) for a in arquivos]}")

    anos_encontrados = sorted({extrair_ano_do_nome(a) for a in arquivos if extrair_ano_do_nome(a)})
    faltando = set(ANOS_ESPERADOS) - set(anos_encontrados)
    if faltando:
        log(f"⚠️  ATENÇÃO: faltam arquivos para os anos: {sorted(faltando)}")

    dfs = [processar_arquivo(a) for a in arquivos]

    log("\n## Consolidação final")
    df_final = pd.concat(dfs, ignore_index=True, sort=False)
    log(f"Total de linhas consolidadas: {len(df_final)}")
    log(f"Total de colunas: {len(df_final.columns)}")
    log(f"Colunas finais: {list(df_final.columns)}")

    # ordena colunas: canônicas primeiro, na ordem do dicionário, depois o resto
    ordem = [c for c in MAPA_COLUNAS.keys() if c in df_final.columns]
    resto = [c for c in df_final.columns if c not in ordem]
    df_final = df_final[ordem + resto]

    nome_saida = f"BPS_20_26_{NOME_ALUNO}.csv"
    caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)
    df_final.to_csv(caminho_saida, index=False, encoding="utf-8-sig", sep=";", decimal=",")
    log(f"\n✅ Base consolidada salva em: {caminho_saida}")

    caminho_log = os.path.join(PASTA_SAIDA, "relatorio_tratamento.md")
    with open(caminho_log, "w", encoding="utf-8") as f:
        f.write("\n".join(log_linhas))
    print(f"\n✅ Log de tratamento salvo em: {caminho_log}")


if __name__ == "__main__":
    main()
