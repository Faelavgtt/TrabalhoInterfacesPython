# Trabalho Interfaces Python

Sistema simples feito em Python com PyQt5 para cadastro de clientes, carros,
servicos e ordens de servico de uma oficina.

## Como rodar

```bash
python src/main.py
```

## Login de teste

```text
usuario: admin
senha: admin
```

## Organizacao dos arquivos

- `src/main.py`: arquivo principal, usado apenas para iniciar o sistema.
- `src/config.py`: caminhos do projeto, tela `.ui` e banco de dados.
- `src/database.py`: conexao com SQLite e criacao das tabelas.
- `src/ui_helpers.py`: funcoes auxiliares para mensagens, tabelas e combos.
- `src/auth_controller.py`: etapa de login.
- `src/cliente_controller.py`: cadastro, edicao, listagem e exclusao de clientes.
- `src/carro_controller.py`: cadastro, edicao, listagem e exclusao de carros.
- `src/servico_controller.py`: cadastro, edicao, listagem e exclusao de servicos.
- `src/ordem_servico_controller.py`: criacao, edicao, listagem e exclusao de ordens.
- `src/sistema.py`: junta as etapas, conecta botoes da tela e carrega os dados.
