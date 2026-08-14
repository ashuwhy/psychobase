/**
 * Screen 2: conversation on the left, five graphs on the right.
 *
 * Owns the one piece of shared state - which turn is selected - and passes the
 * selected turn's interval down to every chart so all five highlight the same
 * range.
 *
 * OWNER: task D (shell, state, layout). Charts come from task C, the turn list
 * from task D, data loading from task B.
 */
export default function ConversationView() {
  return <main className="layout">{/* TODO(task D) */}</main>;
}
