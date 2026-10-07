# Detecção de Anomalias Espaciais e Integridade Eleitoral

## Identificação

- **Disciplina:** Inteligência Artificial: Fundamentos e Aplicações
- **Instituição:** Universidade Federal Fluminense (UFF)
- **Professor:** João Felipe Mitre
- **Modalidade:** projeto individual

## Problema

Investigar, de forma exploratória e responsável, se padrões atípicos em resultados eleitorais agregados por seção e relatos públicos de mídia comunitária podem indicar sinais compatíveis com coação territorial ou compra de votos massiva.

O projeto considera o conflito entre a auditabilidade pública dos resultados e a proteção dos eleitores contra vigilância territorial. Uma anomalia estatística não constitui prova de crime: os resultados serão tratados como sinais para auditoria e não como classificação de pessoas, comunidades ou candidatos.

## Objetivo geral

Desenvolver um pipeline multimodal em Python que combine engenharia de atributos espaciais, detecção não supervisionada de anomalias e processamento de linguagem natural para analisar padrões eleitorais e relatos públicos, além de simular alternativas de agregação e privacidade na divulgação dos resultados.

## Objetivos específicos

1. Calcular indicadores de concentração de votos, comparecimento e variação histórica.
2. Identificar outliers espaciais e temporais em dados eleitorais agregados.
3. Classificar textos públicos em denúncia de coação, denúncia de compra de voto ou discussão política comum.
4. Cruzar resultados estatísticos e sinais textuais em nível regional, respeitando limitações de cobertura e incerteza.
5. Comparar a divulgação hipergranular com alternativas de agregação espacial e privacidade diferencial simulada.
6. Produzir uma análise técnica, ética e jurídica com resultados reproduzíveis.

## Perguntas de pesquisa

- Quais combinações de concentração de votos, comparecimento e mudança histórica produzem os maiores escores de anomalia?
- A proximidade espacial entre anomalias eleitorais e relatos públicos aparece acima do esperado por acaso?
- Como preservar a auditabilidade da totalização sem expor desnecessariamente padrões locais vulneráveis à coação?

## Dados previstos

- Resultados eleitorais e boletins de urna disponibilizados pelo TSE.
- Histórico de eleições e perfil agregado do eleitorado, quando disponível.
- Coordenadas ou endereços de locais de votação, com geocodificação documentada.
- Bases públicas e acadêmicas sobre conflitos territoriais, quando licenciadas e metodologicamente compatíveis.
- Textos e transcrições de fontes públicas, respeitando termos de uso, legislação, privacidade e direitos autorais.

A coleta de redes sociais será opcional e condicionada à disponibilidade legal e técnica. O projeto deve funcionar com um conjunto de dados local anonimizado ou sintético caso a coleta real não seja autorizada ou não seja reproduzível.

## Pipeline metodológico

### 1. Preparação e qualidade dos dados

Padronização de identificadores, tratamento de valores ausentes, documentação das fontes, verificação de cobertura e separação entre dados de desenvolvimento e avaliação.

### 2. Engenharia de atributos espaciais

Cálculo de participação, concentração, comparecimento, abstenção e variações históricas. Quando houver geometria confiável, aplicação de estatística espacial exploratória, incluindo Moran local/LISA, com registro das escolhas de vizinhança.

### 3. Detecção de anomalias

Avaliação de métodos não supervisionados, começando por regras estatísticas interpretáveis e Isolation Forest. DBSCAN ou outro método espacial poderá ser usado como análise complementar. Os módulos serão tratados como:

- **Coação compatível:** concentração extrema e espacialmente persistente, sem afirmar causalidade.
- **Compra de votos compatível:** combinação de salto histórico, comparecimento atípico e concentração localizada.

### 4. PLN

Pré-processamento de textos públicos, transcrição somente de arquivos obtidos legitimamente e classificação exploratória com modelos em português. BERTimbau e Whisper são candidatos metodológicos, mas a escolha final dependerá de recursos computacionais, licença, dados rotulados e avaliação.

### 5. Cruzamento e visualização

Integração dos escores em nível regional, mapas e gráficos com intervalos ou indicadores de incerteza. Nenhum resultado será apresentado como identificação de autores, eleitores ou comunidades criminosas.

