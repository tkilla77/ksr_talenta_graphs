from flask import Flask, redirect, url_for, request, jsonify
import graphs
import fahrplan

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route("/query")
def query():
    source = request.args.get('from')
    dest = request.args.get('to')
    algo = request.args.get('algo')

    try:
        if "Dijkstra" == algo:
            result = graphs.shortest_path(fahrplan.latest, source, dest)
        elif "DFS" == algo:
            result = graphs.find_path_dfs(fahrplan.latest, source, dest)
        elif "BFS" == algo:
            result = graphs.find_path_bfs(fahrplan.latest, source, dest)
        else:
            return "Unknown Algorithm", 404
    except Exception as e:
        return repr(e), 404

    return result

@app.route("/allstops")
def allstops():
    return jsonify(list(fahrplan.latest.keys()))