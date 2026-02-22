# Sistema de Permuta de Aulas

Sistema web desenvolvido em **Python + Django + SQLite** para apoiar a gestão de **permutas e reposições de aulas** entre professores de uma instituição de ensino.

O sistema foi construído como atividade da disciplina **Laboratório de Software II**, seguindo documentos de **Especificação de Requisitos**, **Documento de Arquitetura** e o modelo de dados **MER/DER** do banco.

---

## Objetivo do sistema

Permitir que:

- Professores solicitem **permutas de aulas** entre si;
- Registrem a **data da reposição** dessas aulas;
- O professor substituto possa **confirmar que concorda** com a permuta;
- A coordenação tenha **visão geral** das permutas realizadas, especialmente das que ainda não possuem reposição registrada.

---

## Papéis de usuário

### 1. Coordenador / Admin (usuário `is_staff` / superusuário)

- Acessa o **Django Admin**;
- Cadastra e gerencia:
  - Professores,
  - Disciplinas,
  - Turmas,
  - Horários de aula;
- Consulta permutas e reposições;
- Acompanha permutas **sem reposição registrada** em uma visão específica.

### 2. Professor

- Faz **login** no sistema;
- Consulta seus **horários de aula**;
- **Solicita permuta** de uma aula sua, indicando:
  - data da aula a ser permutada,
  - professor substituto,
  - motivo;
- Após registrar a permuta, **registra a data da reposição**;
- Acompanha suas solicitações em **"Minhas solicitações de permuta"**.

### 3. Professor Substituto

- Visualiza a lista de **permutas em que foi indicado como substituto**;
- Só pode **confirmar a permuta** depois que o professor solicitante **registrar a reposição**;
- Ao confirmar, a permuta é marcada como **APROVADA**, registrando quem decidiu e a data da decisão.

---

## Tecnologias utilizadas

- **Linguagem:** Python 3.x  
- **Framework web:** Django  
- **Banco de dados:** SQLite (padrão do Django para desenvolvimento)  
- **Template engine:** Django Templates  
- **Controle de versão:** Git + GitHub  

---

## Requisitos para executar o projeto

- Python 3 instalado  
- Git instalado  
- (Opcional, mas recomendado) Ambiente virtual (`venv`)

---

## Como rodar o projeto localmente

Abaixo, um passo a passo típico em ambiente Windows (PowerShell), considerando que você vai clonar o repositório do GitHub.

1. Clonar o repositório

```powershell
git clone https://github.com/daianesr35/permuta_novo.git
cd permuta_novo

2. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

3. Instalar as dependências
pip install django

4. Aplicar as migrações do banco
python manage.py migrate

5. Criar um superusuário (admin/coordenação)
python manage.py createsuperuser

Informe:
nome de usuário (ex: admin),
e-mail (opcional),
senha.

6. Executar o servidor de desenvolvimento
python manage.py runserver

Depois, acesse no navegador:
Sistema: http://127.0.0.1:8000/
Admin Django: http://127.0.0.1:8000/admin/