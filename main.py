from src.sistema import OtimizadorTransporte
from src.grafico import VisualizadorGraficos

def print_cabecalho():
    print("\n" + "=" * 80)
    print("SISTEMA DE OTIMIZAÇÃO DE TRANSPORTE URBANO".center(80))
    print("=" * 80)

def print_resultados(cenario, alocacao, tempo):
    """Exibe os resultados formatados no console"""
    print(f"\n► {cenario['nome']}")
    print(f"  {'Bairro':<20} {'Ônibus':>8} {'Tempo (min)':>12}")
    print("-" * 45)
    for bairro, qtd in alocacao.items():
        tempo_bairro = {
            'Santa Rita': 10,
            'Honório Bicalho': 7,
            'Nova Suíça': 5,
            'Bela Fama': 9
        }.get(bairro) * qtd
        print(f"  {bairro:<20} {qtd:>8} {tempo_bairro:>12.1f}")
    print("-" * 45)
    print(f"  {'TOTAL':<20} {sum(alocacao.values()):>8} {tempo:>12.1f}")
    print(f"\n  Observação: {cenario['obs']}")

def main():
    # Configuração dos cenários
    cenarios = [
        {'nome': 'Cenário Base', 'obs': 'Operação padrão'},
        {'nome': 'Ônibus Novos (+20% tempo)',
         'tempos': {'Santa Rita': 12, 'Honório Bicalho': 8.4, 'Nova Suíça': 6, 'Bela Fama': 10.8},
         'obs': 'Veículos com tecnologia ecológica'},
        {'nome': 'Trânsito Intenso (+30% tempo)',
         'tempos': {'Santa Rita': 13, 'Honório Bicalho': 9.1, 'Nova Suíça': 6.5, 'Bela Fama': 11.7},
         'obs': 'Horário de pico com congestionamentos'}
    ]

    # Processamento
    otimizador = OtimizadorTransporte()
    resultados_graficos = []

    print_cabecalho()
    for cenario in cenarios:
        if 'tempos' in cenario:
            alocacao, tempo = otimizador.resolver(tempos=cenario['tempos'])
        else:
            alocacao, tempo = otimizador.resolver()

        resultados_graficos.append({
            'nome': cenario['nome'],
            'alocacao': alocacao,
            'tempo_total': tempo
        })

        print_resultados(cenario, alocacao, tempo)

    # Geração de gráficos
    try:
        VisualizadorGraficos.plot_resultados(resultados_graficos)
        VisualizadorGraficos.plot_regiao_factivel()  # ADIÇÃO 1: Chamada para o novo gráfico
        print("\n" + "=" * 80)
        print(f"Gráficos gerados: 'tempos_totais.png', 'alocacao_bairros.png', 'proporcao_tempo.png', 'regiao_factivel.png'")  # ADIÇÃO 2: Nome do novo arquivo
        print("=" * 80)
    except Exception as e:
        print(f"\n⚠️ Erro ao gerar gráficos: {str(e)}")

if __name__ == "__main__":
    main()