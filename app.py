from flask import Flask, render_template, request, redirect, flash, url_for
#import main
import urllib.request
#from app import app
#from werkzeug.utils import secure_filename
#from main import getPrediction
import os
import numpy as np
from keras.models import load_model
import pandas as pd
import json
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
#SECRET_KEY = 'j\xe2u\xbc\xb6x\x15%!4Z%\xf4\xd4i\nUV\xdd\x8c%II\xcd'
app = Flask(__name__)
model = load_model('model.h5')
df=pd.read_csv('archive/city_day.csv')
app.secret_key = "j\xe2u\xbc\xb6x\x15%!4Z%\xf4\xd4i\nUV\xdd\x8c%II\xcd"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    states=df['City'].unique()
    return render_template('about.html',states=states)

@app.route('/graph/',methods=['POST'])
def graph():
    if request.method == "POST":
        state=request.form.get("city")
        #labels=df.iloc[2:13]
        #explode = (0.1, 0, 0, 0, 0) 
        #fig = px.pie(state, labels=labels)
        '''fig = px.bar(df, x='City', y='AQI',barmode='group')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)'''
        df2=df.loc[(df['City']==state), :]
        '''plt.plot(df2['AQI'])
        plt.title('Some Title')
        plt.xlabel('AQI')'''
        plt.bar(df2['AQI'],df2['PM2.5'], color ='maroon',width = 0.4)
        #plt.ylabel('Some measurements')
        plt.savefig('static/my_plot.png')
        states=df['City'].unique()
        return render_template('about.html',states=states)


@app.route('/predict/')
def predict():
    return render_template('predict.html')

@app.route('/result/',methods=['POST'])
def result():
    if request.method == "POST":
        a=int(request.form.get("a"))
        b=int(request.form.get("b"))
        c=int(request.form.get("c"))
        d=int(request.form.get("d"))
        e=int(request.form.get("e"))
        f=int(request.form.get("f"))
        g=int(request.form.get("g"))
        h=int(request.form.get("h"))
        i=int(request.form.get("i"))
        j=int(request.form.get("j"))
        k=int(request.form.get("k"))
        final_features = [[a,b,c,d,e,f,g,h,i,j,k]]
        label=model.predict(final_features)
        if label >=0 and label<=50:
            output="Good"
        elif label>=51 and label<=100:
            output="Moderate"
        elif label>=101 and label<=150:
            output="Unhealthy"
        elif label>=151 and label<=200:
            output="Unhealthy for Strong People"
        else:
            output="Hazardous"
        print(label)
        #flash(label)
       #first_name = request.form.get("fname")
        return render_template('predict.html', prediction_text=output)
    




if __name__ == "__main__":
  app.run()