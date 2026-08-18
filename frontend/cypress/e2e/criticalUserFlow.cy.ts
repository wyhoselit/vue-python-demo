describe('Critical User Flow E2E', () => {
  it('handles user login, document upload, and RAG query', () => {
    // 1. Visit the login page
    cy.visit('http://localhost:5173/login');

    // 2. Perform login (assuming a test user with credentials)
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    // Assert successful login (e.g., redirect to dashboard)
    cy.url().should('include', '/dashboard');

    // 3. Navigate to document upload page
    cy.get('a[href="/documents"]').click(); // Assuming a link to documents page
    cy.url().should('include', '/documents');

    // 4. Upload a document (assuming a simple file input)
    const fileName = 'test_document.pdf';
    cy.fixture(fileName, 'binary').then(fileContent => {
      cy.get('input[type="file"]').attachFile({
        fileContent,
        fileName,
        mimeType: 'application/pdf'
      });
    });
    cy.get('button[data-test="upload-button"]').click(); // Assuming an upload button

    // Assert document upload success (e.g., success message, document listed)
    cy.contains('Document uploaded successfully').should('be.visible');
    cy.contains(fileName).should('be.visible');

    // 5. Navigate to RAG query page (assuming document processing is fast or mocked)
    cy.get('a[href="/rag"]').click(); // Assuming a link to RAG page
    cy.url().should('include', '/rag');

    // 6. Perform a RAG query
    cy.get('textarea[data-test="query-input"]').type('What is in the test document?');
    cy.get('button[data-test="query-submit"]').click();

    // Assert RAG query response
    cy.get('div[data-test="rag-response"]').should('not.be.empty');
    cy.get('div[data-test="rag-response"]').contains('answer from document').should('be.visible');
  });
});
