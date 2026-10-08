# Angola Corporate Credit Decision Engine

## Descrição do projecto
Este projecto é um protótipo profissional de motor de decisão de crédito corporativo para apoio em entrevistas e demonstrações técnicas, com foco em risco de crédito corporativo em Angola.

## Objectivo
A aplicação analisa pedidos de crédito corporativo, calcula indicadores financeiros, score de risco, cenários de stress, estimativa conceptual de PD/LGD/EAD/ECL e recomendação de crédito com condições e auditoria.

## Aviso de utilização
Este protótipo é apenas um apoio à decisão e não substitui o comité de crédito, a política interna, as metodologias regulatórias ou a aprovação institucional. Não devem ser introduzidos dados reais de clientes.

## Funcionalidades
- Entrada de pedido com dados fictícios.
- Análise financeira de liquidez, rentabilidade, alavancagem e garantia.
- Score de risco explicável com classificação A a E.
- Regras de bloqueio e recomendação.
- Stress testing em cenários base, downside e severo.
- Estimativa conceptual de PD, LGD, EAD e ECL.
- Relatório PDF em português.
- Auditoria simples e dashboard de monitorização com filtros por empresa, sector, província, classe de risco e decisão.
- Interface com tema visual consistente nas páginas da aplicação.

## Estrutura de pastas
- app.py: aplicação principal.
- pages/: páginas Streamlit da aplicação.
- data/: ficheiros de demonstração em CSV.
- tests/: testes unitários.

## Instalação
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
```bash
streamlit run app.py
```

### Windows
Para iniciar no Windows, execute `run_windows.bat` a partir do Explorador de Ficheiros ou do terminal. O script usa `.venv` quando disponível e, caso contrário, o Python Launcher (`py -3`).

Se o Windows bloquear DLLs ou gravações, coloque o projecto num directório de desenvolvimento não protegido (por exemplo, `C:\Users\<utilizador>\Projects\angola_credit_engine`) e instale as dependências nesse ambiente. Não desactive políticas de segurança institucionais; peça à equipa de IT uma localização ou ambiente Python aprovado.

## Dados fictícios
A aplicação utiliza apenas empresas fictícias e valores demonstrativos, incluindo:
- Kwanza Distribuição, Lda.
- Horizonte Construções, Lda.
- Luanda Import, S.A.

## Regras de score
- DSCR e liquidez são avaliados em faixas de risco.
- A dívida/EBITDA e a concentração de clientes têm pesos relevantes.
- A garantia cobre a exposição em função do valor de liquidação.
- O score final situa-se entre 0 e 100 e classifica a empresa em A a E.

## Fórmulas financeiras
- Liquidez corrente = activos correntes / passivos correntes.
- Liquidez imediata = (cash + recebíveis) / passivos correntes.
- DSCR = FC disponibilizado para serviço da dívida / serviço anual da dívida.
- Dívida/EBITDA = dívida existente / EBITDA.
- LTV = montante solicitado / garantia líquida.
- ECL = PD x LGD x EAD.

## Exemplo de demonstração
O utilizador pode carregar uma empresa de demonstração e executar a análise. O protótipo gera uma recomendação e um parecer PDF.

## Limitações
- O módulo ML é experimental, usa apenas dados sintéticos e não está validado para decisões reais.
- Baseado em regras transparentes e dados fictícios.
- O modelo não aprova pedidos automaticamente; o score baseado em regras mantém-se como decisão principal.
- Não substitui a metodologia interna do risco.

## Evoluções futuras
- Integração com bases de dados corporativas.
- Validação independente, monitorização e governança do modelo experimental.
- Módulo de covenants e monitorização automatizada.
- Integração com fluxos de aprovação e workflow interno.


## Publicação na Web

O projecto está preparado para **Streamlit Community Cloud**. Consulte `DEPLOY_STREAMLIT.md` para publicar através do GitHub. O entrypoint é `app.py`.

A aplicação não contém autenticação real: o selector de perfil é apenas demonstrativo. Também não deve ser usada para dados reais de clientes.
