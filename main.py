from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
import json

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: str = Form(...)):
    # Parse the pipeline JSON
    pipeline_data = json.loads(pipeline)
    
    # Extract nodes and edges
    nodes = pipeline_data.get('nodes', [])
    edges = pipeline_data.get('edges', [])
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes to the graph
    for node in nodes:
        G.add_node(node['id'])
    
    # Add edges to the graph
    for edge in edges:
        G.add_edge(edge['source'], edge['target'])
    
    # Calculate the number of nodes and edges
    num_nodes = len(G.nodes)
    num_edges = len(G.edges)
    
    # Check if the graph is a DAG
    is_dag = nx.is_directed_acyclic_graph(G)
    
    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}
