# py-siafi-efd

Um projeto de ciência de dados, que auxilia na análise de planilhas siafi e efd.

Utiliza Pyscript para possibilitar o emprego de Pandas diretamente no frontend. 
Uma orientação a eventos bem definida, ao invés da manipulação de um estado reativo, pode ser bem mais fácil de entender.
Usa-se o padrao pub_sub para controlar os componentes html dinâmicos, cujos templates estão em 'templates'. O html estático se localiza no próprio 'index.html'.
O 'main.py' carrega os listeners, que são funções decoradas em python com 'when' de Pyscript.

## Índice

- [Instalação](#instalação): basta clonar e utilizar a extensão live server;
- [Uso](#uso): Fazer o upload de ambas as planilhas;
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)
