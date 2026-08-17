describe('Observability E2E', () => {
  it('sends metrics to the collector', () => {
    // Visit the frontend
    cy.visit('http://localhost:5173');
    // Wait for document load metric to be exported
    cy.wait(2000);
    // Check the otel-collector's Prometheus endpoint
    cy.request('http://localhost:8889/metrics').then((response) => {
      expect(response.status).to.eq(200);
      // Look for a document load metric exported by OpenTelemetry
      expect(response.body).to.include('document_load_duration_seconds');
    });
  });
});

