import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { loadContextIndex } from "../lib/data";
import type { ContextSummary } from "../types";

/**
 * Screen 1: every available conversation context as a card, name only.
 *
 * OWNER: task B.
 * Done when: cards render from index.json (never hard-coded) and clicking one
 * routes to /context/:contextId.
 */
export default function ContextList() {
  const [contexts, setContexts] = useState<ContextSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    let cancelled = false;
    loadContextIndex()
      .then((data) => {
        if (!cancelled) setContexts(data);
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Could not load contexts");
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) {
    return (
      <main className="page">
        <p className="status-message status-message--error">
          Couldn't load the context list: {error}
        </p>
      </main>
    );
  }

  if (contexts === null) {
    return (
      <main className="page">
        <p className="status-message">Loading contexts…</p>
      </main>
    );
  }

  if (contexts.length === 0) {
    return (
      <main className="page">
        <p className="status-message">No contexts available yet.</p>
      </main>
    );
  }

  return (
    <main className="page">
      <h1 className="page-title">Context</h1>
      <div className="card-grid">
        {contexts.map((ctx) => (
          <article
            key={ctx.context_id}
            className="context-card"
            role="button"
            tabIndex={0}
            onClick={() => navigate(`/context/${ctx.context_id}`)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                navigate(`/context/${ctx.context_id}`);
              }
            }}
          >
            <span className="context-card-name">{ctx.name || ctx.participant_id}</span>
          </article>
        ))}
      </div>
    </main>
  );
}
