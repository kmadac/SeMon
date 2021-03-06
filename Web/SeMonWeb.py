from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from SeMon import Data


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def servers():
    semon = Data.Collector(['192.168.122.104'], '/tmp/semon_results.yaml')
    servers = semon.load_results_yaml()
    return render_template('servers.html', servers=servers)


if __name__ == '__main__':
    app.run(debug=True)