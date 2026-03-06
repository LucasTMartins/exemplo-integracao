# Exemplo de Integração de APIs

Este projeto tem como objetivo demonstrar o conceito de **integração estrutural**, com duas APIs distintas (desenvolvidas com tecnologias diferentes) acessando e compartilhando as informações no mesmo banco de dados.

## Estrutura do Projeto

* `api-nodejs`: Uma API construída com **Node.js** e Express, responsável por parte da lógica e manipulação de dados.
* `api-python`: Uma API construída com **Python** e FastAPI, atuando com seu próprio conjunto de rotas de integração.
* `postgres`: Configuração inicial para criar e disponibilizar o repositório central de dados acessado por ambas as apis.

Esta configuração exemplifica como diferentes tecnologias e frameworks podem coexistir no mesmo ecossistema, separando responsabilidades, porém mantendo uma base de dados unificada por baixo.
