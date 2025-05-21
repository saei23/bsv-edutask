// Description: Cypress test suite for Todo Management (Requirement R8)
describe('Todo Management (Requirement R8)', () => {
    let email = 'cypress@test.com';
    let firstName = 'Cypress';
    let lastName = 'Test';
    let userId;
  
    before(() => {
      // create user and task before running the tests
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: { email, firstName, lastName }
      }).then((res) => {
        userId = res.body._id.$oid;
  
        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: {
            userid: userId,
            title: 'Test Task',
            description: 'Cypress test task',
            url: 'dQw4w9WgXcQ',
            todos: JSON.stringify(['Initial todo'])
          }
        });
      });
    });

    beforeEach(() => {
      // log in and open the task detail view
      // this makes the following tests independent of each other
      cy.visit('/');
      cy.get('[name="email"]').type(email);
      cy.get('form').submit();
      cy.contains('Test Task').click();
      cy.get('.popup').should('exist');
      cy.get('.todo-list').should('exist');    
    });
  
    // Test cases for Requirement R8UC1 Add todo item
    describe('R8UC1: Add todo item', () => {
      it('Test 1: Add valid todo - Non-empty description, button enabled', () => {
        const description = 'Test todo item';

        // wait until the popup is visible
        cy.get('.popup').should('be.visible');

        // write description in the todo field (force due to position/styling)
        cy.get('input[placeholder="Add a new todo item"]')
          .scrollIntoView()
          .should('exist')
          .type(description, { force: true });
          
        // klick on the "Add" button (might be outside viewport → force)
        cy.get('form.inline-form input[type="submit"][value="Add"]')
          .scrollIntoView()
          .should('exist')
          .click({ force: true });
          
        // verify that the new todo item is added at the end
        cy.get('.todo-item').last().should('contain.text', description);
      });

      it('Test 2: Add button disabled on empty input - Empty description, button disabled', () => {
        // make sure we are in the popup
        cy.get('.popup').should('be.visible');
      
        // clear the input field and check that it is empty
        cy.get('input[placeholder="Add a new todo item"]')
          .scrollIntoView()
          .clear({ force: true })
          .should('have.value', '');
      
        // controll that the button is disabled according to the requirement
        cy.get('form.inline-form input[type="submit"][value="Add"]')
          .scrollIntoView()
          .should('have.attr', 'disabled'); // This line will probably fail

        // Try to click the button even if it is disabled, and verify that no new todo is added
        cy.get('.todo-item').its('length').then((initialCount) => {
          cy.get('form.inline-form input[type="submit"][value="Add"]').click({ force: true });
          cy.get('.todo-item').should('have.length', initialCount);
        });
      });
    });

    // Test cases for Requirement R8UC2 Toggle todo item status
    describe('R8UC2: Toggle todo item status', () => {
      // Local setup to ensure correct status before each test
      // This will make sure that the tests are independent of each other and it self
      beforeEach(() => {
        cy.get('.todo-item').should('exist');
    
        cy.get('.todo-item').first().as('targetItem');
    
        // for test 1, make sure the todo is active
        if (Cypress.currentTest.title.includes('active todo item')) {
          cy.get('@targetItem').find('span.checker').then($el => {
            if ($el.hasClass('checked')) {
              cy.wrap($el).click(); // make active
            }
          });
          cy.get('@targetItem').find('span.checker').should('have.class', 'unchecked');
        }
    
        // for test 2, make sure the todo is done
        if (Cypress.currentTest.title.includes('done todo item')) {
          cy.get('@targetItem').find('span.checker').then($el => {
            if (!$el.hasClass('checked')) {
              cy.wrap($el).click(); // make done
            }
          });
          cy.get('@targetItem').find('span.checker').should('have.class', 'checked');
        }
      });
    
      it('Test 1: Toggle active todo item → done', () => {
        // verify toggle to done
        cy.get('@targetItem').find('span.checker').click();
        cy.get('@targetItem').find('span.checker').should('have.class', 'checked');
      });
    
      it('Test 2: Toggle done todo item → active', () => {
        // verify toggle back to active
        cy.get('@targetItem').find('span.checker').click();
        cy.get('@targetItem').find('span.checker').should('have.class', 'unchecked');
      });
    });

    // Test cases for Requirement R8UC3 Delete todo item
    describe('R8UC3: Delete todo item', () => {
      const description = 'Todo to delete';
    
      beforeEach(() => {
        // add a todo to delete
        cy.get('input[placeholder="Add a new todo item"]')
          .scrollIntoView()
          .clear({ force: true })
          .type(description, { force: true });
    
        cy.get('form.inline-form input[type="submit"][value="Add"]')
          .click({ force: true });
    
        cy.contains(description).should('exist');
      });

      it('Test 1: Should delete the specific todo item', () => {
        // save the number of items before deletion
        cy.get('.todo-item').its('length').as('initialCount');
        
        // log items before deletion (to debug)
        cy.get('.todo-item').then((initialItems) => {
          cy.log(`Initial count: ${initialItems.length}`);
          [...initialItems].forEach((el, i) => {
            cy.log(`BEFORE - Item ${i}: "${el.innerText.trim()}"`);
          });
        });
        
        // click on the delete button of the specific todo item
        cy.contains(description)
          .parents('.todo-item')
          .find('.remover')
          .scrollIntoView()
          .should('be.visible')
          .click({ force: true });
        
        cy.wait(1000); // wait for DOM to update
        
        // log items after deletion (to debug)
        cy.get('.todo-item').then((afterItems) => {
          cy.log(`After count: ${afterItems.length}`);
          [...afterItems].forEach((el, i) => {
            cy.log(`AFTER ${i}: "${el.innerText.trim()}"`);
          });
        });
        
        // verify that the number of items has decreased
        cy.get('@initialCount').then(initialCount => {
          cy.get('.todo-item').its('length').should('be.lessThan', initialCount);
        });
        
        // verify that the specific item is no longer present
        cy.contains(description).should('not.exist');
      });

    });

    // after all tests, delete the user for cleanup, we can reuse same user
    after(() => {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${userId}`
    });
  });
});
