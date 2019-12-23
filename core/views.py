from django.shortcuts import render
from .forms import WaterQualityIndexForm
# Create your views here.
from django.shortcuts import redirect
from .models import *
def home(request):
	allpoints = WaterQualityIndex.objects.all()
	context = {
	'data_wqi' : allpoints,
	}
	return render(request,'home/home.html',context)

def new(request):
	if request.method=='POST':
		form_point = WaterQualityIndexForm(request.POST)
		if form_point.is_valid():
			print('form is valid')
			form_point.save()
			return redirect('home')
	else:
		form_point = WaterQualityIndexForm()
	context = {
	'form_point':form_point
	}
	return render(request,'newpoint.html',context)

def stats(request):
	all_wqidata = WaterQualityIndex.objects.all()
	WQIdata = WaterQualityIndex.objects.values('dissolved_oxygen','fecal_coliform','pH','bod5','deltaTemp','phosphate','nitrate','turbidity','ts')
	for experiment in WQIdata.values():
		if experiment['wqi'] is None:
			DO = experiment['dissolved_oxygen']
			FC = experiment['fecal_coliform']
			pH = experiment['pH']
			BOD5 = experiment['bod5']
			deltaTemp = experiment['deltaTemp']
			phosphate = experiment['phosphate']
			nitrate = experiment['nitrate']
			turbidity = experiment['turbidity']
			ts = experiment['ts']

			hesablama = hesablama_funksiyalari(Dissolved_Oxygen=DO,
			Fecal_Coliform = FC,
			pH = pH,
			BOD5 = BOD5,
			Delta_Temp = deltaTemp,
			Phosphate = phosphate,
			Nitrate=nitrate,
			Turbidity= turbidity,
			TS=ts)
			hesablama.q_deyerler()
			son_netice_wqi = hesablama.son_netice()
			print('sonsonson',str(son_netice_wqi))
			netice = ''
			if son_netice_wqi>90.0:
				netice = 'mukemmel'
			elif son_netice_wqi<=90.0 and son_netice_wqi>70.0:
				netice = 'yaxsi'
			elif son_netice_wqi<=70.0 and son_netice_wqi>50.0:
				netice = 'orta'
			elif son_netice_wqi<=50.0 and son_netice_wqi>25.0:
				netice = 'pis'
			else:
				netice = 'cox pis'
			WaterQualityIndex.objects.filter(id=experiment['id']).update(wqi=son_netice_wqi,level=netice)
			print("success")
		else:
			print(experiment['id'],"hesablanmisdir")
	context = {
	'results':all_wqidata,
	}
	return render(request,'stats.html',context)

	# IlkinMammadov98**


