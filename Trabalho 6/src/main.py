import autogen
from typing import List, Dict
import json
import os
from datetime import datetime

# Configuração da API (você deve configurar sua chave da OpenAI)
config_list = [
    {"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY", "sua-chave-aqui")}
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}

# Posts simulados para análise
POSTS_SIMULADOS = [
    "Adorei o novo produto! Qualidade excepcional e entrega rápida!",
    "Péssimo atendimento, nunca mais compro nesta loja.",
    "O produto chegou conforme descrito.",
    "Experiência maravilhosa! Recomendo para todos!",
    "Decepcionante. Esperava muito mais pela qualidade.",
    "Entrega dentro do prazo. Produto ok.",
    "Incrível! Superou todas as minhas expectativas!",
    "Não funciona como prometido. Total desperdício de dinheiro.",
    "Bom custo-benefício. Nada de especial.",
    "Excelente! Voltarei a comprar com certeza!",
]


class SistemaAnaliseMultiAgente:
    """Sistema principal que coordena os agentes"""

    def __init__(self):
        """Inicializa o sistema e cria os agentes"""
        self.posts = POSTS_SIMULADOS
        self.resultados = []
        self.criar_agentes()

    def criar_agentes(self):
        """Cria os três agentes do sistema"""

        # 1. AGENTE COLETOR - Responsável por coletar e preparar os dados
        self.agente_coletor = autogen.AssistantAgent(
            name="AgenteColetor",
            system_message="""Você é o Agente Coletor de Dados.
            Sua função é:
            1. Receber posts de redes sociais
            2. Organizar e estruturar os dados
            3. Enviar os posts um por um para análise
            4. Manter registro de todos os posts processados
            
            Sempre responda em formato estruturado e claro.
            """,
            llm_config=llm_config,
        )

        # 2. AGENTE ANALISADOR - Analisa o sentimento de cada post
        self.agente_analisador = autogen.AssistantAgent(
            name="AgenteAnalisador",
            system_message="""Você é o Agente Analisador de Sentimentos.
            Sua função é:
            1. Receber posts individuais
            2. Analisar o sentimento (POSITIVO, NEGATIVO ou NEUTRO)
            3. Fornecer uma breve justificativa da análise
            4. Atribuir uma pontuação de confiança (0-100%)
            
            Formato de resposta:
            SENTIMENTO: [POSITIVO/NEGATIVO/NEUTRO]
            CONFIANÇA: [0-100]%
            JUSTIFICATIVA: [breve explicação]
            """,
            llm_config=llm_config,
        )

        # 3. AGENTE RELATOR - Gera relatório final com estatísticas
        self.agente_relator = autogen.AssistantAgent(
            name="AgenteRelator",
            system_message="""Você é o Agente Relator.
            Sua função é:
            1. Receber todos os resultados das análises
            2. Calcular estatísticas gerais
            3. Gerar um relatório consolidado
            4. Fornecer insights e recomendações
            
            Sempre inclua:
            - Percentual de cada sentimento
            - Total de posts analisados
            - Tendência geral
            - Recomendações baseadas nos dados
            """,
            llm_config=llm_config,
        )

        # Agente Usuário para coordenação
        self.user_proxy = autogen.UserProxyAgent(
            name="Coordenador",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={"use_docker": False},
        )

    def processar_post(self, post: str, indice: int) -> Dict:
        """Processa um post individual através dos agentes"""
        print(f"\n{'='*70}")
        print(f"PROCESSANDO POST #{indice + 1}")
        print(f"{'='*70}")
        print(f"Post: {post}\n")

        # Etapa 1: Coletor recebe o post
        mensagem_coleta = f"""
        Post #{indice + 1} recebido para processamento:
        "{post}"
        
        Por favor, confirme o recebimento e prepare para análise.
        """

        print("→ AGENTE COLETOR: Recebendo post...")

        # Etapa 2: Analisador processa o sentimento
        mensagem_analise = f"""
        Analise o seguinte post e determine o sentimento:
        "{post}"
        
        Forneça sua análise no formato especificado.
        """

        print("→ AGENTE ANALISADOR: Analisando sentimento...")

        # Simulação simplificada da análise (em produção, usaria chat real)
        resultado = {
            "post": post,
            "indice": indice + 1,
            "sentimento": self._analisar_sentimento_basico(post),
            "timestamp": datetime.now().isoformat(),
        }

        print(f"Sentimento detectado: {resultado['sentimento']}")

        return resultado

    def _analisar_sentimento_basico(self, post: str) -> str:
        """Análise básica de sentimento (fallback sem API)"""
        post_lower = post.lower()

        palavras_positivas = [
            "adorei",
            "excelente",
            "maravilhosa",
            "incrível",
            "recomendo",
            "qualidade",
            "superou",
            "ótimo",
            "bom",
        ]
        palavras_negativas = [
            "péssimo",
            "decepcionante",
            "nunca mais",
            "desperdício",
            "não funciona",
            "ruim",
        ]

        score_positivo = sum(
            1 for palavra in palavras_positivas if palavra in post_lower
        )
        score_negativo = sum(
            1 for palavra in palavras_negativas if palavra in post_lower
        )

        if score_positivo > score_negativo:
            return "POSITIVO"
        elif score_negativo > score_positivo:
            return "NEGATIVO"
        else:
            return "NEUTRO"

    def gerar_relatorio(self, resultados: List[Dict]) -> Dict:
        """Gera relatório final com estatísticas"""
        print(f"\n{'='*70}")
        print("GERANDO RELATÓRIO FINAL")
        print(f"{'='*70}\n")

        total = len(resultados)
        contagem = {"POSITIVO": 0, "NEGATIVO": 0, "NEUTRO": 0}

        for resultado in resultados:
            sentimento = resultado["sentimento"]
            contagem[sentimento] += 1

        relatorio = {
            "total_posts": total,
            "data_analise": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "estatisticas": {
                "positivos": {
                    "quantidade": contagem["POSITIVO"],
                    "percentual": round((contagem["POSITIVO"] / total) * 100, 2),
                },
                "negativos": {
                    "quantidade": contagem["NEGATIVO"],
                    "percentual": round((contagem["NEGATIVO"] / total) * 100, 2),
                },
                "neutros": {
                    "quantidade": contagem["NEUTRO"],
                    "percentual": round((contagem["NEUTRO"] / total) * 100, 2),
                },
            },
            "tendencia_geral": self._determinar_tendencia(contagem),
            "recomendacoes": self._gerar_recomendacoes(contagem, total),
        }

        return relatorio

    def _determinar_tendencia(self, contagem: Dict) -> str:
        """Determina a tendência geral dos sentimentos"""
        max_sentimento = max(contagem, key=contagem.get)

        if max_sentimento == "POSITIVO":
            return (
                "Predominantemente POSITIVA - A maioria dos posts expressa satisfação"
            )
        elif max_sentimento == "NEGATIVO":
            return "Predominantemente NEGATIVA - Há insatisfação significativa"
        else:
            return "NEUTRA - Opiniões equilibradas sem tendência clara"

    def _gerar_recomendacoes(self, contagem: Dict, total: int) -> List[str]:
        """Gera recomendações baseadas nos resultados"""
        recomendacoes = []

        perc_positivo = (contagem["POSITIVO"] / total) * 100
        perc_negativo = (contagem["NEGATIVO"] / total) * 100

        if perc_positivo > 60:
            recomendacoes.append(
                "Excelente reputação! Mantenha a qualidade e considere destacar os feedbacks positivos em marketing."
            )
        elif perc_positivo > 40:
            recomendacoes.append(
                "Reputação razoável. Identifique pontos de melhoria através dos feedbacks neutros e negativos."
            )

        if perc_negativo > 30:
            recomendacoes.append(
                "ATENÇÃO: Alto índice de feedback negativo. Priorize a resolução dos problemas reportados."
            )
            recomendacoes.append(
                "Sugestão: Implementar sistema de resposta rápida a reclamações."
            )

        if perc_negativo < 20:
            recomendacoes.append(
                "Baixo índice de insatisfação. Continue monitorando para manter o padrão."
            )

        return recomendacoes

    def executar(self):
        """Executa o sistema completo"""
        print("\n" + "=" * 70)
        print(" SISTEMA DE ANÁLISE DE SENTIMENTOS - MULTI-AGENTE ".center(70, "="))
        print("=" * 70)
        print(f"\nTotal de posts para análise: {len(self.posts)}")
        print(f"Agentes ativos: Coletor, Analisador, Relator")

        # Processar cada post
        for i, post in enumerate(self.posts):
            resultado = self.processar_post(post, i)
            self.resultados.append(resultado)

        # Gerar relatório final
        relatorio = self.gerar_relatorio(self.resultados)

        # Exibir relatório
        self.exibir_relatorio(relatorio)

        # Salvar resultados
        self.salvar_resultados(relatorio)

        return relatorio

    def exibir_relatorio(self, relatorio: Dict):
        """Exibe o relatório de forma formatada"""
        print("\n" + "=" * 70)
        print(" RELATÓRIO DE ANÁLISE ".center(70, "="))
        print("=" * 70)

        print(f"\nESTATÍSTICAS GERAIS")
        print(f"   Data da Análise: {relatorio['data_analise']}")
        print(f"   Total de Posts: {relatorio['total_posts']}")

        print(f"\nDISTRIBUIÇÃO DE SENTIMENTOS")
        stats = relatorio["estatisticas"]
        print(
            f"   Positivos: {stats['positivos']['quantidade']} ({stats['positivos']['percentual']}%)"
        )
        print(
            f"   Negativos: {stats['negativos']['quantidade']} ({stats['negativos']['percentual']}%)"
        )
        print(
            f"   Neutros: {stats['neutros']['quantidade']} ({stats['neutros']['percentual']}%)"
        )

        print(f"\nTENDÊNCIA GERAL")
        print(f"   {relatorio['tendencia_geral']}")

        print(f"\nRECOMENDAÇÕES")
        for rec in relatorio["recomendacoes"]:
            print(f"   {rec}")

        print("\n" + "=" * 70 + "\n")

    def salvar_resultados(self, relatorio: Dict):
        """Salva os resultados em arquivo JSON"""
        output_dir = "../data"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/analise_sentimentos_{timestamp}.json"

        dados_completos = {"relatorio": relatorio, "posts_analisados": self.resultados}

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)

        print(f"Resultados salvos em: {filename}")


def main():
    """Função principal"""
    print("\nInicializando Sistema Multi-Agente...")

    # Criar e executar o sistema
    sistema = SistemaAnaliseMultiAgente()
    relatorio = sistema.executar()


if __name__ == "__main__":
    main()
