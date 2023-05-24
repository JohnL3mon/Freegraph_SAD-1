from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np, os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
from io import StringIO


class DadosSessao():
	existem_campos = False
	campos = []
	linha_selecionada = ''
	coluna_selecionada = ''
	df = None
	dados_linha = []
	dados_coluna = []

def index(request):
	try:  # requisição POST (enviar DadosSessao à página index.html)
		if request.method == 'POST' and request.FILES['arquivo']:
			arquivo = request.FILES['arquivo']

			msg = 'Sucesso!'
			msg_cor = 'verde'
			DadosSessao.df = pd.read_csv(StringIO(arquivo.read().decode('utf-8')), delimiter=';')
			DadosSessao.campos = DadosSessao.df.columns.tolist()


			for item in DadosSessao.campos: # Limpar campos que não seriam necessárias (id, index)
				if 'Index' in item.capitalize():
					DadosSessao.campos.remove('Index')
				if "Id" in item.capitalize():
					DadosSessao.campos.remove('Id')

			return render(request, 'index.html', context = {'message': msg, 'msg_status': msg_cor, 'campos': DadosSessao.campos})

	except:	# Se confirmar formulário sem arquivo carregado
		try:
			for data in request.POST:
				if 'is-linha' in data:
					# Lógica para tratar as checkbox selecionadas
					for item in request.POST:
						for campo in DadosSessao.campos:
							if campo == item:
								DadosSessao.linha_selecionada = campo
								DadosSessao.dados_linha = DadosSessao.df[campo]#.tolist()
					msg = f'Eixo x selecionado com sucesso ({DadosSessao.linha_selecionada})'
					return render(request, 'index.html', context = {'message': msg, 'msg_status': 'verde', 'campos': DadosSessao.campos, 'row_selected': True})

				elif 'is-coluna' in data:
					# Lógica para exibir gráfico
					for item in request.POST:
						for campo in DadosSessao.campos:
							if campo == item:
								DadosSessao.coluna_selecionada = campo
								DadosSessao.dados_coluna = DadosSessao.df[campo]#.tolist()

								x = DadosSessao.dados_linha
								y = DadosSessao.dados_coluna

								context = {'x': x, 'y': y}
								return render(request, 'resultado.html', context)
		except Exception as e:
			print(e) # Reverse for 'plot_view' not found. 'plot_view' is not a valid view function or pattern name.
			return render(request, 'index.html', context = {'message': f'{e}', 'msg_status': 'vermelho'})

	else:	# requisição GET (só visita/leitura à pagina index.html)
		return render(request, 'index.html')
