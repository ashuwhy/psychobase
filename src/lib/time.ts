/**
 * Charts need numeric X values; the pipeline emits ISO strings. Convert once at
 * load rather than inside the render path.
 *
 * OWNER: task C.
 */
export const toMs = (iso: string): number => new Date(iso).getTime();

export function formatClock(iso: string): string {
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

/** "19:33 - 19:38 (5 min)" for showing which window is highlighted. */
export function formatInterval(start: string, end: string, minutes: number): string {
  return `${formatClock(start)} - ${formatClock(end)} (${minutes} min)`;
}
