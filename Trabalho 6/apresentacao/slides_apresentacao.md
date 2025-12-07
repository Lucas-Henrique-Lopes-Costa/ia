---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# Trabalho Prático 06
## Agentes Inteligentes

**Sistema de Análise de Sentimentos em Redes Sociais**

Autor: Lucas Henrique e Pedro Gonçalves
Data: Dezembro 2024

---

## Descrição da Aplicação

**Sistema Multi-Agente para Análise de Sentimentos**

- Analisa posts de redes sociais automaticamente
- Classifica sentimentos: Positivo, Negativo, Neutro
- Gera relatórios estatísticos e recomendações
- Utiliza o framework **AutoGen** para coordenação de agentes

### Objetivo
Demonstrar como múltiplos agentes inteligentes podem colaborar para resolver uma tarefa complexa de processamento de linguagem natural.

---

## Arquitetura do Sistema

```
┌─────────────────┐
│  Posts de       │
│  Redes Sociais  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Agente Coletor  │  ← Organiza e prepara dados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Agente          │  ← Analisa sentimentos
│ Analisador      │     (Positivo/Negativo/Neutro)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Agente Relator  │  ← Gera relatório final
└────────┬────────┘     e recomendações
         │
         ▼
┌─────────────────┐
│   Relatório     │
│   Final         │
└─────────────────┘
```

---

## Características dos Agentes

### Comunicação

- Os agentes trabalham em **pipeline sequencial**
- Cada agente possui especialização única
- Coordenação via AutoGen framework

---

# Exemplo de Resultados

### Análise de 10 Posts

- **60%** Positivos
- **20%** Negativos
- **20%** Neutros

### Tendência: **Predominantemente POSITIVA**

### Recomendações Geradas

- ✓ Excelente reputação! Destacar feedbacks positivos
- ✓ Baixo índice de insatisfação
- → Continuar monitoramento para manter o padrão

---

## Conclusões

### Aspectos Positivos

1. **Modularidade**: Cada agente tem responsabilidade clara e específica
2. **Escalabilidade**: Fácil adicionar novos agentes ou funcionalidades
3. **Autonomia**: Agentes trabalham de forma independente
4. **Colaboração**: Coordenação eficiente entre agentes

### Aprendizados

- AutoGen facilita a criação de sistemas multi-agente
- Divisão de tarefas melhora a organização do código
- Agentes especializados são mais eficientes que um único agente generalista

---

## Referências

- **AutoGen Documentation**: <https://microsoft.github.io/autogen/>
- **OpenAI API**: <https://platform.openai.com/docs>

---

# Obrigado

- **Link para apresentação**: <https://>

---
