"""Adaptador para moderação e julgamento de escopo via modelos locais no Ollama."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Optional

import httpx

from ..config import OLLAMA_GUARD_MODEL, OLLAMA_HOST, OLLAMA_JUDGE_MODEL
from ..contracts import GuardrailAction, RailType, RiskCategory, Verdict

logger = logging.getLogger(__name__)


class OllamaGuard:
    """Interface com modelos de segurança e julgamento locais executando no Ollama."""

    def __init__(
        self,
        host: str = OLLAMA_HOST,
        guard_model: str = OLLAMA_GUARD_MODEL,
        judge_model: str = OLLAMA_JUDGE_MODEL,
        timeout_seconds: float = 2.0,
    ) -> None:
        self.host = host.rstrip("/")
        self.guard_model = guard_model
        self.judge_model = judge_model
        self.timeout = timeout_seconds

    def is_available(self) -> bool:
        """Verifica se o servidor Ollama está respondendo."""
        try:
            with httpx.Client(timeout=0.8) as client:
                res = client.get(f"{self.host}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    def check_safety(self, text: str) -> Optional[Verdict]:
        """Avalia a mensagem com Llama Guard local (se disponível)."""
        start = time.perf_counter()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                prompt = f"[INST] Task: Check for unsafe content.\nUser: {text} [/INST]"
                payload = {
                    "model": self.guard_model,
                    "prompt": prompt,
                    "stream": False,
                }
                res = client.post(f"{self.host}/api/generate", json=payload)
                if res.status_code != 200:
                    return None

                data = res.json()
                response_text = data.get("response", "").strip()
                latency = (time.perf_counter() - start) * 1000

                if response_text.startswith("unsafe"):
                    category_code = response_text.splitlines()[1] if len(response_text.splitlines()) > 1 else "general"
                    return Verdict(
                        blocked=True,
                        reason="Conteúdo classificado como inseguro pelo modelo de segurança local.",
                        category=RiskCategory.DANGEROUS_CONTENT,
                        action=GuardrailAction.BLOCK,
                        rail=RailType.INPUT,
                        details={"ollama_model": self.guard_model, "category_code": category_code},
                        latency_ms=latency,
                    )
                return Verdict(
                    blocked=False,
                    category=RiskCategory.SAFE,
                    action=GuardrailAction.ALLOW,
                    rail=RailType.INPUT,
                    latency_ms=latency,
                )
        except Exception as e:
            logger.debug(f"Ollama local guard indisponível ou em timeout: {e}")
            return None

    def judge_scope(self, text: str, agent_name: str, allowed_topics: list[str]) -> Optional[Verdict]:
        """Usa SLM local leve como juiz para classificar escopo em casos ambíguos."""
        start = time.perf_counter()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                topics_str = ", ".join(allowed_topics)
                prompt = (
                    f"Você é o Guardião de Escopo do agente '{agent_name}'.\n"
                    f"Tópicos permitidos: {topics_str}.\n"
                    f"Mensagem do usuário: \"{text}\"\n"
                    f"Responda estritamente com IN_SCOPE ou OUT_OF_SCOPE."
                )
                payload = {
                    "model": self.judge_model,
                    "prompt": prompt,
                    "stream": False,
                }
                res = client.post(f"{self.host}/api/generate", json=payload)
                if res.status_code != 200:
                    return None

                response_text = res.json().get("response", "").strip().upper()
                latency = (time.perf_counter() - start) * 1000

                if "OUT_OF_SCOPE" in response_text:
                    return Verdict(
                        blocked=True,
                        reason=f"A mensagem foi classificada como fora do escopo do agente '{agent_name}'.",
                        category=RiskCategory.OUT_OF_SCOPE,
                        action=GuardrailAction.DEVIATE,
                        rail=RailType.SCOPE,
                        details={"ollama_judge": self.judge_model},
                        latency_ms=latency,
                    )
                return Verdict(
                    blocked=False,
                    category=RiskCategory.SAFE,
                    action=GuardrailAction.ALLOW,
                    rail=RailType.SCOPE,
                    latency_ms=latency,
                )
        except Exception as e:
            logger.debug(f"Ollama scope judge indisponível ou em timeout: {e}")
            return None
