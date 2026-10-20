
from datetime import datetime
import pytz

# GATEWAY RESTRITO - barreira juridica P0
def restrito_apresentar(bloco_renderizado: str, texto_livre: str = "") -> str:
    """
    So permite saida se for identica ao bloco renderizado.
    Texto extra, truncado ou livre = mensagem generica (falha fechada).
    """
    if texto_livre and texto_livre != bloco_renderizado:
        return "[MODO RESTRITO] Informacao restrita. Ref: ver origem."
    return bloco_renderizado

def briefing_restrito():
    tz = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(tz).strftime("%d/%m %H:%M")
    bloco = (
        f"BRIEFING JAIME - {agora} (SP)\n"
        f"Modo: restrito | minimizacao + falha fechada\n"
        f"\n"
        f"Agenda: ref: 2 aniversarios / origem: Google Agenda\n"
        f"Gmail: ref: triagem 44 msgs 13/10 / origem: Gmail+Hotmail\n"
        f"Drive: ref: \ADV\modelos\ 2 docs base mapeados\n"
        f"\n"
        f"Pendencias P0: definir classificacao JUR [JUR] vs automatica\n"
        f"Status nuvem: 24h online (Render/Railway)\n"
        f"\n"
        f"Use /agenda para detalhe ref/data/origem"
    )
    return restrito_apresentar(bloco, bloco)

def agenda_restrita():
    bloco = (
        "AGENDA - modo restrito\n"
        "Hoje: ref: 0 reunioes / origem: Google Agenda\n"
        "Amanha: ref: verificar / origem: Google Agenda\n"
        "\n"
        "Para ver nome de cliente: modo precisa estar em JUR liberado"
    )
    return restrito_apresentar(bloco, bloco)

def triagem_emails():
    bloco = (
        "TRIAGEM - ultimos 13/10 (ref)\n"
        "Total: 44 msgs | mantidos: Doc Estudante (19:36), Fala.BR 00567 (15:56), Unimed 448203 (11:01)\n"
        "Origem: rk.juridico@outlook + Gmail\n"
        "Modo: so ref/data/origem - sem valores de boleto\n"
        "\n"
        "Para ver detalhe: /triagem completa (precisa liberar lista fechada de remetentes pessoais)"
    )
    return restrito_apresentar(bloco, bloco)

def gerar_documento(args: str):
    args = args.lower()
    if "procuracao" in args:
        return (
            "GERADOR PROCURACAO\n"
            "Base: \ADV\modelos\1 MODELO PROC NOVA.doc\n"
            "Preencha: CPF, nome, RG\n"
            "Saida: timbrado azul marinho + dourado (sobrio) + marca d'agua\n"
            "Envie: /gerar procuracao CPF 123 nome Fulano"
        )
    if "contrato" in args or "honorario" in args:
        return (
            "GERADOR CONTRATO HONORARIOS\n"
            "Base: \ADV\modelos\1 CONTRATO HON PREV NOVO.doc\n"
            "Clausulas lista fechada (sem inventar valor)\n"
            "Saida: \ADV\contratos_gerados\"
        )
    return "Use: /gerar procuracao ou /gerar contrato"
