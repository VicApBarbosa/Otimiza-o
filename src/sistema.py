import pulp

class OtimizadorTransporte:
    def __init__(self):
        self.capacidade = 40
        self.frota_max = 30
        self.custo_onibus = 400
        self.preco_passagem = 10.90
        self.custo_fixo = 5000

    def resolver(self, tempos, demanda):
        """Resolve o modelo para um cenário específico."""
        model = pulp.LpProblem(f"Otimizacao_{id(tempos)}", pulp.LpMinimize)

        x = {
            bairro: pulp.LpVariable(f'x_{bairro}', lowBound=0, cat='Integer')
            for bairro in demanda.keys()
        }

        # Função objetivo: Minimizar tempo total de operação
        model += pulp.lpSum(tempos[bairro] * x[bairro] for bairro in demanda.keys())

        # Restrições
        for bairro in demanda.keys():
            model += self.capacidade * x[bairro] >= demanda[bairro]  # Atender demanda

        # Ordem decrescente de frota (Santa Rita >= Honório >= Nova Suíça >= Bela Fama)
        bairros_ordenados = ['Santa Rita', 'Honório Bicalho', 'Nova Suíça', 'Bela Fama']
        for i in range(len(bairros_ordenados) - 1):
            model += x[bairros_ordenados[i]] >= x[bairros_ordenados[i + 1]]

        # Frota máxima e viabilidade econômica
        model += pulp.lpSum(x.values()) <= self.frota_max
        model += (self.preco_passagem * sum(demanda.values())) - \
                 (self.custo_onibus * pulp.lpSum(x.values())) >= self.custo_fixo

        model.solve(pulp.PULP_CBC_CMD(msg=False))

        return {bairro: int(x[bairro].value()) for bairro in x.keys()}, pulp.value(model.objective)