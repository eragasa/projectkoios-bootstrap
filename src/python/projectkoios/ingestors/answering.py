from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
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
        citations = tuple(evidence.citation for evidence in retrieval.evidence)
        evidence_lines = [f"- {evidence.title} ({evidence.citation})" for evidence in retrieval.evidence]
        evidence_block = "\n".join(evidence_lines) if evidence_lines else "- no evidence found"
        prompt = (
            f"Question: {query}\n\n"
            f"Evidence:\n{evidence_block}\n\n"
            "Write a concise answer with citations."
        )
        if backend is not None:
            try:
                body = backend.generate(prompt)
            except Exception as exc:
                if backend_on_failure != "fallback":
                    raise RuntimeError(f"backend '{backend.name}' failed while composing answer") from exc
                body = self._fallback_summary(query, retrieval)
        else:
            body = self._fallback_summary(query, retrieval)

        cited_body = self._append_citations(body, citations)

        if format == AnswerFormat.STRUCTURED_JSON:
            payload = {
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

        payload = {
            "query": query,
            "answer": cited_body,
            "citations": list(citations),
        }
        return Answer(query=query, format=format, text=cited_body, citations=citations, payload=payload)

    def _fallback_summary(self, query: str, retrieval: RetrievalResult) -> str:
        if not retrieval.evidence:
            return f"No relevant evidence found for: {query}"
        lines = [f"Answering: {query}", ""]
        for evidence in retrieval.evidence:
            lines.append(f"{evidence.title} — {evidence.excerpt}")
        return "\n".join(lines)

    def _append_citations(self, body: str, citations: tuple[str, ...]) -> str:
        if not citations:
            return body
        lines = [body.rstrip(), "", "Citations:"]
        lines.extend(f"- {citation}" for citation in citations)
        return "\n".join(lines)
