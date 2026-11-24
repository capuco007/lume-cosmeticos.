# Lumé Cosméticos

Projeto de portfólio: loja virtual demonstrativa de cosméticos, desenvolvida com Python, Flask, SQLite, HTML e CSS.

## Funcionalidades

- Catálogo demonstrativo de produtos.
- Cadastro de cliente com nome, e-mail e telefone.
- Login e logout.
- Senhas armazenadas com hash usando Werkzeug.
- Área do cliente.
- Banco de dados SQLite criado automaticamente na primeira execução.

## Tecnologias

- Python 3
- Flask
- SQLite
- HTML5 e CSS3
- Jinja2

## Executar localmente (Windows)

1. Instale Python 3.10 ou superior: https://www.python.org/downloads/
2. Abra o terminal dentro desta pasta.
3. Crie e ative um ambiente virtual:

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Instale as dependências:

   ```bash
   py -m pip install -r requirements.txt
   ```

5. Inicie:

   ```bash
   py app.py
   ```

6. Acesse http://127.0.0.1:5000

O arquivo `lume.db` é criado localmente e está listado no `.gitignore`, portanto não será enviado ao GitHub.

## Publicar o código no GitHub

1. Crie um repositório no GitHub, por exemplo `lume-cosmeticos`.
2. Extraia esta pasta no computador.
3. No terminal, dentro da pasta do projeto, execute:

   ```bash
   git init
   git add .
   git commit -m "Adiciona projeto Lumé Cosméticos"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/lume-cosmeticos.git
   git push -u origin main
   ```

   Troque `SEU-USUARIO` pelo seu usuário do GitHub.

## Importante: GitHub e hospedagem

O GitHub armazena e apresenta o código-fonte, ótimo para seu portfólio. Porém, **GitHub Pages não executa aplicações Python/Flask nem fornece banco SQLite para o site**. Para deixar esta versão com cadastro e login funcionando publicamente, será necessário publicar o backend Flask em uma plataforma de hospedagem compatível e configurar um banco persistente.

Para uma demonstração pública sem backend, pode-se publicar uma versão estática separada, mas o cadastro/login real não funcionará nela.

## Segurança

Este projeto é uma demonstração de portfólio, não uma loja pronta para receber dados reais ou pagamentos. Antes de produção:
- configure `SECRET_KEY` forte por variável de ambiente;
- desative `debug`;
- use HTTPS;
- adicione proteção CSRF e limitação de tentativas de login;
- configure armazenamento persistente e backups;
- crie política de privacidade e tratamento adequado dos dados pessoais.

Nunca envie `lume.db`, senhas, tokens ou arquivos `.env` para o repositório.
