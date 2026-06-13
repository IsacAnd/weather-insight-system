
# WIS - Melhorias do Sistema

## 1. Frontend

### RF-001 - Implementação de Cache de Requisições

**Descrição:**  
Implementar cache de requisições no frontend utilizando React Query para reduzir chamadas redundantes ao backend e melhorar o desempenho da aplicação.

**Critérios de Aceitação:**
- Requisições de consulta devem utilizar cache gerenciado pelo React Query.
- Dados previamente carregados devem ser reutilizados enquanto o cache estiver válido.
- O cache deve ser invalidado automaticamente quando houver atualização dos dados relacionados.
- O tempo de validade do cache deve ser configurável.

**Prioridade:** Alta

---

### RF-002 - Geração de Insights Sob Demanda

**Descrição:**  
A geração de insights por Inteligência Artificial deve ocorrer somente mediante solicitação explícita do usuário.

**Critérios de Aceitação:**
- Nenhuma requisição para o serviço de IA deve ser executada automaticamente durante o carregamento da página.
- O usuário deve iniciar a geração do insight por meio de um botão ou ação equivalente.
- O sistema deve exibir um indicador visual de processamento durante a execução da requisição.
- O resultado gerado deve ser exibido ao término do processamento.

**Prioridade:** Alta

---

### RF-003 - Atualização Automática de Logs

**Descrição:**  
Implementar atualização automática dos logs exibidos na interface sem necessidade de recarregamento manual da página.

**Critérios de Aceitação:**
- A sincronização dos logs deve ocorrer automaticamente a cada 60 segundos.
- A atualização deve ocorrer em segundo plano.
- O estado atual da interface deve ser preservado durante a atualização.
- Em caso de falha, os dados já exibidos devem permanecer disponíveis para o usuário.

**Prioridade:** Média

---

### RNF-001 - Desempenho

**Descrição:**  
As melhorias implementadas devem reduzir o número de requisições desnecessárias ao backend e aos serviços de IA.

**Critérios de Aceitação:**
- O número de chamadas repetidas para os mesmos dados deve ser reduzido através do uso de cache.
- O serviço de IA deve ser acionado apenas mediante interação do usuário.
- A atualização periódica dos logs não deve impactar significativamente a experiência de navegação.



## 2. Backend

### RF-004 - Cache de Insights

**Descrição:**  
Implementar um mecanismo de cache para os insights gerados pela Inteligência Artificial, reduzindo chamadas repetidas à API e melhorando o tempo de resposta do sistema.

**Critérios de Aceitação:**
- O sistema deve gerar um identificador único (hash) com base nos dados utilizados para gerar o insight.
- Antes de realizar uma nova chamada à IA, o sistema deve verificar se já existe um insight armazenado para o mesmo hash.
- Caso exista um resultado em cache, o sistema deve retornar o insight armazenado sem realizar uma nova chamada à API.
- O mecanismo de cache deve possuir política de expiração configurável.

**Prioridade:** Alta

---

### RF-005 - Timeout e Monitoramento de Chamadas Externas

**Descrição:**  
Implementar controle de tempo limite para chamadas à API da DeepSeek, garantindo maior resiliência da aplicação em casos de lentidão ou indisponibilidade do serviço externo.

**Critérios de Aceitação:**
- Todas as requisições para a API da DeepSeek devem possuir timeout configurado.
- Quando o tempo limite for excedido, a requisição deve ser encerrada automaticamente.
- O sistema deve registrar informações sobre a falha em logs.
- Um alerta deve ser gerado para informar indisponibilidade ou degradação do serviço externo.
- O sistema deve retornar uma mensagem de erro adequada ao cliente consumidor da API.

**Prioridade:** Alta

---

### RF-006 - Rate Limiting da API

**Descrição:**  
Implementar controle de taxa de requisições utilizando o Throttler do NestJS para proteger a API contra abuso, excesso de chamadas e possíveis ataques de negação de serviço.

**Critérios de Aceitação:**
- O número máximo de requisições por usuário ou endereço IP deve ser configurável.
- Requisições que excederem o limite definido devem ser bloqueadas temporariamente.
- O sistema deve retornar o código HTTP apropriado para limite excedido.
- Os eventos de bloqueio devem ser registrados para auditoria e monitoramento.

**Prioridade:** Média

---

### RF-007 - Validação de Dados de Entrada

**Descrição:**  
Implementar DTOs e mecanismos de validação para garantir a integridade e consistência dos dados recebidos pela API.

**Critérios de Aceitação:**
- Todas as rotas que recebem dados de entrada devem utilizar DTOs.
- Campos obrigatórios devem ser validados antes do processamento da requisição.
- Tipos de dados inválidos devem ser rejeitados automaticamente.
- Mensagens de erro devem indicar claramente os campos inválidos.
- Requisições inválidas não devem chegar à camada de negócio da aplicação.

**Prioridade:** Alta

---

### RNF-002 - Confiabilidade e Resiliência

**Descrição:**  
O backend deve ser capaz de lidar adequadamente com falhas de serviços externos e requisições inválidas sem comprometer a estabilidade da aplicação.

