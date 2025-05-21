// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('login', (email) => {
    // Skriv in e-postadress
    cy.get('#email').type(email);

    // Tryck på submit-knappen
    cy.get('input[type="submit"]').click();

    // Vänta tills användaren är inloggad (t.ex. att /login inte finns i URL)
    cy.url().should('not.include', '/login');
});

Cypress.Commands.add('ensureTaskExists', () => {
  cy.get('body').then(($body) => {
    const taskElements = $body.find('.container-element, .task-item, [data-testid="task"]');
    
    if (taskElements.length === 0) {
      cy.get('input[placeholder*="Task"], input[name="title"], .task-input').first()
        .type('Test Task för Todo-hantering');
      cy.get('button').contains(/add|create|submit/i).click();
      cy.wait(1000);
    }
  });
});