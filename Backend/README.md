# Backend da Aula 9 — arquivos locais

O repositório contém este guia, um inicializador e um exemplo de conexão. Copie os seguintes arquivos **do material fornecido na aula** para esta pasta:

- `BackendEstudoAPI.exe`
- `BackendEstudoAPI.dll`
- `BackendEstudoAPI.deps.json`
- `BackendEstudoAPI.runtimeconfig.json`
- `BackendEstudoAPI.staticwebassets.endpoints.json`
- `MySqlConnector.dll`

`BackendEstudoAPI.pdb`, `banco_estudo.sql` e `Source/` também acompanham o material, mas não são necessários para executar o servidor compilado. Esses arquivos recebidos não são publicados por padrão; o `.gitignore` os mantém locais. O ZIP completo entregue nesta conversa já inclui os arquivos fornecidos.

Execute `iniciar_backend.bat` com ASP.NET Core Runtime 10 x64 instalado. O diagnóstico fica em `http://localhost:5080`. Sem MySQL disponível, o servidor usa JSON local. Com MySQL, cria `fecap_estudo` e as tabelas conforme o comportamento do backend da aula.

Para configurar uma conexão diferente, copie `mysql_config.exemplo.txt` para `mysql_config.txt` e edite a cópia local. O exemplo tem senha vazia e não contém a configuração pessoal do computador.

O código Python integra as rotas originais; não é necessário recompilar o backend para usar os binários fornecidos.
