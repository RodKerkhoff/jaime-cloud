# JAIME - Assistente Geral - Pacote Nuvem 24h

## O que e
Bot Telegram rodando em polling (nao precisa webhook) - funciona 24h no Render/Railway plano gratis.

## Como subir no Render.com (3 cliques)
1. Crie conta no render.com (Login com GitHub)
2. New + > Web Service > Connect repo OU Upload files
3. Se upload: arraste todos os arquivos deste zip
4. Environment Variables:
   TELEGRAM_TOKEN = seu token
   TZ = America/Sao_Paulo
5. Build Command: pip install -r requirements.txt
6. Start Command: python bot.py
7. Deploy

Pronto: bot online. Teste em t.me/seu_bot com /start e /briefing

## Estrutura
- bot.py: polling Telegram
- jaime_core.py: briefing_restrito, restrito_apresentar() = gateway P0 anti-vazamento, triagem, agenda
- requirements.txt
- .env.example

## P0 que falta configurar
1. Classificacao JUR: no jaime_core.py troque logica para [JUR] ou automatica (processo, vara, comarca)
2. Lista fechada boletos pessoais: adicione remetentes permitidos (Angeloni etc) com leitura transitoria

## Seguranca
- Nunca commite .env com token real
- No BotFather use /revoke se vazar
- Modo restrito: toda saida juridica passa por restrito_apresentar()

## Proximos passos
- Adicionar briefing automatico 07h30: use APScheduler dentro do bot.py
- Conectar Gmail/Drive real: implementar OAuth Google

Duvida: fale com Meta AI nesta janela "JAIME - Assistente Geral"