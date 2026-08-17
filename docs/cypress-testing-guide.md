# Cypress E2E Testing Guide

This guide explains how to write and run End-to-End (E2E) tests using Cypress in this project.

## Project Structure

Cypress tests are located in the `frontend/cypress` directory.
- `frontend/cypress.config.ts`: Cypress configuration file.
- `frontend/cypress/e2e/`: Contains your E2E test files (e.g., `observability.cy.ts`).

## Writing Cypress Tests

Cypress tests are written in JavaScript/TypeScript and use a syntax similar to Mocha and Chai.

### Basic Structure

A Cypress test typically consists of `describe` blocks for test suites and `it` blocks for individual tests.

```typescript
// frontend/cypress/e2e/example.cy.ts
describe('My Test Suite', () => {
  beforeEach(() => {
    // Runs before each test in this describe block
    cy.visit('http://localhost:5173'); // Example: Visit your application's base URL
  });

  it('should test something specific', () => {
    // This is an individual test case
    cy.get('selector').should('be.visible'); // Example: Assert an element is visible
    cy.contains('Text').click(); // Example: Click an element containing specific text
    cy.url().should('include', '/new-page'); // Example: Assert URL change
  });

  it('can perform another test', () => {
    cy.get('another-selector').type('some input'); // Example: Type into an input field
    cy.request('/api/data').then((response) => {
      expect(response.status).to.eq(200); // Example: Make an API request and assert its status
    });
  });
});
```

### Key Cypress Commands

-   **`cy.visit(url)`**: Navigates to a URL.
-   **`cy.get(selector)`**: Selects one or more DOM elements.
-   **`cy.contains(text)`**: Selects a DOM element containing the specified text.
-   **`.click()`**: Clicks a DOM element.
-   **`.type(text)`**: Types text into an input field.
-   **`.should(assertion, value)`**: Makes an assertion about the current subject.
-   **`cy.request(url)`**: Makes an HTTP request outside of the browser's UI. Useful for checking API endpoints or backend services directly.
-   **`cy.wait(milliseconds)`**: Pauses the test for a specified duration. Use sparingly, prefer waiting for specific elements or network requests.

### Example: Observability E2E Test (`frontend/cypress/e2e/observability.cy.ts`)

This test verifies that the frontend correctly sends metrics to the OpenTelemetry Collector.

```typescript
describe('Observability E2E', () => {
  it('sends metrics to the collector', () => {
    // Visit the frontend application
    cy.visit('http://localhost:5173');
    // Wait for document load metric to be exported (adjust wait time as needed)
    cy.wait(2000);
    // Directly request metrics from the otel-collector's Prometheus endpoint
    cy.request('http://localhost:8889/metrics').then((response) => {
      expect(response.status).to.eq(200);
      // Assert that a specific metric (document_load_duration_seconds) is present in the response body
      expect(response.body).to.include('document_load_duration_seconds');
    });
  });
});
```

## Running Cypress Tests

To run Cypress tests, navigate to the `frontend/` directory and use the `cypress` command.

1.  **Open the Cypress Test Runner (Interactive Mode):**
    ```bash
    cd frontend
    npx cypress open
    ```
    This command opens the Cypress Test Runner UI, where you can select and run tests interactively.

2.  **Run Tests in Headless Mode (CLI):**
    ```bash
    cd frontend
    npx cypress run
    ```
    This command runs all tests in the headless browser and outputs results to the terminal. This is typically used in CI/CD pipelines.

3.  **Run a Specific Test File:**
    ```bash
    cd frontend
    npx cypress run --spec "cypress/e2e/observability.cy.ts"
    ```
    Replace `"cypress/e2e/observability.cy.ts"` with the path to your desired test file.

Before running Cypress tests, ensure that your frontend application and any necessary backend services (like the OpenTelemetry Collector) are running. The `baseUrl` in `cypress.config.ts` (`http://localhost:5173` by default) should point to your running frontend application.
