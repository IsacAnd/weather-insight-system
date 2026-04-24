# Itens de Configuração Mapeados

- **ID:** IC-01
  - **Descrição:** Backend Service (NestJS) - API principal para persistência e integração com IA.
  - **Repositório:** GitHub
  - **Owner:** @IsacAnd
  - **Branch padrão:** main
  - **Tags:** v1.0.0, stable

- **ID:** IC-02
  - **Descrição:** Frontend Dashboard (React) - Interface para visualização dos dados climáticos.
  - **Repositório:** GitHub
  - **Owner:** 
  - **Branch padrão:** main
  - **Tags:** v1.0.0, stable

- **ID:** IC-03
  - **Descrição:** Weather Data Producer - Script Python para coleta de dados da API Open-Meteo.
  - **Repositório:** GitHub
  - **Owner:** @IsacAnd
  - **Branch padrão:** main
  - **Tags:** v1.0.0, stable

- **ID:** IC-04
  - **Descrição:** Weather Data Worker - Script Go para processamento de mensagens do RabbitMQ.
  - **Repositório:** GitHub
  - **Owner:** @IsacAnd
  - **Branch padrão:** main
  - **Tags:** v1.0.0, stable

- **ID:** IC-05
  - **Descrição:** Manifestos de Dependência - Arquivos `package.json`, `requirements.txt` e `go.mod`.
  - **Repositório:** GitHub
  - **Owner:** 
  - **Branch padrão:** main
  - **Tags:** v1.0.0

- **ID:** IC-06
  - **Descrição:** Manual de Operação - Instruções de instalação e deploy no `README.md`.
  - **Repositório:** GitHub
  - **Owner:** 
  - **Branch padrão:** main
  - **Tags:** v1.0.0

- **ID:** IC-07
  - **Descrição:** Documentação de Endpoints - Tabela de rotas e contratos da API no `API.md`.
  - **Repositório:** GitHub
  - **Owner:** 
  - **Branch padrão:** main
  - **Tags:** v1.0.0

- **ID:** IC-08
  - **Descrição:** Especificação de Requisitos - Definição das funcionalidades e fluxos de dados.
  - **Repositório:** GitHub
  - **Owner:** @JoanaSthefanny
  - **Branch padrão:** main
  - **Tags:** v1.0.0

- **ID:** IC-09
  - **Descrição:** Docker Compose Config - Orquestração de containers, redes e volumes.
  - **Repositório:** GitHub
  - **Owner:** 
  - **Branch padrão:** main
  - **Tags:** v1.0.0

- **ID:** IC-10
  - **Descrição:** Plano de Gerência (Lista de ICs) - Documento mestre de organização da GCS.
  - **Repositório:** GitHub
  - **Owner:** @JoanaSthefanny
  - **Branch padrão:** main
  - **Tags:** v1.0.0

---

# Controle de Mudanças via Git

Para garantir a integridade da **Baseline** do projeto, foi utlizado a marcação de versões (tags) para congelar estados estáveis do sistema.

### Marcação de Versões:
```bash
# Comando para criar a tag da Baseline inicial
git tag -a v1.0.0 -m "Release: Baseline inicial de GCS - Todos os ICs homologados"  
git push origin --tags