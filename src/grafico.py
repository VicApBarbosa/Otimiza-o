import matplotlib.pyplot as plt
import numpy as np

class VisualizadorGraficos:
    @staticmethod
    def plot_resultados(resultados):
        """Gera gráficos comparando os 3 cenários isolados."""
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'ggplot')
        plt.rcParams.update({'font.size': 10, 'axes.titlesize': 12, 'axes.titleweight': 'bold'})

        if len(resultados) != 3:
            raise ValueError("Devem haver exatamente 3 cenários.")

        # Dados para os gráficos
        cenarios = [r['nome'] for r in resultados]
        tempos = [r['tempo_total'] for r in resultados]
        alocacoes = {bairro: [r['alocacao'][bairro] for r in resultados]
                    for bairro in ['Santa Rita', 'Honório Bicalho', 'Nova Suíça', 'Bela Fama']}

        # --- Gráfico 1: Tempo Total ---
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        cores = ['#2ecc71', '#3498db', '#e74c3c']  # Verde, Azul, Vermelho
        bars = ax1.bar(cenarios, tempos, color=cores, edgecolor='black')

        ax1.set_title("Tempo Total de Operação por Cenário", pad=20)
        ax1.set_ylabel("Tempo (minutos)")
        ax1.grid(axis='y', linestyle=':', alpha=0.7)

        # Anotar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f} min',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig("tempos_totais.png", dpi=300)
        plt.close(fig1)

        # --- Gráfico 2: Alocação por Bairro ---
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        width = 0.2
        x = np.arange(len(cenarios))

        for i, bairro in enumerate(alocacoes.keys()):
            ax2.bar(x + (i * width), alocacoes[bairro], width, label=bairro, edgecolor='black')

        ax2.set_title("Alocação de Ônibus por Bairro", pad=20)
        ax2.set_ylabel("Quantidade de Ônibus")
        ax2.set_xticks(x + width * 1.5)
        ax2.set_xticklabels(cenarios, rotation=45)
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(axis='y', linestyle=':', alpha=0.7)

        plt.tight_layout()
        plt.savefig("alocacao_bairros.png", dpi=300, bbox_inches='tight')
        plt.close(fig2)