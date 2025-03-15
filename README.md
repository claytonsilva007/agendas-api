# Documentação do Projeto Agenda-API

## 1. Visão Geral

O **Agenda-API** é um sistema composto por dois projetos principais: uma API construída com Django REST Framework (DRF) e uma aplicação web desenvolvida com Django. O objetivo é oferecer um gerenciamento de agendas, permitindo que usuários criem, visualizem, editem e excluam agendas de forma intuitiva. A API fornece os dados e a lógica de backend, enquanto o frontend web oferece uma interface amigável para interação com esses dados.

A solução é conteinerizada com Docker e utiliza Nginx como proxy reverso para gerenciar requisições entre a API e o frontend, além de um banco de dados PostgreSQL para persistência. A API inclui autenticação baseada em tokens JWT para segurança.

---

## 2. Objetivo e Escopo

### 2.1. Backend (API)
- Fornecer uma API RESTful para gerenciamento de agendas com operações CRUD (criar, ler, atualizar, deletar).
- Atributos das agendas:
  - `id`: Identificador único.
  - `titulo`: String descritiva da agenda.
- Implementar autenticação baseada em tokens JWT para proteger os endpoints.

### 2.2. Frontend (Webapp)
- Desenvolver uma interface web responsiva para interação com a API.
- Funcionalidades:
  - Criar, visualizar, editar e excluir agendas.
  - Experiência de usuário intuitiva e simples.

---

## 3. Arquitetura do Projeto

### 3.1. Estrutura Geral
O projeto é dividido em dois serviços principais:
- **API**: Implementada com Django REST Framework, localizada em `./api`. Responsável pela lógica de negócios, manipulação de dados e autenticação JWT.
- **Webapp**: Interface web construída com Django, localizada em `./webapp`. Consome a API e apresenta os dados ao usuário.

Esses serviços são integrados por meio de uma arquitetura baseada em contêineres Docker, com os seguintes componentes adicionais:
- **Nginx**: Proxy reverso que redireciona requisições para a API (`/api/`) ou para o frontend (`/webagenda/`).
- **PostgreSQL**: Banco de dados relacional para persistência de dados.

### 3.2. Estrutura de Diretórios
```
agenda-api/
├── api/                  # Projeto Django REST Framework (API)
│   ├── agenda/           # Aplicação DRF para lógica de agendas
│   ├── core/             # Configurações do projeto DRF
│   ├── Dockerfile        # Configuração do contêiner da API
│   ├── entrypoint.sh     # Script de inicialização com superusuário
│   ├── manage.py         # Gerenciador do Django
│   └── requirements.txt  # Dependências Python
├── webapp/               # Projeto Django (Frontend)
│   ├── core/             # Configurações do projeto Django
│   ├── entrypoint.sh     # Script de inicialização
│   ├── webagenda/        # Aplicação Django para interface
│   │       └── templates/    # Templates HTML
│   │       └── webagenda/      
│   └── Dockerfile        # Configuração do contêiner do frontend
│   ├── manage.py         # Gerenciador do Django
│   └── requirements.txt  # Dependências Python
├── docker-compose.yml    # Configuração dos serviços Docker
├── nginx.conf            # Configuração do Nginx
└── .env                  # Variáveis de ambiente
```

### 3.3. Fluxo de Comunicação
1. O usuário acessa o sistema via `http://localhost`.
2. O Nginx redireciona:
   - Requisições para `/api/` → Serviço `api` (porta 8000).
   - Requisições para `/webagenda/` → Serviço `webagenda` (porta 8001).
3. A API, protegida por JWT, interage com o banco de dados PostgreSQL para gerenciar as agendas.
4. O frontend consome a API e exibe os dados nos templates HTML.

### 3.4. Premissas Adotadas
- **Modularidade**: Separação clara entre backend (API) e frontend (webapp).
- **Segurança**: Uso de autenticação JWT para proteger endpoints da API.
- **Simplicidade**: Uso de ferramentas amplamente conhecidas (Docker, Nginx, PostgreSQL) para facilitar implementação e manutenção.
- **Portabilidade**: Solução conteinerizada, independente de IDEs ou sistemas operacionais específicos.
- **Escalabilidade**: Arquitetura baseada em serviços permite ajustes futuros, como adicionar novos contêineres.

---

## 4. Requisitos Implementados
- **Gerenciamento de Agendas**: Operações CRUD disponíveis na API e refletidas no frontend.
- **Atributos da Agenda**: `id` e `titulo` conforme especificado.
- **Autenticação**: Tokens JWT implementados na API para segurança.
- **Responsividade**: Templates HTML projetados para adaptação a diferentes dispositivos (a ser ajustado conforme CSS implementado via Bootstrap).

---

## 5. Guia de Implementação

### 5.1. Pré-requisitos
- Docker e Docker Compose instalados.
- Arquivo `.env` configurado com as variáveis abaixo:
  ```
  POSTGRES_USER=seu_usuario
  POSTGRES_PASSWORD=sua_senha
  POSTGRES_DB=nome_do_banco
  ```
- Caso o arquivo `.env` não seja editado, as informações padrão serão utilizadas.

### 5.2. Passo a Passo
1. **Clone o Repositório**
   ```bash
   git clone https://github.com/claytonsilva007/agendas-api.git
   cd agenda-api
   ```
   ![Clonando o repositório]([https://drive.google.com/uc?export=download&id=ID_DO_ARQUIVO](https://drive.google.com/uc?export=download&id=1oqsHp-vwtc_mQRlu5Tj3jzqteKBpz0PY))
    
2. **Configure o Arquivo `.env`**
   - Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias (veja exemplo acima).

3. **Construa e Inicie os Contêineres**
   ```bash
   docker-compose up --build
   ```
   - Isso construirá as imagens da API, webapp, Nginx e PostgreSQL e iniciará os serviços. Durante a inicialização da API, o script `entrypoint.sh` executará:
     - `python manage.py migrate`: Aplica as migrações do banco de dados.
     - `python manage.py collectstatic`: Coleta arquivos estáticos.
     - `python manage.py createsuperuser`: Cria um superusuário com credenciais padrão (`admin`, `admin@example.com`, `admin123`), ignorando erros se já existir.

4. **Acesse o Sistema**
   - API: `http://localhost/api/agenda/` (requer token JWT para endpoints protegidos).
   - Acesse `http://localhost/api/admin/` e faça login com as credenciais de superusuário (usuário: admin,  password: admin123) para visualizar os dados.
   - Frontend: `http://localhost/webagenda/`.
   - Caso você não esteja logado, a página de login será apresentada e você deverá informar as credenciais de superusuário (usuário: admin,  password: admin123) para gerenciar a agenda.
   - O Nginx redireciona automaticamente requisições da raiz (`/`) para `/api/agenda/`.

5. **Parar os Contêineres**
   ```bash
   docker-compose down
   ```
   - Para remover os volumes (dados do banco), use:
     ```bash
     docker-compose down -v
     ```

### 5.3. Observações
- Certifique-se de que as portas 80 (Nginx) e 5234 (PostgreSQL externo) estejam livres.
- Para obter um token JWT, acesse `/api/token/` com as credenciais do superusuário (`admin`, `admin123`) via POST com `username` e `password`.

---

## 6. Próximos Passos (Opcional)
- Adicionar autenticação no frontend para integração com JWT.
- Implementar testes unitários para API e webapp.
- Otimizar o frontend com CSS/JavaScript para maior responsividade.

---
