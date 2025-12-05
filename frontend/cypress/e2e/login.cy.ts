describe('Login', () => {
  it('loads login page', () => {
    cy.visit('/login')
    cy.contains('Sign in')
  })
})
