<missao>

# Missão: Originar proposta no SITE e verificar no ACOM

## Objetivo
Originar uma proposta pelo **simulador solar do SITE** e confirmar que ela está visível no **ACOM**.

## Recursos de apoio
- **Simulador solar (SITE):** https://abc.com.br
- **CPF de teste:** se o usuário não tiver um CPF que passe na pré-análise, indique `<fonte de CPF de teste>`.
- **Manual de consulta de logs da captura:** `<link do manual>`. Use quando a proposta não for encontrada no ACOM.

---

## Etapa 1 — Acesso ao SITE
**Objetivo:** garantir que o usuário está no simulador solar correto.

**Instruções ao usuário:**
1. Acessar https://abc.com.br.

**Comportamento do agente:**
- Peça confirmação do acesso e uma descrição da tela.
- Tela esperada: tela inicial do simulador, com a opção de iniciar uma simulação.

**Checkpoint:** acesso confirmado e tela descrita bate com o esperado.

---

## Etapa 2 — Preenchimento dos dados no SITE
**Objetivo:** originar a proposta passando por pré-análise, simulação e dados do proponente.

### 2.1 Pré-análise
- Explique: avaliação inicial das informações do cliente para verificar se é possível seguir com a proposta.
- Lembre que há CPF de teste disponível, se necessário.
- Peça para avisar ao chegar à próxima tela.

### 2.2 Simulação
- Explique: definição das condições do financiamento (valores, prazo, parcelas).
- Peça para avisar ao chegar à próxima tela.

### 2.3 Dados do proponente
- Explique: informações cadastrais do cliente que formalizam a proposta.
- Explique que a proposta é **persistida de forma assíncrona** e pode levar algum tempo para aparecer nos demais sistemas.
- Peça o **número da proposta** exibido e que o usuário **guarde o CPF** utilizado.

**Checkpoint:** número da proposta e CPF informados.

---

## Etapa 3 — Verificação no ACOM
**Objetivo:** confirmar que a proposta originada está visível no ACOM.

### 3.1 Contexto
- Explique: `<descrição resumida do ACOM>`.
- Peça confirmação de entendimento antes de seguir.

### 3.2 Acesso e reconhecimento da tela
- Peça para acessar o ACOM e descrever a tela.
- Tela esperada: tela inicial com a opção de consulta de propostas.

### 3.3 Verificação de perfil
- Verificação guiada: o usuário precisa estar logado como **operador solar**.
- Pré-requisito: sem acesso de operador, interrompa e oriente a solicitar o acesso.

### 3.4 Consulta da proposta
- Guie a consulta **pelo CPF** usado na origem.
- Peça o número da proposta encontrada.

### 3.5 Se a proposta não for encontrada
- Por ser assíncrona, sugira aguardar alguns instantes e consultar novamente.
- Persistindo, oriente a consultar os logs da captura pelo manual.

**Checkpoint:** proposta localizada no ACOM.

---

## Critério de finalização
- [ ] Proposta originada no SITE.
- [ ] Proposta visível no ACOM.
- [ ] **Evidência:** número da proposta do SITE **igual** ao encontrado no ACOM.

Se os números não baterem, investigue: CPF digitado, proposta duplicada, ambiente errado.

---

## Exemplo de execução (referência de tom)

> **Agente Tutor:** Vamos iniciar a missão de originar uma proposta no SITE e verificá-la no ACOM. Acesse o simulador solar em https://abc.com.br. Você conseguiu acessar? Descreva brevemente a tela.
>
> **Usuário:** Sim. Apareceu a tela inicial com a opção de iniciar uma simulação.
>
> **Agente Tutor:** Selecione essa opção e preencha os dados da pré-análise. Essa etapa faz uma avaliação inicial das informações necessárias para seguir com a proposta. Avise quando chegar à próxima tela.
>
> **Usuário:** Concluí a pré-análise e estou na tela de simulação.
>
> **Agente Tutor:** Preencha os dados da simulação e avance. Depois, informe o que apareceu.
>
> **Usuário:** A simulação foi concluída. Estou preenchendo os dados do proponente.
>
> **Agente Tutor:** Preencha os dados de teste. A proposta é processada de forma assíncrona, então vamos confirmar a origem antes de consultar o ACOM. Quando concluir, me passe o número da proposta e guarde o CPF usado.
>
> **Usuário:** Concluí. Número: 12345.
>
> **Agente Tutor:** Agora vamos ao ACOM. `<explicação do ACOM>`. Ficou claro? Podemos seguir?
>
> **Usuário:** Sim.
>
> **Agente Tutor:** Acesse o ACOM e descreva a tela inicial.
>
> **Usuário:** Vejo a opção de consulta de propostas.
>
> **Agente Tutor:** Antes de consultar, confirme que está logado com o perfil de operador solar. Onde aparece o seu perfil na tela?
>
> **Usuário:** Aparece "Operador Solar" no canto superior.
>
> **Agente Tutor:** Perfeito. Acesse a consulta de propostas e pesquise pelo CPF usado na origem.
>
> **Usuário:** Encontrei a proposta 12345.
>
> **Agente Tutor:** O número bate com o gerado no SITE. Missão concluída: a proposta foi originada e localizada no ACOM.

</missao>