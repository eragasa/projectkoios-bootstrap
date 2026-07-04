from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any
import json

from projectkoios.ingestors.backends import BackendAdapter
from projectkoios.ingestors.retrieval import RetrievalResult


class AnswerFormat(StrEnum):
    CITED_SUMMARY = "cited_summary"
    STRUCTURED_JSON = "structured_json"


@dataclass(frozen=True, slots=True)
class Answer:
    query: str
    format: AnswerFormat
    text: str
    citations: tuple[str, ...]
    payload: dict[str, object]


class AnswerComposer:
    def compose(
        self,
        query: str,
        retrieval: RetrievalResult,
        *,
        format: AnswerFormat,
        backend: BackendAdapter | None = None,
        backend_on_failure: str = "error",
    ) -> Answer:
        citations: tuple[str, ...] = tuple(evidence.citation for evidence in retrieval.evidence)
        evidence_lines: list[str] = [f"- {evidence.title} ({evidence.citation})" for evidence in retrieval.evidence]
        evidence_block: str = "\n".join(evidence_lines) if evidence_lines else "- no evidence found"
        prompt: str = (
            f"Question: {query}\n\n"
            f"Evidence:\n{evidence_block}\n\n"
            "Write a concise answer with citations."
        )
        body: str = self.compose_body(
            prompt=prompt,
            query=query,
            retrieval=retrieval,
            backend=backend,
            backend_on_failure=backend_on_failure,
        )
        cited_body: str = self.append_citations(body, citations)

        if format == AnswerFormat.STRUCTURED_JSON:
            payload: dict[str, Any] = {
                "query": query,
                "answer": cited_body,
                "citations": list(citations),
                "evidence": [
                    {
                        "title": evidence.title,
                        "citation": evidence.citation,
                        "excerpt": evidence.excerpt,
                        "score": evidence.score,
                    }
                    for evidence in retrieval.evidence
                ],
            }
            return Answer(query=query, format=format, text=json.dumps(payload, indent=2, ensure_ascii=False), citations=citations, payload=payload)

        fallback_payload: dict[str, Any] = {
            "query": query,
            "answer": cited_body,
            "citations": list(citations),
        }
        return Answer(query=query, format=format, text=cited_body, citations=citations, payload=fallback_payload)

    def compose_body(
        self,
        *,
        prompt: str,
        query: str,
        retrieval: RetrievalResult,
        backend: BackendAdapter | None,
        backend_on_failure: str,
    ) -> str:
        if backend is None:
            return self.fallback_summary(query, retrieval)
        try:
            return backend.generate(prompt)
        except Exception as exc:
            if backend_on_failure != "fallback":
                raise RuntimeError(f"backend '{backend.name}' failed while composing answer") from exc
            return self.fallback_summary(query, retrieval)

    def fallback_summary(self, query: str, retrieval: RetrievalResult) -> str:
        if not retrieval.evidence:
            return f"No relevant evidence found for: {query}"
        evidence_lines: list[str] = [f"{evidence.title} — {evidence.excerpt}" for evidence in retrieval.evidence]
        lines: list[str] = [f"Answering: {query}", "", *evidence_lines]
        return "\n".join(lines)

    def append_citations(self, body: str, citations: tuple[str, ...]) -> str:
        if not citations:
            return body
        lines: list[str] = [body.rstrip(), "", "Citations:"]
        lines.extend(f"- {citation}" for citation in citations)
        return "\n".join(lines)
