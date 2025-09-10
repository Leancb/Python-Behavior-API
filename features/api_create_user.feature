Feature: POST create user
  Validar criação de usuário e mensagem/corpo/contrato

  Background:
    Given the API base url

  @post @contract
  Scenario: Criar usuário com sucesso (201) e validar contrato
    Given the request body:
      """
      {
        "name": "morpheus",
        "job": "leader"
      }
      """
    When I send a POST request to "/api/users"
    Then the response status code should be 201
    And the json path "$.name" should equal "morpheus"
    And the json path "$.job" should equal "leader"
    And the response body should match schema "api_contracts/user_created.schema.json"
    And the json path "$.id" should not be empty
    And the json path "$.createdAt" should not be empty

  @message @post
  Scenario: Mensagem/conteúdo esperado em campo
    Given the request body:
      """
      {"name":"Neo","job":"The One"}
      """
    When I send a POST request to "/api/users"
    Then the response status code should be 201
    And the json path "$.name" should equal "Neo"
    And the response should contain text "createdAt"
