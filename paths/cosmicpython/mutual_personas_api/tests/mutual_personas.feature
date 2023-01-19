# Created by alvar at 14/1/23
Feature: Add a new socie
  As a user I send a graphql post request
  and a user is created in the DB and returned as response

  Scenario: Add user happy path
    Given a user with permissions
    When post a graphql mutation
    Then a new associated is created in DB
    Then the mutation responds with the new socie