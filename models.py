from datetime import datetime, timedelta
from workalendar.america import Brazil

class ContadorDePrazo:
    def __init__(self):
        self.calendario = Brazil()

    def AdicionarFeriadosMoveis(self, ano):
        """
        Adiciona feriados móveis ao calendário, como Sexta-feira Santa.
        """
        self.calendario.holidays(ano).append((self.calendario.get_good_friday(ano), "Sexta-feira Santa"))

    def CalcularDiasCorridos(self, dataInicial, diasCorridos):
        """
        Soma os dias corridos, excluindo o dia inicial e incluindo o último.
        """
        return dataInicial + timedelta(days=diasCorridos)

    def CalcularProximoDiaUtil(self, data):
        """
        Ajusta a data para o próximo dia útil, caso esteja em um fim de semana ou feriado.
        """
        while not self.calendario.is_working_day(data):
            data += timedelta(days=1)
        return data

    def CalcularDiasUteis(self, dataInicial, diasUteis):
        """
        Soma os dias úteis corretamente, incluindo ajuste para o próximo dia útil.
        """
        diasUteisContados = 0
        while diasUteisContados < diasUteis:
            if self.calendario.is_working_day(dataInicial):
                diasUteisContados += 1
            dataInicial += timedelta(days=1)
        return dataInicial - timedelta(days=1)

class Projudi(ContadorDePrazo):
    def RetornarPrazos(self, dataExpedicao):
        """
        Calcula os prazos de Embargos de Declaração e Recurso Inominado no sistema Projudi,
        considerando o feriado móvel da Sexta-feira Santa.
        """
        ano = dataExpedicao.year
        self.AdicionarFeriadosMoveis(ano)

        # 10 dias corridos para ciência das partes
        dataCiencia = self.CalcularDiasCorridos(dataExpedicao, 10)

        # Ajustar para o próximo dia útil, caso necessário
        dataInicioRecursos = self.CalcularProximoDiaUtil(dataCiencia + timedelta(days=1))

        # Prazos para ED e RI
        prazos = {
            "Embargos de Declaração (ED)": self.CalcularProximoDiaUtil(
                self.CalcularDiasUteis(dataInicioRecursos, 5)
            ),
            "Recurso Inominado (RI)": self.CalcularProximoDiaUtil(
                self.CalcularDiasUteis(dataInicioRecursos, 10)
            )
        }

        mensagem = (
            "Nota: Feriados móveis, como Sexta-feira Santa, não são considerados "
            "na contagem do prazo. Por favor, verifique manualmente a validade da data em "
            "casos de feriados móveis ou específicos de sua localidade."
        )

        return prazos, mensagem

class PJESystem(ContadorDePrazo):
    def RetornarPrazos(self, dataPublicacao):
        """
        Calcula os prazos de Embargos de Declaração, Recurso Inominado e Apelação no sistema PJE.
        """
        dataInicio = dataPublicacao + timedelta(days=1)

        prazos = {
            "Embargos de Declaração (ED)": self.CalcularDiasUteis(dataInicio, 5),
            "Recurso Inominado (RI)": self.CalcularDiasUteis(dataInicio, 10),
            "Apelação": self.CalcularDiasUteis(dataInicio, 15)
        }

        mensagem = (
            "Nota: Feriados móveis, como Sexta-feira Santa, não são considerados "
            "na contagem do prazo. Por favor, verifique manualmente a validade da data em "
            "casos de feriados móveis ou específicos de sua localidade."
        )

        return prazos, mensagem