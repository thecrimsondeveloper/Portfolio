export class EventBus {
  constructor(snapshot) {
    this.snapshot = snapshot;
    this.clients = new Set();
  }

  connect(response) {
    response.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    });
    response.write(`data: ${JSON.stringify(this.snapshot())}\n\n`);
    this.clients.add(response);
    response.on("close", () => this.clients.delete(response));
  }

  emit() {
    const payload = `data: ${JSON.stringify(this.snapshot())}\n\n`;
    for (const client of this.clients) {
      client.write(payload);
    }
  }
}
