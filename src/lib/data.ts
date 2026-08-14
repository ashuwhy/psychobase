import type { ContextData, ContextSummary } from "../types";

/**
 * Loads what scripts/build_data.py produced. Files live in public/, so they are
 * fetched at runtime and a new context needs no code change or rebuild.
 *
 * OWNER: task B. Add caching if the same context is opened repeatedly.
 */
const BASE = "/data/build";

export async function loadContextIndex(): Promise<ContextSummary[]> {
  const res = await fetch(`${BASE}/index.json`);
  if (!res.ok) throw new Error(`Could not load context list (${res.status})`);
  return res.json();
}

export async function loadContext(contextId: string): Promise<ContextData> {
  const res = await fetch(`${BASE}/${contextId}.json`);
  if (!res.ok) throw new Error(`Could not load context ${contextId} (${res.status})`);
  return res.json();
}
