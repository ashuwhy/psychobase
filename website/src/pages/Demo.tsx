import { Link } from "react-router-dom";

/**
 * /demo: the 6 Nov live run of the multi-turn model, cut to three minutes.
 * The QR code on the final-eval deck (live-demo slide) points here.
 */
export default function Demo() {
  return (
    <main className="page demo-page">
      <Link to="/" className="back-link">
        ← Contexts
      </Link>
      <h1 className="page-title">Live demo</h1>
      <p className="demo-lede">
        Our fine-tuned model in two made-up scenarios, six turns each, recorded on 6 Nov 2026. Each
        turn shows the simulated user message with its physiology summary, then two replies: one
        with the physiology and one from text alone. The waits for the model are cut.
      </p>
      <video
        className="demo-video"
        controls
        playsInline
        preload="metadata"
        poster="/data/demo/poster.jpg"
      >
        <source src="/data/demo/physiobase-demo.mp4" type="video/mp4" />
        <a href="/data/demo/physiobase-demo.mp4">Download the video (MP4, 3 min)</a>
      </video>
      <div className="demo-cases">
        <section className="demo-case">
          <h2>A · PhD stipend, three months late</h2>
          <p>Stress climbs from 4 to 6. The student calls the replies repetitive at turn 5 and gives up at turn 6.</p>
        </section>
        <section className="demo-case">
          <h2>B · Nurse, third night shift in a row</h2>
          <p>Stress falls from 3 to 1. She settles and plans a second check with the senior sister.</p>
        </section>
      </div>
      <p className="demo-note">
        The simulator writes the user text and the physiology together, so the stress score is
        simulated, not measured. The reply with physiology chose a different strategy from the
        text-only reply in 9 of the 12 turns.
      </p>
    </main>
  );
}
