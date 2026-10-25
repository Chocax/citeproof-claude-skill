/**
 * CiteProof helpers for building .docx files with the `docx` npm package.
 *
 *   const cp = require("./docx_notes.js");
 *   children.push(...cp.conventionNote({ lang: "es" }));
 *   children.push(cp.citedText(["Texto que cita a ", { cite: "(Lee, 2021)", url: "https://..." }, "."]));
 *   children.push(...cp.captureNote({ cite: "(Lee, 2021)", url: "https://...", find: "verbatim fragment", lang: "es" }));
 *   children.push(...cp.evidenceImage({ png: "evidence/01.png", url: "https://...", cite: "(Lee, 2021)", lang: "es" }));
 *
 * Every URL produced here is a real hyperlink (w:hyperlink), so Ctrl+click works in Word.
 */
const fs = require("fs");
const {
  Paragraph, TextRun, ExternalHyperlink, ImageRun, AlignmentType, UnderlineType,
} = require("docx");

const NOTE_FONT = "Arial";
const NOTE_SIZE = 20; // half-points → 10 pt
const T = {
  es: { tag: "[NOTA – BORRAR] ", link: "Hipervínculo en la cita ", evidence: "Evidencia de ", captured: "capturada el " },
  en: { tag: "[NOTE – DELETE] ", link: "Hyperlink goes on the citation ", evidence: "Evidence for ", captured: "captured " },
};

const noteRun = (text, extra = {}) =>
  new TextRun({ text, font: NOTE_FONT, size: NOTE_SIZE, highlight: "yellow", underline: { type: UnderlineType.SINGLE }, ...extra });

const noteLink = (url) =>
  new ExternalHyperlink({
    link: url,
    children: [new TextRun({ text: url, font: NOTE_FONT, size: NOTE_SIZE, highlight: "yellow", color: "0563C1", underline: { type: UnderlineType.SINGLE } })],
  });

/** Manual-mode capture note: 2 lines, citation named, clickable link, verbatim fragment. */
function captureNote({ cite, url, find, tip, section, lang = "es" }) {
  const t = T[lang] || T.es;
  const where = cite + (section ? ` (${section})` : "");
  return [
    new Paragraph({
      spacing: { after: 0, line: 260 },
      keepNext: true,
      children: [noteRun(t.tag + t.link + where + " · Link: "), noteLink(url)],
    }),
    new Paragraph({
      spacing: { after: 160, line: 260 },
      children: [noteRun("Ctrl+F: «" + find + "»" + (tip ? "  · " + tip : ""))],
    }),
  ];
}

/** One-time note at the top of the document explaining the convention. */
function conventionNote({ lang = "es" } = {}) {
  const lines = lang === "en"
    ? [
        "[NOTE – DELETE] Each yellow note names the citation where the hyperlink goes, a clickable link (Ctrl+click) and a verbatim fragment.",
        "Open the link, press Ctrl+F with the fragment, screenshot the highlighted passage, paste it here, hyperlink the citation and delete the note.",
        "If Ctrl+F doesn't find the whole fragment (curly quotes, PDF line breaks), search 4–5 consecutive words.",
      ]
    : [
        "[NOTA – BORRAR] Cada nota amarilla dice en qué cita va el hipervínculo, el link (Ctrl+clic para abrirlo) y una frase textual de la fuente.",
        "Abre el link, busca la frase con Ctrl+F, toma la captura del fragmento, pégala aquí, ponle el hipervínculo a la cita y borra la nota.",
        "Si Ctrl+F no encuentra la frase completa (comillas tipográficas, saltos de línea de un PDF), busca 4 o 5 palabras seguidas.",
      ];
  return lines.map((l, i) => new Paragraph({ spacing: { after: i === lines.length - 1 ? 200 : 0, line: 260 }, children: [noteRun(l)] }));
}

/**
 * A body paragraph where citations are hyperlinked.
 * parts: array of strings, {t, b, i} runs, or {cite, url} citations.
 */
function citedText(parts, paragraphOpts = {}) {
  const children = parts.map((p) => {
    if (typeof p === "string") return new TextRun(p);
    if (p.cite) return new ExternalHyperlink({ link: p.url, children: [new TextRun({ text: p.cite, style: "Hyperlink" })] });
    return new TextRun({ text: p.t, bold: p.b, italics: p.i });
  });
  return new Paragraph({ children, spacing: { after: 140, line: 300 }, alignment: AlignmentType.JUSTIFIED, ...paragraphOpts });
}

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

/** Auto-mode evidence: hyperlinked screenshot + one-line caption. */
function evidenceImage({ png, url, cite, lang = "es", widthIn = 6.0, date }) {
  const t = T[lang] || T.es;
  const { w, h } = pngSize(png);
  const wpx = Math.round(widthIn * 96);
  const hpx = Math.round((wpx * h) / w);
  const when = date || new Date().toISOString().slice(0, 10);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      keepNext: true,
      spacing: { before: 80, after: 40 },
      children: [new ExternalHyperlink({
        link: url,
        children: [new ImageRun({ type: "png", data: fs.readFileSync(png), transformation: { width: wpx, height: hpx },
          altText: { title: t.evidence + cite, description: url, name: png } })],
      })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new TextRun({ text: `${t.evidence}${cite} — ${t.captured}${when}. `, italics: true, size: 18 }),
        new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: "Hyperlink", size: 18 })] })],
    }),
  ];
}

/** Reference-list entry with hanging indent and a clickable URL/DOI at the end. */
function referenceEntry(parts, url) {
  const children = parts.map((p) => (typeof p === "string" ? new TextRun(p) : new TextRun({ text: p.t, italics: p.i, bold: p.b })));
  if (url) children.push(new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: "Hyperlink" })] }));
  return new Paragraph({ children, indent: { left: 720, hanging: 720 }, spacing: { after: 120, line: 276 } });
}

module.exports = { captureNote, conventionNote, citedText, evidenceImage, referenceEntry };
