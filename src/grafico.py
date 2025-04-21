import matplotlib.pyplot as plt
import numpy as np


class VisualizadorGraficos:
    @staticmethod
    def plot_resultados(resultados):
        """Gera três tipos de gráficos a partir dos resultados"""
        try:
            # Tenta usar o estilo seaborn, se não existir usa o padrão
            plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'ggplot')
        except:
            plt.style.use('default')

        # Verificação de dados
        if not resultados:
            raise ValueError("Nenhum dado fornecido para plotagem")

        # Extração de dados segura
        try:
            cenarios = [r['nome'] for r in resultados]
            tempos_totais = [r['tempo_total'] for r in resultados]

            bairros = ['Santa Rita', 'Honório Bicalho', 'Nova Suíça', 'Bela Fama']
            alocacoes = {b: [r['alocacao'][b] for r in resultados] for b in bairros}

        except KeyError as e:
            raise KeyError(f"Estrutura de dados inválida: {str(e)}")

        # Configurações comuns
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.titleweight'] = 'bold'

        # 1. Gráfico de Tempo Total
        fig1 = plt.figure(figsize=(10, 5))
        cores = ['#2ecc71', '#3498db', '#e74c3c']  # Verde, Azul, Vermelho
        bars = plt.bar(cenarios, tempos_totais, color=cores[:len(cenarios)])

        plt.title("Tempo Total por Cenário", pad=20)
        plt.ylabel("Minutos")
        plt.grid(axis='y', linestyle=':', alpha=0.7)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 2,
                     f'{height:.1f} min',
                     ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig("tempos_totais.png", dpi=300)
        plt.close(fig1)

        # 2. Gráfico de Alocação por Bairro
        fig2 = plt.figure(figsize=(12, 6))
        x = np.arange(len(cenarios))
        width = 0.18

        for i, bairro in enumerate(bairros):
            plt.bar(x + (i * width), alocacoes[bairro], width, label=bairro)

        plt.title("Alocação de Ônibus por Bairro", pad=20)
        plt.ylabel("Quantidade de Ônibus")
        plt.xticks(x + (width * 1.5), cenarios)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.grid(axis='y', linestyle=':', alpha=0.7)

        plt.tight_layout()
        plt.savefig("alocacao_bairros.png", dpi=300, bbox_inches='tight')
        plt.close(fig2)

        # 3. Gráfico de Proporção de Tempo
        fig3 = plt.figure(figsize=(10, 6))
        cores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

        for i, r in enumerate(resultados):
            tempos = [
                r['alocacao']['Santa Rita'] * 10,
                r['alocacao']['Honório Bicalho'] * 7,
                r['alocacao']['Nova Suíça'] * 5,
                r['alocacao']['Bela Fama'] * 9
            ]
            plt.pie(tempos,
                    radius=1.3 - (i * 0.2),
                    colors=cores,
                    wedgeprops=dict(width=0.3, edgecolor='w'),
                    startangle=90)

        plt.legend(bairros, title="Bairros",
                   bbox_to_anchor=(1, 0.5), loc='center left')
        plt.title("Distribuição do Tempo por Bairro", pad=20)

        plt.tight_layout()
        plt.savefig("proporcao_tempo.png", dpi=300, bbox_inches='tight')
        plt.close(fig3)

    @staticmethod
    def plot_regiao_factivel():
        """Gráfico da região factível para x1 (Santa Rita) e x2 (Honório Bicalho)"""
        plt.figure(figsize=(10, 6))

        # Definir eixos
        x1 = np.linspace(0, 10, 500)
        x2 = np.linspace(0, 10, 500)

        # Restrições
        demanda_sr = 5  # x1 >= 5 (40*5 >= 200)
        demanda_hb = 4.5  # x2 >= 4.5 (40*4.5 >= 180)
        frota_max = 30  # x1 + x2 <= 30 (simplificado para 2 variáveis)
        ordem = x1 >= x2  # x1 >= x2

        # Plotar restrições
        plt.axvline(x=demanda_sr, color='r', linestyle='-', label=r'$x_1 \geq 5$ (Santa Rita)')
        plt.axhline(y=demanda_hb, color='b', linestyle='-', label=r'$x_2 \geq 4.5$ (Honório Bicalho)')
        plt.plot(x1, x1, 'g--', label=r'$x_1 \geq x_2$ (Ordem decrescente)')
        plt.plot(x1, frota_max - x1, 'k-', label=r'$x_1 + x_2 \leq 30$ (Frota máxima)')

        # Área factível (usando fill_between)
        plt.fill_between(
            x1,
            np.maximum(demanda_hb, np.minimum(x1, frota_max - x1)),
            where=(x1 >= demanda_sr) & (x1 <= 10),
            color='lightgray',
            alpha=0.5,
            label='Região Factível'
        )

        # Ponto ótimo (5, 4)
        plt.plot(5, 4, 'ro', markersize=8, label='Solução Ótima (5, 4)')

        # Curvas de nível da função objetivo (Z = 10x1 + 7x2)
        X1, X2 = np.meshgrid(x1, x2)
        Z = 10 * X1 + 7 * X2
        levels = np.linspace(50, 200, 10)
        cs = plt.contour(X1, X2, Z, levels=levels, colors='gray', linestyles='dotted', alpha=0.7)
        plt.clabel(cs, inline=True, fontsize=8)

        # Configurações do gráfico
        plt.xlabel('Santa Rita ($x_1$)', fontsize=12)
        plt.ylabel('Honório Bicalho ($x_2$)', fontsize=12)
        plt.title('Região Factível e Solução Ótima', pad=20, fontsize=14)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.xlim(0, 10)
        plt.ylim(0, 10)

        plt.tight_layout()
        plt.savefig("regiao_factivel.png", dpi=300, bbox_inches='tight')
        plt.close()