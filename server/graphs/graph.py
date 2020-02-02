from graph_model import data_log_graph, parameters_graph


graph1=data_log_graph()
graph1.set_min(0)
graph1.set_max(1)
graph1.generate_graph(10000)

graph2=parameters_graph()
graph2.set_min(0)
graph2.set_max(1)
graph2.invert(1)
graph2.set_point(100)
graph2.generate_graph(10000)