**Critérios de Aceitação:**
- Falhas em serviços externos não devem causar indisponibilidade da API.
- Todas as exceções devem ser tratadas e registradas em logs.
- O sistema deve fornecer mensagens de erro padronizadas para o cliente.
- Os mecanismos de cache e rate limiting devem contribuir para a estabilidade do ambiente em situações de alta carga.

## 3. Producer

### RF-008 - Reconexão Automática com RabbitMQ

**Descrição:**  
Implementar um mecanismo de reconexão automática no Producer para garantir a continuidade da comunicação com o RabbitMQ em casos de reinicialização do broker, falhas temporárias de rede ou perda inesperada da conexão.

**Critérios de Aceitação:**
- O Producer deve detectar automaticamente a perda de conexão com o RabbitMQ.
- O sistema deve tentar restabelecer a conexão sem necessidade de intervenção manual.
- As tentativas de reconexão devem ocorrer em intervalos configuráveis.
- O processo de reconexão deve continuar até que a conexão seja restabelecida com sucesso.
- Eventos de desconexão, falha de reconexão e reconexão bem-sucedida devem ser registrados em logs.
- Após a reconexão, o Producer deve voltar a publicar mensagens normalmente.
- O sistema não deve exigir reinicialização da aplicação para recuperar a comunicação com o broker.

**Prioridade:** Alta

---

### RNF-003 - Disponibilidade da Mensageria

**Descrição:**  
O serviço Producer deve manter alta disponibilidade e tolerância a falhas relacionadas ao sistema de mensageria, minimizando interrupções causadas por indisponibilidade temporária do RabbitMQ.

**Critérios de Aceitação:**
- Falhas temporárias do RabbitMQ não devem causar encerramento da aplicação.
- O sistema deve recuperar automaticamente a comunicação após a disponibilidade do broker ser restabelecida.
- O tempo de indisponibilidade percebido pelo sistema deve ser minimizado através do mecanismo de reconexão automática.
- Todas as ocorrências relacionadas à conexão devem ser registradas para fins de monitoramento e auditoria.

## 4. Worker

### RF-009 - Implementação de Dead Letter Queue (DLQ)

**Descrição:**  
Implementar uma Dead Letter Queue (DLQ) para armazenar mensagens que não puderem ser processadas com sucesso pelo Worker após o esgotamento das tentativas de reprocessamento. O objetivo é evitar perda de mensagens e permitir análise posterior das falhas.

**Critérios de Aceitação:**
- Mensagens que falharem no processamento devem ser redirecionadas para uma fila de DLQ após atingir o limite máximo de tentativas.
- A DLQ deve armazenar a mensagem original juntamente com informações sobre o erro ocorrido.
- O sistema deve registrar em logs o motivo do envio da mensagem para a DLQ.
- Mensagens presentes na DLQ não devem ser descartadas automaticamente.
- Deve ser possível identificar e consultar mensagens que foram encaminhadas para a DLQ.

**Prioridade:** Alta

---

### RF-010 - Política de Retry para Processamento de Mensagens

**Descrição:**  
Implementar uma política de reprocessamento automático para mensagens que apresentarem falhas temporárias durante o processamento, aumentando a resiliência do sistema e reduzindo falhas ocasionais causadas por indisponibilidade momentânea de serviços dependentes.

**Critérios de Aceitação:**
- O Worker deve realizar novas tentativas de processamento quando ocorrer uma falha recuperável.
- O número máximo de tentativas deve ser configurável.
- O intervalo entre as tentativas deve ser configurável.
- Cada tentativa de reprocessamento deve ser registrada em logs.
- Após atingir o limite máximo de tentativas sem sucesso, a mensagem deve ser encaminhada para a DLQ.
- O sistema deve evitar loops infinitos de reprocessamento.

**Prioridade:** Alta

---

### RF-011 - Identificação Única de Mensagens

**Descrição:**  
Implementar um identificador único (Message ID) para todas as mensagens publicadas e processadas pelo sistema, permitindo rastreabilidade completa durante o fluxo de mensageria.

**Critérios de Aceitação:**
- Toda mensagem enviada pelo Producer deve possuir um Message ID único.
- O Message ID deve acompanhar a mensagem durante todo o ciclo de processamento.
- O identificador deve ser registrado nos logs do Producer e do Worker.
- Deve ser possível localizar eventos relacionados a uma mensagem específica através do Message ID.
- O Message ID deve ser incluído em mensagens de erro e eventos de auditoria.

**Prioridade:** Alta

---

### RNF-004 - Rastreabilidade e Auditoria de Mensagens

**Descrição:**  
O sistema de mensageria deve fornecer mecanismos que permitam rastrear o ciclo de vida completo de cada mensagem, facilitando monitoramento, auditoria e diagnóstico de problemas.

**Critérios de Aceitação:**
- Todas as etapas do processamento devem registrar o Message ID correspondente.
- Falhas, tentativas de reprocessamento e envios para a DLQ devem ser auditáveis.
- Deve ser possível identificar rapidamente o status de uma mensagem através dos registros do sistema.
- Os logs devem conter informações suficientes para análise e investigação de falhas.