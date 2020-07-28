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

		if dd =='India':
			l1 = results[0]['name']
			l2 = results[0]['admin1']
			l3 = df[ df['Code']==results[0]['cc']]['Name'].values[0]
			ans+='\nCity - '+l1+'\nState/Neighbourhood - '+l2+'\nCountry - '+l3
		else:
			l1='None'
			l2='None'
			l3= dd
			ans+='\n'+l3
	
		df1=pd.read_csv('../Travel_Risk_Analysis_Internship/data/district_info.csv')
		df1.set_index('District',inplace=True)

		df2=pd.read_csv('../Travel_Risk_Analysis_Internship/data/state_info.csv')
		df2.set_index('State',inplace=True)

		df3=pd.read_csv('../Travel_Risk_Analysis_Internship/data/country_info.csv')
		df3.set_index('country',inplace=True)
	
	
	
		try:
			dfff = pd.read_csv('../Travel_Risk_Analysis_Internship/advisory_info_from_api.csv')
			dfff.set_index('Code',inplace=True)
			dfff.head()

			ans+="\n Risk Rating  : "+dfff.loc[ results[0]['cc'] , 'Risk_Rating']
			ans+="\n Advice  : "+dfff.loc[ results[0]['cc'] , 'Advice']
		except:
			ans+="No advisory risk score and short advice found"

		ans=ans.replace('\n','<br>')

		return render_template('index.html',entered_text=ans)

	return render_template("index.html")






if __name__ == "__main__":
	app.run(debug = True)

