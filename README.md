# Gerenciamento de Novatos

Sistema web para registrar e acompanhar problemas de acesso enfrentados por novatos durante o turno de treinamento.

## Como funciona

- **Instrutores/novatos** preenchem um formulário público relatando o problema encontrado (nome do novato, turno, instrutor, sistema afetado, tipo de problema e observações).
- **A gerente** acessa um painel protegido por senha, onde visualiza todos os relatos enviados, marca cada um como "Resolvido" (ou reabre), e ao final do turno usa o botão **Finalizar turno** para apagar todos os registros e recomeçar do zero.

## Funcionalidades

- Formulário de envio de relatos, sem necessidade de login
- Painel administrativo protegido por senha
- Marcação de relatos como resolvidos/pendentes
- Encerramento de turno com limpeza total dos dados
- Persistência dos dados em banco SQLite até o encerramento manual do turno

## Tecnologias

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/)

## Rodando localmente

Pré-requisitos: Python 3 instalado.

```bash
pip install -r requirements.txt
python main.py
```

O servidor sobe em `http://localhost:5000`.

Por padrão, sem nenhuma configuração extra, o login do painel (`/painel`) usa uma senha de teste local. Para definir a senha real e uma chave de sessão própria, configure as variáveis de ambiente `SENHA_PAINEL` e `CHAVE_SECRETA` antes de rodar o programa.

## Estrutura do projeto

```
main.py               # Rotas e lógica da aplicação Flask
templates/             # Páginas HTML (Jinja2)
static/style.css       # Estilos
requirements.txt        # Dependências Python
```

## Licença

Este projeto está sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
