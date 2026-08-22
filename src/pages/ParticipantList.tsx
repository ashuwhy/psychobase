import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { loadContextSummary } from "../lib/data";
import type { ContextSummary } from "../types";

/**
 * Screen 2: the variant(s) inside one context - the original conversation,
 * plus a "Modified" rewrite when one exists, rather than the two appearing
 * as separate cards on the context selection screen.
 *
 * OWNER: task B.
 * Done when: each variant renders as a card from the context's index entry
 * and clicking one routes to /context/:contextId/participant/:variantId.
 */
export default function ParticipantList() {
  const { contextId } = useParams<{ contextId: string }>();
  const [summary, setSummary] = useState<ContextSummary | null | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!contextId) return;
    let cancelled = false;
    setSummary(undefined);
    setError(null);
    loadContextSummary(contextId)
      .then((found) => {
        if (!cancelled) setSummary(found ?? null);
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Could not load this context");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [contextId]);

  if (error) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message status-message--error">{error}</p>
      </main>
    );
  }

  if (summary === undefined) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message">Loading…</p>
      </main>
    );
  }

  if (summary === null) {
    return (
      <main className="page">
        <Link to="/" className="back-link">
          ← Context
        </Link>
        <p className="status-message status-message--error">
          No context found for "{contextId}".
        </p>
      </main>
    );
  }

  return (
    <main className="page">
      <Link to="/" className="back-link">
        ← Context
      </Link>
      <h1 className="page-title">{summary.name || summary.context_id}</h1>
      <div className="card-grid">
        {summary.variants.map((variant) => (
          <article
            key={variant.id}
            className={`context-card${variant.label === "Modified" ? " context-card--modified" : ""}`}
            role="button"
            tabIndex={0}
            onClick={() => navigate(`/context/${summary.context_id}/participant/${variant.id}`)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                navigate(`/context/${summary.context_id}/participant/${variant.id}`);
              }
            }}
          >
            <span className="context-card-avatar" aria-hidden="true">
              {variant.label.charAt(0)}
            </span>
            <span className="context-card-name">{variant.label}</span>
            <span className="context-card-sub">
              {variant.participant_id || summary.context_id} · {variant.turn_count} turns
            </span>
          </article>
        ))}
      </div>
    </main>
  );
}
