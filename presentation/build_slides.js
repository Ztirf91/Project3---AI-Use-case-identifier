const pptxgen = require("pptxgenjs");
const path = require("path");

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "AI Use Case Identifier";
  pres.author = "Ironhack Project 3";

  const C = {
    bg: "0F172A",
    card: "1E293B",
    text: "F8FAFC",
    muted: "94A3B8",
    accent: "0F766E",
    light: "CCFBF1",
  };

  function bg(slide) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: "100%", h: "100%",
      fill: { color: C.bg },
    });
  }

  // 1 Title
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("AI Use Case Identifier", {
      x: 0.8, y: 2.0, w: 11.5, h: 1,
      fontSize: 40, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    s.addText("Pre-meeting briefs for AI consulting with SMEs\nIronhack Project 3 · LangGraph MVP", {
      x: 0.8, y: 3.2, w: 11.5, h: 1,
      fontSize: 20, color: C.muted, margin: 0, isTextBox: true,
    });
  }

  // 2 Problem + user
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("Problem and user", {
      x: 0.8, y: 0.5, w: 11.5, h: 0.6,
      fontSize: 32, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.8, y: 1.4, w: 5.5, h: 4.2, fill: { color: C.card }, rectRadius: 0.15,
    });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 6.7, y: 1.4, w: 5.5, h: 4.2, fill: { color: C.card }, rectRadius: 0.15,
    });
    s.addText("The problem", {
      x: 1.1, y: 1.7, w: 5, h: 0.4, fontSize: 18, bold: true, color: C.light, margin: 0, isTextBox: true,
    });
    s.addText("SMEs want AI, but consultants spend the first meeting guessing the business model, processes, and where AI could help. Generic use-case lists do not stick.", {
      x: 1.1, y: 2.3, w: 5, h: 2.8, fontSize: 16, color: C.text, margin: 0, isTextBox: true,
    });
    s.addText("The user", {
      x: 7.0, y: 1.7, w: 5, h: 0.4, fontSize: 18, bold: true, color: C.light, margin: 0, isTextBox: true,
    });
    s.addText("An AI consultant preparing a first conversation with a German SME — later the same brief can be a lead magnet for owners and MDs.", {
      x: 7.0, y: 2.3, w: 5, h: 2.8, fontSize: 16, color: C.text, margin: 0, isTextBox: true,
    });
  }

  // 3 Autonomy
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("Autonomy: one command → report", {
      x: 0.8, y: 0.5, w: 11.5, h: 0.6,
      fontSize: 28, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    const steps = [
      "Website + jobs",
      "News + register",
      "Business model\n+ process map",
      "Rubric + RAG\n+ rerank",
      "Report + map",
    ];
    steps.forEach((label, i) => {
      const x = 0.6 + i * 2.5;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x, y: 2.2, w: 2.2, h: 2.0, fill: { color: C.card }, rectRadius: 0.12,
      });
      s.addText(String(i + 1), {
        x, y: 2.35, w: 2.2, h: 0.4, fontSize: 14, bold: true, color: C.accent, align: "center", margin: 0, isTextBox: true,
      });
      s.addText(label, {
        x: x + 0.1, y: 2.85, w: 2.0, h: 1.1, fontSize: 14, color: C.text, align: "center", margin: 0, isTextBox: true,
      });
      if (i < steps.length - 1) {
        s.addText("→", {
          x: x + 2.05, y: 2.9, w: 0.4, h: 0.4, fontSize: 20, color: C.muted, margin: 0, isTextBox: true,
        });
      }
    });
    s.addText("python -m app.run --company \"KoRo\" --url \"https://www.korodrogerie.de\"", {
      x: 0.8, y: 5.0, w: 11.5, h: 0.5, fontSize: 16, color: C.light, margin: 0, isTextBox: true,
    });
  }

  // 4 Report
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("The report: useful before the meeting", {
      x: 0.8, y: 0.5, w: 11.5, h: 0.6,
      fontSize: 28, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    const items = [
      { t: "Company + process map", d: "Documented vs assumption, unit economics" },
      { t: "Three use cases", d: "Change process first → AI assist → pilot" },
      { t: "Redesign + Option B", d: "Augment people, speculative bigger bet" },
      { t: "Meeting questions", d: "General discovery + case-specific checks" },
    ];
    items.forEach((item, i) => {
      const y = 1.4 + i * 1.0;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: 0.8, y, w: 11.5, h: 0.85, fill: { color: C.card }, rectRadius: 0.1,
      });
      s.addText(item.t, {
        x: 1.1, y: y + 0.12, w: 11, h: 0.35, fontSize: 18, bold: true, color: C.light, margin: 0, isTextBox: true,
      });
      s.addText(item.d, {
        x: 1.1, y: y + 0.45, w: 11, h: 0.3, fontSize: 14, color: C.muted, margin: 0, isTextBox: true,
      });
    });
  }

  // 5 Stack
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("Why LangGraph (not n8n for this MVP)", {
      x: 0.8, y: 0.5, w: 11.5, h: 0.6,
      fontSize: 28, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    const bullets = [
      "Shared typed state: research → model → picks → report",
      "Rules in code: evidence ids, quick win + redesign, retrieved cards only",
      "RAG + company-fit rerank inside the match node",
      "n8n stays secondary: templates feed the library; later webhook/UI",
    ];
    bullets.forEach((b, i) => {
      s.addText("▸  " + b, {
        x: 0.8, y: 1.5 + i * 0.85, w: 11.5, h: 0.7,
        fontSize: 18, color: C.text, margin: 0, isTextBox: true,
      });
    });
  }

  // 6 GTM
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("GTM: next three sprints", {
      x: 0.8, y: 0.4, w: 11.5, h: 0.55,
      fontSize: 28, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    const sprints = [
      { n: "1", t: "Brief for email", m: "30 requests · 25% book a call" },
      { n: "2", t: "Validate questions", m: "7/10 calls decide on a use case" },
      { n: "3", t: "Vertical workshop", m: "2 paid workshops booked" },
    ];
    sprints.forEach((sp, i) => {
      const x = 0.8 + i * 4.0;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x, y: 1.4, w: 3.7, h: 4.0, fill: { color: C.card }, rectRadius: 0.15,
      });
      s.addText("Sprint " + sp.n, {
        x: x + 0.25, y: 1.7, w: 3.2, h: 0.4, fontSize: 14, color: C.accent, margin: 0, isTextBox: true,
      });
      s.addText(sp.t, {
        x: x + 0.25, y: 2.3, w: 3.2, h: 1.2, fontSize: 22, bold: true, color: C.text, margin: 0, isTextBox: true,
      });
      s.addText(sp.m, {
        x: x + 0.25, y: 4.0, w: 3.2, h: 1.0, fontSize: 15, color: C.muted, margin: 0, isTextBox: true,
      });
    });
  }

  // 7 Demo / close
  {
    const s = pres.addSlide();
    bg(s);
    s.addText("Demo + backup", {
      x: 0.8, y: 1.8, w: 11.5, h: 0.7,
      fontSize: 36, bold: true, color: C.text, margin: 0, isTextBox: true,
    });
    s.addText("Live: python -m app.run …\nBackup: samples/koro.md + process-map.png\nGitHub: Ztirf91/Project3---AI-Use-case-identifier", {
      x: 0.8, y: 2.8, w: 11.5, h: 2.0,
      fontSize: 20, color: C.muted, margin: 0, isTextBox: true,
    });
  }

  const outPptx = path.join(__dirname, "project3_slides.pptx");
  await pres.writeFile({ fileName: outPptx });
  console.log("Wrote", outPptx);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
