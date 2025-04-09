from datetime import datetime

def EstaNoRecesso(data):
    """
    Verifica se a data está no recesso do Judiciário (20/12 a 20/01).
    Retorna True se estiver no recesso, False caso contrário.
    """
    if (data.month == 12 and data.day >= 20) or (data.month == 1 and data.day <= 20):
        return True
    return False

def AjustarParaFimDoRecesso(data):
    """
    Se a data cair no recesso do Judiciário, ajusta para o primeiro dia útil após o recesso (21/01).
    """
    if EstaNoRecesso(data):
        return datetime(data.year + 1 if data.month == 12 else data.year, 1, 21)
    return data

def AdicionarFeriadosMoveis(calendario, ano):
    """
    Adiciona feriados móveis, como Sexta-feira Santa, ao calendário.
    """
    calendario.holidays(ano).append((calendario.get_good_friday(ano), "Sexta-feira Santa"))
    return calendario