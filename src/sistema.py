import pulp


class OtimizadorTransporte:
    def __init__(self):
        self.demandas = {
            'Santa Rita': 200,
            'Honório Bicalho': 180,
            'Nova Suíça': 220,
            'Bela Fama': 160
        }
        self.capacidade = 40
        self.frota_max = 30
        self.custo_onibus = 400
        self.preco_passagem = 10.90
        self.custo_fixo = 5000
        self.tempos_base = {
            'Santa Rita': 10,
            'Honório Bicalho': 7,
            'Nova Suíça': 5,
            'Bela Fama': 9
        }

    def resolver(self, tempos=None):
        """Resolve o modelo com tempos padrão ou customizados"""
        tempos = tempos if tempos else self.tempos_base

        model = pulp.LpProblem("Otimizacao_Transporte_4var", pulp.LpMinimize)

        x = {
            'Santa Rita': pulp.LpVariable('x1', lowBound=0, cat='Integer'),
            'Honório Bicalho': pulp.LpVariable('x2', lowBound=0, cat='Integer'),
            'Nova Suíça': pulp.LpVariable('x3', lowBound=0, cat='Integer'),
            'Bela Fama': pulp.LpVariable('x4', lowBound=0, cat='Integer')
        }

        # Função objetivo
        model += (
                tempos['Santa Rita'] * x['Santa Rita'] +
                tempos['Honório Bicalho'] * x['Honório Bicalho'] +
                tempos['Nova Suíça'] * x['Nova Suíça'] +
                tempos['Bela Fama'] * x['Bela Fama']
        )

        # Restrições
        model += 40 * x['Santa Rita'] >= 200
        model += 40 * x['Honório Bicalho'] >= 180
        model += 40 * x['Nova Suíça'] >= 220
        model += 40 * x['Bela Fama'] >= 160

        # Ordem decrescente de frota
        model += x['Santa Rita'] >= x['Honório Bicalho']
        model += x['Honório Bicalho'] >= x['Nova Suíça']
        model += x['Nova Suíça'] >= x['Bela Fama']

        # Frota máxima e viabilidade econômica
        model += sum(x.values()) <= self.frota_max
        model += (self.preco_passagem * sum(self.demandas.values())) - \
                 (self.custo_onibus * sum(x.values())) >= self.custo_fixo

        model.solve(pulp.PULP_CBC_CMD(msg=False))

        return {bairro: int(var.value()) for bairro, var in x.items()}, pulp.value(model.objective)