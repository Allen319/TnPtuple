#!/usr/bin/env python3
import ROOT as rt
import os
import ROOT
from copy import deepcopy, copy
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from prettytable import PrettyTable
Runs = {'2017':['DY','data'],'2018':['DY','data']}
#refs = ['Mu17', 'DoubleIsoMu17Mu8_IsoMu17leg', 'DoubleIsoMu17Mu8_IsoMu8leg', 'DoubleIsoMu17Mu8_Mu17leg','DoubleIsoMu17Mu8_Mu8leg']
colorDict = {'DYnoPUreweighting':'crimson','closure':'blue','DY':'steelblue','data':'black', 'RunA':'orange','RunB':'limegreen','RunC':'indianred','RunD':'mediumpurple','RunE':'hotpink','RunF':'brown'}
etaBins= [0.0,0.9,1.2,2.1,2.4]

histos={}

def getEventEfficiency2D(th2):
	newEffHisto = th2.Clone()
	newEffHisto.SetDefaultSumw2()
	NbinsX = th2.GetNbinsX()
	NbinsY = th2.GetNbinsY()
	for x in range(NbinsX):
		for y in range(NbinsY):
			th2.SetBinContent(x+1,y+1,1-(1-th2.GetBinContent(x+1,y+1))*(1-th2.GetBinContent(x+1,y+1)))
			th2.SetBinError(x+1,y+1,(2-th2.GetBinContent(x+1,y+1))*th2.GetBinError(x+1,y+1))
	return th2

def getSoupEfficiency2D(refTh2,soupTh2):
	newEffHisto = refTh2.Clone()
	newEffHisto.SetDefaultSumw2()
	NbinsX = refTh2.GetNbinsX()
	NbinsY = refTh2.GetNbinsY()
	for x in range(NbinsX):
		for y in range(NbinsY):
			refBin = refTh2.GetBinContent(x+1,y+1)
			soupBin = soupTh2.GetBinContent(x+1,y+1)
			refErr = refTh2.GetBinError(x+1,y+1)
			soupErr = soupTh2.GetBinError(x+1,y+1)
			newEffHisto.SetBinContent(x+1,y+1, refBin*soupBin)
			newEffHisto.SetBinError(x+1,y+1,rt.TMath.Sqrt(refBin*refBin*soupErr*soupErr+soupBin*soupBin*refErr*refErr))
	return newEffHisto
def getEventEfficiency1D(th1):
	newEffHisto = th1.Clone()
	newEffHisto.SetDefaultSumw2()
	NbinsX = th1.GetNbinsX()
	for x in range(NbinsX):
		th1.SetBinContent(x+1,1-(1-th1.GetBinContent(x+1))*(1-th1.GetBinContent(x+1)))
		th1.SetBinError(x+1,(2-th1.GetBinContent(x+1))*th1.GetBinError(x+1))
	return th1
def getSoupEfficiency1D(refTh1,soupTh1):
	newEffHisto = refTh1.Clone()
	newEffHisto.SetDefaultSumw2()
	NbinsX = refTh1.GetNbinsX()
	for x in range(NbinsX):
		refBin = refTh1.GetBinContent(x+1)
		soupBin = soupTh1.GetBinContent(x+1)
		refErr = refTh1.GetBinError(x+1)
		soupErr = soupTh1.GetBinError(x+1)
		newEffHisto.SetBinContent(x+1, refBin*soupBin)
		newEffHisto.SetBinError(x+1,rt.TMath.Sqrt(refBin*refBin*soupErr*soupErr+soupBin*soupBin*refErr*refErr))
	return newEffHisto

def getSoup(eff1,eff2):
	return eff1*eff2

def getSoupError(eff1,err1,eff2,err2):
	return rt.TMath.Sqrt(eff1*eff1*err2*err2+eff2*eff2*err1*err1)

def getEfficiency(th2,name):
	newHisto = th2.Clone()
	newHisto.SetDefaultSumw2()
	newHisto.SetName(name)
	return newHisto
def getDiff(th2a,th2b,name):
	newHisto = th2a.Clone()
	newHisto.SetDefaultSumw2()
	newHisto.Add(th2b,-1)
	newHisto.SetName(name)
	return newHisto


