#https://wiki.python.org.br/ListaDeExercicios
#https://github.com/rmveiga/exercicios_python
#https://www.realizzarecursos.com.br/blog/exercicios-de-python/
#https://www.youtube.com/watch?v=nIHq1MtJaKs
#https://docs.python.org/pt-br/3/tutorial/index.html
#https://awari.com.br/python-aprenda-a-imprimir-em-cores/?utm_source=blog&utm_campaign=projeto+blog&utm_medium=Python:%20Aprenda%20a%20Imprimir%20em%20Cores


import matplotlib.pyplot as plt  
cores = ["red", "green"]  
gemas = [["Ruby", "Fire Quartz"], ["Esmeralda", "Jade"]]  
plt.figure(figsize=(8, 4))  
plt.barh(cores, [len(g) for g in gemas], color=cores)  
plt.show()

#site
#jogo
#programa
#automação
#