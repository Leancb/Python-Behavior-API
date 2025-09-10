Feature: Casos negativos
  Verificar mensagens, status e corpo em erros

  Background:
    Given the API base url

  @negative @auth
  Scenario: Login sem senha retorna 400 e mensagem
    Given the request body:
      """
      {"email":"peter@klaven"}
      """
    When I send a POST request to "/api/login"
    Then the response status code should be 400
    And the response should contain text "Missing password"