### 6. Mitigação simulada

Comparação entre resultados por seção e versões agregadas por área, além de uma simulação de ruído calibrado. A apuração oficial não será alterada; a simulação serve apenas para discutir o compromisso entre auditabilidade, utilidade analítica e proteção contra coação.

## Ferramentas e blocos de construção

O projeto reutiliza bibliotecas consolidadas em vez de reimplementar algoritmos de análise de dados. As dependências específicas estão em [requirements.txt](requirements.txt).

- **Dados eleitorais:** `basedosdados` para consultas às tabelas tratadas, quando o acesso e a fonte forem adequados; dados brutos do TSE continuam sendo a referência de conferência.
- **Geoprocessamento:** `geopandas`, `shapely`, `libpysal` e `esda` para operações espaciais e Moran local/LISA.
- **Anomalias:** `scikit-learn` e `pyod`, começando por Isolation Forest e mantendo métodos complementares como análise de sensibilidade.
- **PLN:** `transformers` e `datasets`, com BERTimbau como candidato para classificação em português.
- **Transcrição:** `openai-whisper`, somente para arquivos obtidos legitimamente e quando o custo computacional for compatível.
- **Visualização e experimentação:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly` e Jupyter.

`Instaloader` e `google-api-python-client` não são necessários para o núcleo reprodutível e só devem ser adicionados se houver autorização, termos de uso compatíveis, credenciais e um plano de proteção de dados. O pipeline deve aceitar dados locais anonimizados ou sintéticos sem depender de raspagem de redes sociais.

O uso dessas ferramentas será descrito no relatório, incluindo versões, fontes, licenças, parâmetros e limitações. A adoção de um pacote pronto não substitui a validação dos dados, a avaliação dos modelos nem a interpretação crítica dos resultados.

## Estrutura inicial

- `src/`: pipeline executável e módulos reutilizáveis.
- `tests/`: testes automatizados.
- `data/`: dados brutos e processados; o experimento inicial é sintético.
- `outputs/`: resultados gerados localmente.
- `notebooks/`: análises exploratórias e figuras do relatório.
- `relatorio/`, `slides/` e `video/`: materiais dos entregáveis.

## Primeiro experimento

Crie um ambiente virtual e instale as dependências do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r projeto_eleitoral\requirements-dev.txt
```

Execute o experimento sintético a partir da raiz do workspace:

```powershell
python projeto_eleitoral\src\synthetic_pipeline.py
python -m pytest projeto_eleitoral\tests\test_synthetic_pipeline.py -q
```

Esse experimento não usa dados reais nem credenciais. Ele serve para validar a engenharia do pipeline antes da importação dos dados eleitorais oficiais.

## Estratégia de armazenamento e execução

O disco `D:` foi verificado em 07/10/2026 e tinha aproximadamente 920 GB livres. Isso permite manter uma cópia temporária de trabalho, mas a política preferencial do projeto é:

1. armazenar a base eleitoral bruta completa em Google Drive, Google Cloud Storage ou outro repositório autorizado;
2. manter no computador apenas amostras, metadados, scripts e resultados agregados;
3. não versionar arquivos brutos, tokens, cookies ou credenciais;
4. registrar no relatório a fonte, a data de obtenção, o tamanho e o checksum dos arquivos usados.

O Google Colab é uma boa opção para as etapas pesadas de geoprocessamento e PLN, especialmente quando forem necessários GPU ou mais memória. O fluxo recomendado é montar o Google Drive no Colab, executar o notebook a partir de uma cópia versionada deste projeto e gravar apenas resultados reproduzíveis no diretório de saída. O código deve continuar funcionando localmente com dados sintéticos ou uma amostra, para que o projeto não dependa exclusivamente do Colab.

Neste workspace não há atualmente um conector MCP autenticado para Google Drive ou Colab. A comunicação pode ser feita por notebooks exportados, repositório Git ou armazenamento compartilhado. Credenciais de APIs devem ser inseridas diretamente no ambiente de execução, usando os mecanismos de secrets do Colab ou variáveis locais, e nunca incluídas nos notebooks ou enviadas no chat.