def getWidth(th1):
	NbinsX = th1.GetNbinsX()
	width=[]
	for aBin in range(1,NbinsX+1):
		width.append(th1.GetBinWidth(aBin)/2)
	return width

def getPos(th1):
	NbinsX = th1.GetNbinsX()
	pos = []
	for aBin in range(1,NbinsX+1):
		pos.append(th1.GetBinCenter(aBin))
	return pos

def getMargin(th1):

	NbinsX = th1.GetNbinsX()
	margin = []
	for aBin in range(1,NbinsX+2):
		margin.append(th1.GetBinLowEdge(aBin))
		if aBin==NbinsX+2:
			margin.append(th1.GetBinLowEdge(aBin)+th1.GetBinWidth(aBin))
	return margin

def main():
	rt.TH1.SetDefaultSumw2()
	for year in Runs:
		for aRun in Runs[year]:
			histos[year+aRun+'ref_eta']=deepcopy(root_file.Get(year+aRun+"_ref_eta"))
			histos[year+aRun+'ref_pt'] =deepcopy(root_file.Get(year+aRun+"_ref_pt"))
			histos[year+aRun+'ref_pt_eta']=deepcopy(root_file.Get(year+aRun+"_ref_pt_eta"))
			histos[year+aRun+'ref_nvtx']=deepcopy(root_file.Get(year+aRun+"_ref_nvtx"))
	fig = plt.figure(1,(8,5))


	for obs in ["eta","pt","nvtx"]:
		for year in Runs:

			fig, ax = plt.subplots(2,1)
			for aRun in Runs[year]:
				name = year+aRun+"ref_"+obs
				bins = []
				errors = [[],[]]
				upperlims = []
				for aBin in range(1,histos[name].GetNbinsX()+1):
					bins.append(histos[name].GetBinContent(aBin))
					if histos[name].GetBinContent(aBin)+ histos[name].GetBinError(aBin)>1:
						errors[1].append(1-histos[name].GetBinContent(aBin))
						errors[0].append(histos[name].GetBinError(aBin))
					else:
						errors[1].append(histos[name].GetBinError(aBin))
						errors[0].append(histos[name].GetBinError(aBin))
				print(year,aRun)
				ax[0].errorbar(getPos(histos[name]), bins, fmt='', color = colorDict[aRun], ms=3, marker='o' , ls='none', xerr=getWidth(histos[name]), yerr=errors, label= year+aRun)
			ax[0].set_xticks(getMargin(histos[name]))
			ax[1].set_xticks(getMargin(histos[name]))
			for i in [0,1]:
				if obs == 'pt':
					ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.0f'))
				elif obs == 'eta':
					ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.1f'))
				else:
					ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.0f'))
			ax[0].set_xlim(getMargin(histos[name])[0],getMargin(histos[name])[-1] )

			ax[0].set_ylim(min(min(bins),0.9), 1.05)

			ax[0].set_title(ref)
			ax[0].set_ylabel('efficiency')

			ratios = []
			for aBin in range(1,histos[year+'data'+'ref_'+obs].GetNbinsX()+1):
				ratios.append(histos[year+'data'+'ref_'+obs].GetBinContent(aBin)/histos[year+'DY'+'ref_'+obs].GetBinContent(aBin))
			ax[1].errorbar(getPos(histos[year+'data'+'ref_'+obs]), ratios, fmt='', color = colorDict['data'], ms=3, marker='o' , ls='none', xerr=getWidth(histos[year+'data'+'ref_'+obs]))
			ax[1].set_ylim(min(min(ratios),0.95),max(max(ratios),1.05))
			ax[1].set_xlim(getMargin(histos[name])[0],getMargin(histos[name])[-1] )
			ax[1].set_ylabel('Data/MC')
			ax[1].set_xlabel(obs)
			ax[0].grid(True)
			ax[1].grid(True)
			ax[0].legend(loc='lower right',frameon=False)
			plt.savefig(year+'_'+ref+'_'+obs+'.png')
			plt.cla()
			plt.close()


if __name__ == '__main__':	
		labels = ["Tight","Tight_CMSShape","MediumPrompt","MediumPrompt_CMSShape"]
		for ref in labels:
			root_file = rt.TFile("eff_"+ref+".root")
			main()
