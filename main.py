import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from models import Projudi, PJESystem

def AtualizarInterface():
    sistemaSelecionado = comboSistema.get()
    if sistemaSelecionado == "Projudi":
        labelData.config(text="Informe a Data de Expedição:")
    elif sistemaSelecionado == "PJE/TJSE/TJAL":
        labelData.config(text="Informe a Data de Publicação:")

def CalcularPrazo():
    sistemaSelecionado = comboSistema.get()
    dataTexto = entradaData.get()

    try:
        data = datetime.strptime(dataTexto, "%d/%m/%Y")

        resultadoTexto.delete(1.0, tk.END)
        
        if sistemaSelecionado == "Projudi":
            contador = Projudi()
            prazos, mensagem = contador.RetornarPrazos(data)
        else:  # PJE/TJSE/TJAL
            contador = PJESystem()
            prazos, mensagem = contador.RetornarPrazos(data)

        # Exibe os prazos dos recursos com cores
        for recurso, prazo in prazos.items():
            if "Embargos de Declaração" in recurso:
                resultadoTexto.insert(tk.END, f"{recurso}: {prazo.strftime('%d/%m/%Y')}\n", "verde")
            elif "Recurso Inominado" in recurso:
                resultadoTexto.insert(tk.END, f"{recurso}: {prazo.strftime('%d/%m/%Y')}\n", "vermelho")
            elif "Apelação" in recurso:
                resultadoTexto.insert(tk.END, f"{recurso}: {prazo.strftime('%d/%m/%Y')}\n", "azul")

        # Adiciona a mensagem informativa
        resultadoTexto.insert(tk.END, f"\n{mensagem}")

        # Calcula os prazos fatais para os próximos 5 dias úteis
        resultadoTexto.insert(tk.END, f"\n\nPrazos fatais dos próximos 5 dias úteis:\n", "negrito")
        dataAtual = data
        for _ in range(5):
            # Calcula o próximo dia útil
            dataAtual = contador.CalcularProximoDiaUtil(dataAtual + timedelta(days=1))
            prazos_subsequentes, _ = contador.RetornarPrazos(dataAtual)
            resultadoTexto.insert(tk.END, f"\nData: {dataAtual.strftime('%d/%m/%Y')}\n", "negrito")
            for recurso, prazo in prazos_subsequentes.items():
                if "Embargos de Declaração" in recurso:
                    resultadoTexto.insert(tk.END, f"  {recurso}: {prazo.strftime('%d/%m/%Y')}\n", "verde")
                elif "Recurso Inominado" in recurso:
                    resultadoTexto.insert(tk.END, f"  {recurso}: {prazo.strftime('%d/%m/%Y')}\n", "vermelho")
                elif "Apelação" in recurso:
                    resultadoTexto.insert(tk.END, f"  {recurso}: {prazo.strftime('%d/%m/%Y')}\n", "azul")
    except ValueError:
        resultadoTexto.delete(1.0, tk.END)
        resultadoTexto.insert(tk.END, "Data inválida! Use o formato dd/mm/aaaa.\n")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Calculadora de Prazos Judiciais")

# Filtro de sistema
ttk.Label(janela, text="Selecione o sistema:").grid(row=0, column=0, padx=10, pady=5)
comboSistema = ttk.Combobox(janela, values=["Projudi", "PJE/TJSE/TJAL"])
comboSistema.grid(row=0, column=1, padx=10, pady=5)
comboSistema.bind("<<ComboboxSelected>>", lambda event: AtualizarInterface())

# Campo para entrada de data
labelData = ttk.Label(janela, text="Informe a Data:")
labelData.grid(row=1, column=0, padx=10, pady=5)
entradaData = ttk.Entry(janela)
entradaData.grid(row=1, column=1, padx=10, pady=5)

# Botão para calcular
botaoCalcular = ttk.Button(janela, text="Calcular", command=CalcularPrazo)
botaoCalcular.grid(row=2, column=0, columnspan=2, pady=10)

# Resultado
resultadoTexto = tk.Text(janela, height=20, width=70)
resultadoTexto.tag_configure("verde", foreground="green")
resultadoTexto.tag_configure("vermelho", foreground="red")
resultadoTexto.tag_configure("azul", foreground="blue")
resultadoTexto.tag_configure("negrito", font=("TkDefaultFont", 10, "bold"))
resultadoTexto.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Inicia o loop
janela.mainloop()