O Drive já foi montado no Colab em `MyDrive/projeto_eleitoral`, e o manifesto inicial foi criado em `data/manifest.json`. O inventário atual registra zero arquivos brutos; nenhuma base eleitoral pesada foi importada ainda. Antes do download, devem ser definidos a eleição, o recorte geográfico, o nível de agregação e a fonte oficial.

## Recorte geográfico inicial

O escopo inicial está definido para a eleição de **2026**, nos municípios de **Niterói** e **São Gonçalo**, no estado do Rio de Janeiro, em nível de seção eleitoral quando esse nível estiver disponível na fonte oficial. O objetivo de expansão é cobrir posteriormente todos os municípios do estado do Rio de Janeiro.

O recorte foi escolhido para limitar o custo inicial de armazenamento e processamento, permitindo validar o método em uma área conhecida antes da expansão estadual. A configuração está registrada em [data/project_scope.json](data/project_scope.json), e a fonte selecionada está em [data/source_selection.json](data/source_selection.json). O TSE já disponibiliza o recurso estadual em ZIP, com tamanho HTTP verificado de 1.295.006 bytes; o checksum será preenchido após o download direto para o Drive.

### Fonte tratada para exploração

Também foi confirmada na Base dos Dados a tabela **Resultados por Candidato e Seção Eleitoral**, com cobertura até 2026 e tamanho integral estimado em **76,30 GB**. Ela não deve ser baixada. A estratégia será consultar via BigQuery apenas o ano de 2026, o estado RJ, Niterói e São Gonçalo, e as colunas necessárias. A consulta exigirá autenticação no ambiente do Colab e deve registrar bytes processados, custo estimado e data da consulta.

O ZIP oficial do TSE permanece como referência de validação. Os resultados da Base dos Dados só serão usados no modelo depois de comparar contagens, identificadores e totais agregados com a fonte oficial.

## Avaliação

- **Detecção:** inspeção de casos conhecidos ou construídos em dados sintéticos, estabilidade dos rankings e análise de sensibilidade.
- **PLN:** precisão, revocação, F1 e matriz de confusão em amostra anotada, se houver dados rotulados.
- **Espacial:** análise de autocorrelação e robustez a diferentes definições de vizinhança.
- **Mitigação:** erro agregado, preservação de tendências e risco de reidentificação em cenários simulados.

## Limitações e cuidados

- Correlação estatística não prova coação, compra de votos ou qualquer ilícito.
- Resultados eleitorais agregados não permitem inferir a intenção individual dos eleitores.
- Ausência de denúncia não significa ausência de ocorrência.
- Dados de redes sociais têm viés de seleção, duplicação, localização incerta e possível desinformação.
- O projeto não deve publicar listas acusatórias, coordenadas sensíveis ou dados pessoais.
- Questões jurídicas serão apresentadas como análise acadêmica, com referências oficiais verificadas antes da versão final.

## Entregáveis

- `relatorio/`: relatório técnico em edição e versão final em PDF.
- `slides/`: apresentação da metodologia, resultados e limitações.
- `video/`: roteiro, materiais de apoio e registro da apresentação.
- `notebooks/`: exploração, experimentos e geração de figuras.
- `src/`: código reutilizável de ingestão, atributos, modelos, PLN e visualização.
- `data/`: somente dados autorizados, anonimizados, sintéticos ou instruções de obtenção.

## Referências iniciais

- HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. *The Elements of Statistical Learning*. 2. ed. Springer, 2009.
- JAMES, G. et al. *An Introduction to Statistical Learning*. 2. ed. Springer, 2021.
- MITCHELL, T. *Machine Learning*. McGraw-Hill, 1997.
- GOODFELLOW, I.; BENGIO, Y.; COURVILLE, Y. *Deep Learning*. MIT Press, 2016.
- VANDERPLAS, J. *Python Data Science Handbook*. O'Reilly, 2016.
- RUSSELL, S.; NORVIG, P. *Artificial Intelligence: A Modern Approach*. 3. ed. Pearson, 2010.

As referências específicas de TSE, métodos de PLN, dados territoriais e legislação serão adicionadas após a confirmação das fontes efetivamente utilizadas.
