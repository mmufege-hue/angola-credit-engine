# Publicação no Streamlit Community Cloud

## 1. Subir o projecto para GitHub

Crie um repositório e coloque **todo o conteúdo desta pasta** na raiz do repositório.

## 2. Publicar

No Streamlit Community Cloud, crie uma nova aplicação e seleccione:

- Repository: o seu repositório GitHub
- Branch: `main`
- Main file path: `app.py`

O ficheiro `requirements.txt` instala as dependências e `.python-version` pede Python 3.12.

## 3. Segurança

Este projecto é um protótipo. Não coloque NIFs, demonstrações financeiras, credenciais bancárias ou outros dados reais no repositório.

O SQLite é local e efémero no ambiente cloud. Para persistência real, substitua `database.py` por PostgreSQL ou outro serviço gerido.

## 4. Limitações de crédito

O score é baseado em regras transparentes. O módulo de ML usa dados sintéticos e não deve ser usado para aprovação real. A ECL do dashboard é apenas uma aproximação pedagógica.
