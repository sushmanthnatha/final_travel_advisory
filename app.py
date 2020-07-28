from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import reverse_geocoder as rg

app = Flask(__name__)

@app.route("/")
@cross_origin()
def main():
	return render_template('index.html')


@app.route("/advisoryinfo", methods = ["GET", "POST"])
@cross_origin()
def advisoryinfo():
	if request.method == "POST":
		dlat  = request.form["lat"]
		dlong = request.form["long"]

		ans=" You entered Latitute - {} \n Longiitude - {} ".format(dlat,dlong)

		latlong=(dlat,dlong)
		results=rg.search(latlong)
		df=pd.read_csv('../Travel_Risk_Analysis_Internship/country_isocode.csv')
		dd = df[ df['Code']==results[0]['cc']]['Name'].values[0] 
		ans+="\n "+dd
		

		ans=ans.replace('\n','<br>')

		return render_template('index.html',entered_text=ans)

	return render_template("index.html")






if __name__ == "__main__":
	app.run(debug = True)

