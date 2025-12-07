# Trabalho Prático 06 - Agentes Inteligentes

**Sistema de Análise de Sentimentos em Redes Sociais com Multi-Agentes**

## Descrição da Aplicação

Sistema inteligente que utiliza múltiplos agentes colaborativos para analisar sentimentos de posts de redes sociais. A aplicação demonstra como agentes especializados podem trabalhar em conjunto para resolver uma tarefa complexa.

### Agentes do Sistema

1. **Agente Coletor**
   - Responsável por coletar e organizar posts
   - Prepara dados para processamento
   - Mantém registro de todos os posts

2. **Agente Analisador**
   - Analisa o sentimento de cada post
   - Classifica como: POSITIVO, NEGATIVO ou NEUTRO
   - Fornece justificativas e nível de confiança

3. **Agente Relator**
   - Consolida resultados das análises
   - Calcula estatísticas gerais
   - Gera insights e recomendações

## Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. (Opcional) Configure sua chave da OpenAI:

```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

**Nota:** O sistema funciona sem a chave da API usando análise de sentimentos baseada em palavras-chave. Para usar o AutoGen completo com GPT-4, configure a chave da OpenAI.

### Execução

```bash
cd src
python analise_sentimentos_agentes.py
```

## Estrutura do Projeto

```
Trabalho 6/
├── src/
│   └── analise_sentimentos_agentes.py    # Código principal
├── data/
│   └── analise_sentimentos_*.json        # Resultados salvos
├── apresentacao/
│   └── slides_apresentacao.md            # Slides do relatório
├── requirements.txt                       # Dependências
└── README.md                             # Este arquivo
```

## Exemplo de Saída

O sistema processa 10 posts simulados e gera:

- Análise individual de cada post
- Estatísticas consolidadas (percentuais)
- Tendência geral dos sentimentos
- Recomendações baseadas nos dados
- Arquivo JSON com todos os resultados

## Tecnologias Utilizadas

- **Python 3.x**
- **AutoGen** - Framework para agentes inteligentes
- **OpenAI API** (opcional) - Para análise avançada

## Autor

Lucas Henrique

## Licença

Projeto acadêmico - Trabalho Prático 06
