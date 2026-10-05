"""Interface de Linha de Comando (CLI) para o Agente Tutor de Onboarding."""

import sys
import os
import argparse
import asyncio

# Adiciona o diretório atual ao path de execução
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configura encoding utf-8 para terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from config.settings import settings
from src.tools.profile_tools import register_developer_profile, get_developer_profile
from src.tools.mission_tools import (
    list_available_missions,
    start_mission,
    get_current_mission_status,
    advance_mission_step
)
from src.tools.knowledge_tools import ask_knowledge_agent
from src.mock_kb.mock_kb_server import start_mock_server


def run_demonstration_flow():
    """Executa uma demonstração passo a passo do fluxo do tutor conforme o fluxograma."""
    print("=" * 70)
    print("🎯 DEMONSTRAÇÃO DO FLUXO DO AGENTE TUTOR DE ONBOARDING")
    print("=" * 70)

    # 1. Classificação de Intenção e Boas-Vindas
    print("\n[RODADA 1] Boas-vindas e Classificação de Intenção:")
    print("Dev: 'Olá! Sou um novo desenvolvedor e acabei de entrar na empresa.'")
    print("Tutor: 'Olá! Seja muito bem-vindo ao time de engenharia! 🚀'")
    print("       'Como posso te ajudar hoje?'")
    print("       '> Iniciar/Continuar onboarding'")
    print("       '> Tirar dúvida técnica ou de processo'")

    # 2. Entrevista do Desenvolvedor
    print("\n[RODADA 2] Entrevista de Onboarding do Usuário:")
    print("Dev: 'Gostaria de iniciar o onboarding. Sou desenvolvedor Backend com foco em Java e Spring.'")
    print("Tutor acionando ferramenta: register_developer_profile(...)")
    profile_res = register_developer_profile(
        developer_name="Carlos Silva",
        area="backend",
        primary_stack="java, spring, postgres",
        experience_level="junior",
        goals="Dominar a arquitetura dos microsserviços da empresa e fluxos de faturamento"
    )
    print(f"Resultado da Tool: {profile_res['message']}")
    print(f"Perfil Gravado no Estado: {profile_res['profile']}")

    # 3. Seleção de Missão
    print("\n[RODADA 3] Seleção de Missão Compatível com Perfil:")
    print("Tutor acionando ferramenta: list_available_missions(...)")
    missions_res = list_available_missions()
    print(f"Total de missões disponíveis: {missions_res['total_available']}")
    for m in missions_res["missions"]:
        print(f"  - [{m['id']}] ({m['type'].upper()}) {m['title']} (~{m['estimated_minutes']} min)")

    print("\nDev: 'Quero começar pela missão técnica tech-01!'")
    print("Tutor acionando ferramenta: start_mission('tech-01')...")
    start_res = start_mission("tech-01")
    print(f"Status: {start_res['message']}")
    curr_step = start_res["current_step"]
    print(f"\n[RODADA 4] Execução da Missão - Etapa {curr_step['step_number']} de {curr_step['total_steps']}:")
    print(f"Título: {curr_step['title']}")
    print(f"Instrução: {curr_step['instruction']}")
    print(f"Ação Esperada: {curr_step['expected_action']}")
    print(f"Dica: {curr_step['hint']}")

    # 4. Avanço do Passo 1
    print("\nDev: 'Clonei o repositório ms-documento-api e verifiquei o pom.xml. O projeto usa Java 21 e Spring Boot.'")
    print("Tutor acionando ferramenta: advance_mission_step(...)")
    adv_res1 = advance_mission_step(step_notes="Clonado repositório ms-documento-api, Java 21 e Spring Boot")
    next_step = adv_res1["next_step"]
    print(f"Resultado: {adv_res1['message']}")
    print(f"\n[RODADA 5] Execução da Missão - Etapa {next_step['step_number']} de {next_step['total_steps']}:")
    print(f"Título: {next_step['title']}")
    print(f"Instrução: {next_step['instruction']}")
    print(f"Ação Esperada: {next_step['expected_action']}")

    # 5. Dúvida do Dev (Oferecer Suporte com consulta A2A)
    print("\n[RODADA 6] Dúvida do Dev (Oferecer Suporte com consulta A2A):")
    print("Dev: 'Abri o docker-compose.yml mas fiquei em dúvida sobre qual é o motor de armazenamento usado aqui.'")
    print("Tutor: 'Vou consultar nossa Base de Conhecimento oficial via A2A para checar os detalhes arquiteturais!'")
    print("Tutor acionando ferramenta: ask_knowledge_agent('motor de armazenamento', category='tecnica')...")
    kb_res = ask_knowledge_agent(query="motor de armazenamento", category="tecnica")
    print(f"Resposta A2A [{kb_res['source']}]:\n\"{kb_res['answer']}\"")
    print("Tutor: 'Entendeu? Usamos PostgreSQL para metadados e MinIO/S3 para os binários. Agora pode prosseguir!'")

    # 6. Dev valida a etapa e avança
    print("\n[RODADA 7] Dev reporta resultado do passo 2:")
    print("Dev: 'Perfeito! Verifiquei no docker-compose e vi o container do PostgreSQL 16 e do MinIO configurados.'")
    adv_res2 = advance_mission_step(step_notes="Identificado PostgreSQL 16 para metadados e MinIO para binários")
    step3 = adv_res2["next_step"]
    print(f"Resultado: {adv_res2['message']}")
    print(f"Instrução da Etapa 3: {step3['instruction']}")

    # 7. Conclusão da Missão
    print("\n[RODADA 8] Conclusão da última etapa:")
    print("Dev: 'Rodei os testes locais com sucesso! Todos os testes de integração passaram.'")
    final_res = advance_mission_step(step_notes="Testes unitários e de integração executados com 100% de sucesso")
    print(f"Resultado Final: {final_res['message']}")
    print(f"Total de missões concluídas pelo Dev: {final_res['total_completed_missions']}")

    print("\n" + "=" * 70)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Agente Tutor de Onboarding (Google ADK)")
    parser.add_argument("--demo", action="store_true", help="Executa o fluxo de demonstração completo")
    parser.add_argument("--mock-kb", action="store_true", help="Inicia o servidor mock A2A da Base de Conhecimento")
    parser.add_argument("--test", action="store_true", help="Executa a suíte de testes com pytest")

    args = parser.parse_args()

    if args.mock_kb:
        start_mock_server()
    elif args.test:
        import pytest
        pytest.main(["tests", "-v"])
    else:
        # Modo padrão: demonstração do fluxo guiado
        run_demonstration_flow()


if __name__ == "__main__":
    main()
