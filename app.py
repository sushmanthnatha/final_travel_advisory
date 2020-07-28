from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import reverse_geocoder as rg
import tempfile
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
			ans+='\n\n'+l3
	

		
		df1=pd.read_csv('../Travel_Risk_Analysis_Internship/data/district_info.csv')
		df1.set_index('District',inplace=True)

		df2=pd.read_csv('../Travel_Risk_Analysis_Internship/data/state_info.csv')
		df2.set_index('State',inplace=True)

		df3=pd.read_csv('../Travel_Risk_Analysis_Internship/data/country_info.csv')
		df3.set_index('country',inplace=True)
		
		


		try:
			dfff = pd.read_csv('../Travel_Risk_Analysis_Internship/advisory_info_from_api.csv')

			#dfff = pd.read_csv('./advisory_info_from_api.csv')
			dfff.set_index('Code',inplace=True)
			

			ans+="\n Risk Rating  : "+str(dfff.loc[ results[0]['cc'] , 'Risk_Rating'])
			ans+="\n Advice  : "+str(dfff.loc[ results[0]['cc'] , 'Advice'])
		#except Exception as e: ans+=e
		except:
			ans+="\n No advisory risk score and short advice found"



		
		try:
			with open('../Travel_Risk_Analysis_Internship/scrapy_sample/Alldata/'+l3+'.txt', 'r') as f:
				sid = SentimentIntensityAnalyzer()
				ss = sid.polarity_scores(f.read())  
				ans+='\n'+l3+'- Sentiment Analysis - 1 : '
				for i in ss.keys():
					ans+=i+'-'+str(ss[i])+' , '
				ans+='\n\n'
		#except Exception as e: ans+=e
		except:
			ans+='\nSentiment analysis cant be done due to internal error or mismatch error'
	
		
		if l1 in df1.index:
			x=list(df1.loc[l1,:])
			ans+=l1+'\nActive          : '+str(x[1])
			ans+='\nConfirmed       : '+str(x[0])
			ans+='\nDelta_Confirmed : '+str(x[2])
		elif l2 in df2.index : 
			x=list(df2.loc[l2,:])
			ans+=l2+'\nActive          : '+str(x[1])
			ans+='\nConfirmed       : '+str(x[0])
			ans+='\nDelta_Confirmed : '+str(x[2])
		elif l3 in df3.index :
			x=list(df3.loc[l3,:])
			ans+=l3+'\nTotal_Confirmed  : '+str(x[1])
			ans+='\nDelta_Confirmed  : '+str(x[0])
			ans+='\nTotal_Deaths     : '+str(x[3])
			ans+='\nDelta_Deaths     : '+str(x[2])
	
		else:
			ans+='Improper location / Details Not Found / Cant be shown due to name mismatch '
		
		ans+='\n\nCombined Advisory data of '+l3+' : \n\n'
	
		try:
			with open('../Travel_Risk_Analysis_Internship/scrapy_sample/Alldata/'+l3+'.txt', 'r') as f:
				ans+=f.read()
		except:
			ans+='Advisory file not found or mismatch or country name'
		
		ans=ans.replace('\n','<br>')

		return render_template('index.html',entered_text=ans)

	return render_template("index.html")






if __name__ == "__main__":
	app.run(debug = True)

