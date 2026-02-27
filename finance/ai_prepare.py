from dao.transaction_dao import TransactionDAO
import pandas as pd


def gerar_resumo_financeiro() -> dict:
    with TransactionDAO() as dao:
        transactions = list(dao.get_all_transactions(all=False))
        transactions_list = [
            {
                "id": t.id,
                "description": t.description,
                "date": t.transaction_date.strftime("%d/%m/%Y"),
                "value": t.transaction_value,
                "type": t.type,
                "category": t.category.name if t.category else None,
            }

            for t in transactions
        ]
        df = pd.DataFrame(transactions_list)
    df['value'] = pd.to_numeric(df['value'], errors='coerce').fillna(0.0)
    df['type'] = df['type'].astype(str).str.strip().str.capitalize()
    # garantir datas
    try:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    except Exception:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # calcular métricas básicas
    receitas = df.loc[df['type'] == 'Receita', 'value'].sum()
    despesas = df.loc[df['type'] == 'Despesa', 'value'].sum()
    saldo = receitas - despesas
    taxa_poupanca_pct = (saldo / receitas * 100) if receitas != 0 else 0.0

    # distribuição por categoria (somente despesas)
    despesas_por_cat = (
        df.loc[df['type'] == 'Despesa']
        .groupby('category')['value']
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    # dívida detectada: categoria chamada 'Dívidas' ou 'Dividas'
    dividas = 0.0
    for key in ['Dívidas', 'Dividas', 'Divida', 'Dívida']:
        if key in df['category'].unique():
            dividas += df.loc[
                (df['category'] == key) & (df['type'] == 'Despesa'), 'value'
                ].sum()

    resumo = {
        "receitas": round(float(receitas), 2),
        "despesas": round(float(despesas), 2),
        "saldo": round(float(saldo), 2),
        "taxa_poupanca_pct": round(float(taxa_poupanca_pct), 2),
        "despesas_por_categoria":
            {str(k): float(v) for k, v in despesas_por_cat.items()},
        "dividas": round(float(dividas), 2),
        "periodo_inicio": str(df['date'].min()) if
            not df['date'].isnull().all() else None,
        "periodo_fim": str(df['date'].max()) if
            not df['date'].isnull().all() else None,
    }
    return resumo


def montar_prompt_para_openai(resumo: dict) -> str:
    # Template em PT-BR para o modelo receber e gerar diagnóstico
    prompt = f"""
    Você é um especialista em finanças pessoais. Analise o resumo financeiro
    abaixo e gere um relatório de diagnóstico completo, claro e motivador.
    Divida o relatório em: Visão geral, Principais pontos de atenção,
    Oportunidades de economia, Plano de ação (3 a 5 passos) e Recomendação
    de produtos/contas para reserva de emergência.
    Seja prático e dê números concretos (valores em reais e percentuais).

    Resumo financeiro (auto-gerado):
    - Período: {resumo.get('periodo_inicio')} até {resumo.get('periodo_fim')}
    - Receitas totais: R$ {resumo.get('receitas'):.2f}
    - Despesas totais: R$ {resumo.get('despesas'):.2f}
    - Saldo: R$ {resumo.get('saldo'):.2f}
    - Taxa de poupança (% sobre a receita):
        {resumo.get('taxa_poupanca_pct'):.2f}%
    - Dívidas identificadas (valor): R$ {resumo.get('dividas'):.2f}
    - Distribuição das maiores categorias de despesa:
        {resumo.get('despesas_por_categoria')}

    Dê recomendações específicas com valores (ex.: "reduza X na categoria Y,
    isso economiza R$ Z por mês") e proponha metas (ex.: reserva de emergência
    equivalente a N meses de despesas).
    Formate sua resposta usando markdown, com títulos e listas para facilitar a leitura.
    """
    return prompt
