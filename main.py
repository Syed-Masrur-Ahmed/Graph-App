from flask import Flask, render_template, request, redirect
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from time import sleep
import os
import asyncio

plt.style.use('fivethirtyeight')

my_path = "/".join(os.path.abspath(__file__).split("\\")[0:-1]) + "/static/"

app = Flask(__name__)

global columns
columns = []
col_rep = -1

data_ = []
data_rep = -1

data_string = ""
graph = []
graph_rep = -1

keys = []

global l
l = 0
global b
b = 0
global s
s = 0

global clear
clear = 0

global col_clear
col_clear = 0

async def line(df):
  if len(columns) > 0 and col_rep > -1:  
    plt.figure()
    plt.xlabel(columns[col_rep]["col1"])
    plt.ylabel(columns[col_rep]["col2"])  
    plt.plot(df[columns[col_rep]["col1"]], df[columns[col_rep]["col2"]], color = "#36453B")        
    plt.savefig(my_path + "line.png", bbox_inches = "tight")
    plt.close()
    global l
    l = 1
    return

async def bar(df):
  if len(columns) > 0 and col_rep > -1:  
    plt.figure()
    plt.xlabel(columns[col_rep]["col1"])
    plt.ylabel(columns[col_rep]["col2"])
    plt.bar(df[columns[col_rep]["col1"]], df[columns[col_rep]["col2"]], color = "#36453B")        
    plt.savefig(my_path + "bar.png", bbox_inches = "tight")
    plt.close()
    global b
    b = 1
    return

async def scatter(df):
  if len(columns) > 0 and col_rep > -1:  
    plt.figure()
    plt.xlabel(columns[col_rep]["col1"])
    plt.ylabel(columns[col_rep]["col2"])    
    plt.scatter(df[columns[col_rep]["col1"]], df[columns[col_rep]["col2"]], color = "#36453B")        
    plt.savefig(my_path + "scatter.png", bbox_inches = "tight")
    plt.close()
    global s
    s = 1
    return

@app.route('/', methods=["GET", "POST"])
def index():  
  if request.method == "POST":
    global col_rep
    col_rep += 1
    columns.append(request.form)
    return redirect('/data')
     
  return render_template("index.html")
  
@app.route('/data', methods=['GET', 'POST'])
def data():
  global col_clear
  global clear
  global data_
  global data_string
  global columns
  if col_clear == 1:
    columns = []
    col_clear = 0
  if clear == 1:
    data_ = []
    data_string = ""
    clear = 0   
  if request.method == "POST":
    global data_rep
    data_rep += 1
    data_.append(request.form)
    return render_template("data.html", columns=columns, col_rep = col_rep, data_=data_, data_rep=data_rep)
  if data != []:
    return render_template("data.html", columns=columns, col_rep = col_rep, data_=data_, data_rep=data_rep)
  else:
    return render_template("data.html", columns=columns, col_rep = col_rep)

#https://flask.palletsprojects.com/en/2.0.x/async-await/
@app.route('/graph', methods=['GET', 'POST'])
async def graph_():
  if request.method == "POST":
    global data_string
    data_string = ""
    graph.append(request.form)
    global graph_rep
    graph_rep += 1
    for x in data_:
      row = str(x["data1"]) + "," + str(x["data2"]) + "\n"
      data_string += row
    df = pd.read_csv(StringIO(data_string), names = [columns[col_rep]["col1"], columns[col_rep]["col2"]]) 
    
    global l
    global b
    global s
    l = 0
    b = 0
    s = 0

    for x in graph[-1]:
     
      if x[0] == "l":        
        await line(df)
      if x[0] == "b":
        await bar(df)  
      if x[0] == "s":
        await scatter(df)
    
    return render_template("graph.html", graph_data=data_string, graph_rep=graph_rep, graph=graph, path = 0,
    l = l, b = b, s = s )    
    
  
  return render_template("graph.html")

@app.route('/clear', methods=["POST"])
def clear():
  
  if request.method == "POST":
      global clear
      clear = 1
 
  return redirect("/data")

@app.route('/clearcol', methods=["POST"])

def clearcol():
  
  if request.method == "POST":
      global col_clear
      col_clear = 1
  return  redirect("/") 
 



@app.route('/datatograph', methods=["POST"])
def datatograph():
     return redirect("/graph")  

@app.route('/restart', methods=["POST"])
def restart():
    if request.method == "POST":
      global clear
      clear = 1
      global col_clear
      col_clear = 1
    return redirect("/")  

app.run(host='0.0.0.0', port=8080)