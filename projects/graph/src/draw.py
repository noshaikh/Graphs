"""
General drawing methods for graphs using Bokeh.
"""

import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8
from graph import Graph # no need to import Vertex


#BokehGraph doesnt inherit from Graph, but takes it in the initializer as an argument
class BokehGraph:
    """Class that takes a graph and exposes drawing methods."""

    def __init__(self, graph):
        self.graph=graph


#draw function
    def draw(self):
        graph = self.graph
        N = len(graph.vertices)   #note that colors have to be the same length as indices
        node_indices = list(graph.vertices.keys())
        print(node_indices)
        plot = figure(title='Graph Layout Demonstration', x_range=(-7, 7), y_range=(-7, 7),
                    tools='', toolbar_location=None)

        graph_renderer = GraphRenderer()

        graph_renderer.node_renderer.data_source.add(node_indices, 'index')
        # graph.node_renderer.data_source.add(Spectral8, 'color')
        graph_renderer.node_renderer.glyph = Oval(height=0.3, width=0.2, fill_color='red')

        edge_start = []
        edge_end =[]

        #this is O(E), where E is average number of edges which is the total number of edges divided by nodes
        for vertex_id in node_indices:
            for v in graph.vertices[vertex_id].edges:
                edge_start.append(vertex_id)
                edge_end.append(v)


        graph_renderer.edge_renderer.data_source.data = dict(
            start=edge_start,
            end=edge_end)

        # start of layout code
        # circ = [i*2*math.pi/ len(self.graph.vertices) for i in node_indices]
        # x = [math.cos(i) for i in circ]
        # y = [math.sin(i) for i in circ]

        x = []
        y = []
        for vertex_id in node_indices:
            vertex = graph.vertices[vertex_id]
            x.append(vertex.x)
            y.append(vertex.y)

        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph_renderer)

        output_file('graph.html')
        show(plot)



graph = Graph()  
graph.add_vertex('0')
graph.add_vertex('1')
graph.add_vertex('2')
graph.add_vertex('3')
graph.add_edge('0', '1')
graph.add_edge('0', '3')

bg = BokehGraph(graph)
bg.draw()