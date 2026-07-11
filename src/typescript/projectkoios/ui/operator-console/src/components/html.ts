export class HtmlRenderer {
  escape(value: string): string {
    return value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  renderList(items: readonly string[]): string {
    return `<ul>${items.map((item: string) => `<li>${this.escape(item)}</li>`).join("")}</ul>`;
  }
}
