Feature: GET users - lista paginada
  As a QA
  I want to fetch users
  So that I can validate status, headers, corpo e contrato

  Background:
    Given the API base url

  @smoke @get
  Scenario: Status 200, tempo e headers válidos
    When I send a GET request to "/api/users?page=2"
    Then the response status code should be 200
    And the response time should be less than 1500 ms
    And the response header "Content-Type" should contain "application/json"

  @contract @get
  Scenario: Corpo segue o contrato (lista de usuários)
    When I send a GET request to "/api/users?page=2"
    Then the response body should match schema "api_contracts/users_list.schema.json"

  @body @get
  Scenario: Campos principais do corpo existem e têm tipos esperados
    When I send a GET request to "/api/users?page=2"
    Then the json path "$.page" should be an integer
    And the json path "$.data" should be an array
    And the json path "$.data[0].email" should contain "@"