import math
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
class hesablama_funksiyalari:
	def __init__(self,Dissolved_Oxygen,Fecal_Coliform,pH,BOD5,Delta_Temp,Phosphate,Nitrate,Turbidity,TS):
		self.Dissolved_Oxygen = Dissolved_Oxygen
		self.Fecal_Coliform = Fecal_Coliform
		self.pH = pH
		self.BOD5 = BOD5
		self.Delta_Temp = Delta_Temp
		self.Phosphate = Phosphate
		self.Nitrate = Nitrate
		self.Turbidity = Turbidity
		self.TS = TS

		self.q_Dissolved_Oxygen = 0
		self.q_Fecal_Coliform = 0
		self.q_pH = 0
		self.q_BOD5 = 0
		self.q_Delta_Temp = 0
		self.q_Phosphate = 0
		self.q_Nitrate = 0
		self.q_Turbidity = 0
		self.q_TS = 0

		neticeler_listi = {}
	def q_deyerler(self):
		#init
		DO = self.Dissolved_Oxygen
		FC = self.Fecal_Coliform
		PH = self.pH
		bod = self.BOD5
		DT = self.Delta_Temp
		PT = self.Phosphate
		NT = self.Nitrate
		TB = self.Turbidity
		TSx = self.TS

		# Dissolved_Oxygen 
		if self.Dissolved_Oxygen<=100:
		 	self.q_Dissolved_Oxygen = -0.00000272*(DO)**4+0.000368*(DO)**3-0.004975*(DO)**2+0.509044*(DO)+1.376853
		elif self.Dissolved_Oxygen<=140 and self.Dissolved_Oxygen>100:
			self.q_Dissolved_Oxygen = 189.31*math(e)**(-0.0063*DO)
		else:
			self.q_Dissolved_Oxygen = 50

		# Fecal_Coliform
		if self.Fecal_Coliform<=1000:
		 	self.q_Fecal_Coliform = -11.332*math.log2(FC)+97.389
		elif self.Fecal_Coliform<=100000 and self.Fecal_Coliform>1000:
			self.q_Fecal_Coliform = -3.855*math.log2(FC)+45.952
		else:
			self.q_Fecal_Coliform = 2

		# pH
		if self.pH<2:
			self.q_pH = 0
		elif self.pH>2 and self.pH<=7.4:
			self.q_pH = -0.521223*(PH)**4+9.391153*(PH)**3-55.61814*(PH)**2+137.4489*(PH)-119.2418;
		elif self.pH>7.4 and self.pH<=12:
			self.q_pH = -0.7298*(PH)**4+29.54561*(PH)**3-440.069*(PH)**2+2835.152*(PH)-6572.185
		else:
			self.q_pH = 0

		# BOD5
		if self.BOD5<=30:
			self.q_BOD5 = 93.949*2.71828**(-0.1021*bod)
		else:
			self.q_BOD5 = 2

		# Delta_Temp
		if self.Delta_Temp<0:
			self.q_Delta_Temp = 3.818*(DT)+93.49
		else:
			self.q_Delta_Temp = -0.00043*(DT)**4+0.024654*(DT)**3-0.328228*(DT)**2-3.573817*(DT)+94.31032
		# Phosphate
		if self.Phosphate<=10:
			self.q_Phosphate = -16.969*math.log2(PT)+41.046
		else:
			self.q_Phosphate = 2

		# Nitrate
		if self.Nitrate<=70:
			self.q_Nitrate = 0.00000000383*(NT)**6-0.00000129*(NT)**5+0.000169*(NT)**4-0.010838*(NT)**3+0.363239*(NT)**2-6.996626*(NT)+94.4843
		elif self.Nitrate>70 and self.Nitrate<=75:
			self.q_Nitrate = 5
		elif self.Nitrate>75 and self.Nitrate<=80:
			self.q_Nitrate = 4
		elif self.Nitrate>80 and self.Nitrate<=85:
			self.q_Nitrate = 3
		elif self.Nitrate>85 and self.Nitrate<=100:
			self.q_Nitrate = 2
		else:
			self.q_Nitrate = 1

		# Turbidity
		if self.Turbidity<=100:
			self.q_Turbidity = 0.00000114*(TB)**4-0.000347*(TB)**3+0.039581*(TB)**2-2.434706*(TB)+97.4592
		else:
			self.q_Turbidity = 5

		# TS
		if self.TS>500:
			self.q_TS = 20
		else:
			self.q_TS = 0.0000000000107*(TSx)**5-0.0000000178*(TSx)**4+0.0000108*(TSx)**3-0.00299*(TSx)**2+0.246919*(TSx)+80.46506


	def son_netice(self):

		self.q_Dissolved_Oxygen = self.q_Dissolved_Oxygen * 0.17
		self.q_Fecal_Coliform = self.q_Fecal_Coliform * 0.16
		self.q_pH = self.q_pH * 0.11
		self.q_BOD5 = self.q_BOD5 * 0.11
		self.q_Delta_Temp = self.q_Delta_Temp * 0.11
		self.q_Phosphate = self.q_Phosphate * 0.1
		self.q_Nitrate = self.q_Nitrate * 0.1
		self.q_Turbidity = self.q_Turbidity * 0.08
		self.q_TS = self.q_TS * 0.07

		son_netice = self.q_Dissolved_Oxygen+self.q_Fecal_Coliform+self.q_pH+self.q_BOD5+self.q_Delta_Temp+self.q_Phosphate+self.q_Nitrate+self.q_Turbidity+self.q_TS
		self.neticeler_listi = {
		'Dissolved_Oxygen (Hell olmus oksigen)' : self.q_Dissolved_Oxygen,
		'Fecal_Coliform (Bagirsaq copu)' : self.q_Fecal_Coliform,
		'pH (potensial Hidrogen)' : self.q_pH,
		'BOD5 (Bioloji oksigen telebi)' : self.q_BOD5,
		'Delta_Temp (Temperatur)' : self.q_Delta_Temp,
		'Phosphate (Fosfat)' : self.q_Phosphate,
		'Nitrate (Nitrat)' : self.q_Nitrate,
		'Turbidity (Bulaniqliliq)' : self.q_Turbidity,
		'TS (Umumi madde miqdari)' : self.q_TS,
		}
		pprint(self.neticeler_listi)
		pprint('Son netice '+str(son_netice))
		return son_netice
	def vizual_netice(self):
		barsL = []
		neticelerL = []
		for key,val in self.neticeler_listi.items():
			barsL.append(key)
			neticelerL.append(val)
		ypos = np.arange(len(barsL))

		plt.bar(ypos,neticelerL)
		plt.xticks(ypos,range(1,len(barsL)))
		plt.show()



# hesablama.vizual_netice()