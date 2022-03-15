from flask import Flask, render_template, request, redirect
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import os

plt.style.use('fivethirtyeight')

my_path = "/".join(os.path.abspath(__file__).split("\\")[0:-1]) + "/static/"

app = Flask(__name__)

columns = []

data_ = []
data_string = ""

graph = []
# l = Line Graph; b = Bar Graph; s = Scatter Plot
l = False
b = False
s = False

clear = False


async def line(df):
    if len(columns) > 0:
        plt.figure()
        plt.xlabel(columns[-1]["col1"])
        plt.ylabel(columns[-1]["col2"])
        plt.plot(df[columns[-1]["col1"]],
                 df[columns[-1]["col2"]], color="#36453B")
        plt.savefig(my_path + "line.png", bbox_inches="tight")
        plt.close()
        global l
        l = True
        return


async def bar(df):
    if len(columns) > 0:
        plt.figure()
        plt.xlabel(columns[-1]["col1"])
        plt.ylabel(columns[-1]["col2"])
        plt.bar(df[columns[-1]["col1"]],
                df[columns[-1]["col2"]], color="#36453B")
        plt.savefig(my_path + "bar.png", bbox_inches="tight")
        plt.close()
        global b
        b = True
        return


async def scatter(df):
    if len(columns) > 0:
        plt.figure()
        plt.xlabel(columns[-1]["col1"])
        plt.ylabel(columns[-1]["col2"])
        plt.scatter(df[columns[-1]["col1"]],
                    df[columns[-1]["col2"]], color="#36453B")
        plt.savefig(my_path + "scatter.png", bbox_inches="tight")
        plt.close()
        global s
        s = True
        return


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        columns.append(request.form)
        return redirect('/data')

    return render_template("index.html")


@app.route('/data', methods=['GET', 'POST'])
def data():
    global clear
    global data_
    global data_string
    global columns
    if clear:
        data_ = []
        data_string = ""
        clear = False
    if request.method == "POST":
        data_.append(request.form)
        return render_template("data.html", columns=columns, data_=data_)
    if data != []:
        return render_template("data.html", columns=columns, data_=data_)
    else:
        return render_template("data.html", columns=columns)


@app.route('/graph', methods=['GET', 'POST'])
async def graph_():
    if request.method == "POST":
        if len(data_) > 0:
            global data_string
            data_string = ""
            graph.append(request.form)
            for x in data_:
                row = str(x["data1"]) + "," + str(x["data2"]) + "\n"
                data_string += row
            df = pd.read_csv(StringIO(data_string), names=[
                columns[-1]["col1"], columns[-1]["col2"]])
            global l
            global b
            global s
            l = False
            b = False
            s = False

            for x in graph[-1]:
                if x[0] == "l":
                    await line(df)
                if x[0] == "b":
                    await bar(df)
                if x[0] == "s":
                    await scatter(df)
        return render_template("graph.html", graph_data=data_string, graph=graph,
                               l=l, b=b, s=s)

    return render_template("graph.html")


@app.route('/clear', methods=["POST"])
def clear():
    if request.method == "POST":
        global clear
        clear = True

    return redirect("/data")


@app.route('/datatograph', methods=["POST"])
def datatograph():
    return redirect("/graph")


@app.route('/clearrow', methods=["POST"])
def clearrow():
    if request.method == "POST":
        global data_
        data_ = data_[0:-1]

    return redirect("/data")


app.run(host='0.0.0.0', port=8080)
