from langgraph.graph import END, START, StateGraph

from app.nodes.match import match_use_cases
from app.nodes.model import model_business
from app.nodes.report import render_report
from app.nodes.research import read_site, search_news_register
from app.state import RunState


def build_graph():
    graph = StateGraph(RunState)
    graph.add_node("site", read_site)
    graph.add_node("search", search_news_register)
    graph.add_node("model", model_business)
    graph.add_node("match", match_use_cases)
    graph.add_node("report", render_report)
    graph.add_edge(START, "site")
    graph.add_edge("site", "search")
    graph.add_edge("search", "model")
    graph.add_edge("model", "match")
    graph.add_edge("match", "report")
    graph.add_edge("report", END)
    return graph.compile()
