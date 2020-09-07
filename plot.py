#!/usr/bin/env python3 
import ROOT
import os, sys
import copy
import yaml
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def getBinsAndErrors(h_data):
  bins = []
  errors = [[], []]
  for aBin in range(1,h_data.GetNbinsX()+1): 
    bins.append(h_data.GetBinContent(aBin))
    
    if h_data.GetBinContent(aBin)+ h_data.GetBinError(aBin)>1:
      errors[1].append(1-h_data.GetBinContent(aBin))
      errors[0].append(h_data.GetBinError(aBin))
    else:
      errors[1].append(h_data.GetBinError(aBin))
      errors[0].append(h_data.GetBinError(aBin))
  return bins, errors

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

def saveAllHistos():
  histos = {}
  for i in range(0,f1.GetListOfKeys().Capacity()):                                                                                                       
    histoNames.append(f1.GetListOfKeys().At(i).GetName())

def main():
  plotDirectory = os.getcwd()+"/outputs/"+label+"/"+year+"/plots"
  for aPdf in pdfs:
    subDirectory = plotDirectory + "/" + aPdf
    f_data = ROOT.TFile(subDirectory+"/eff_data.root")
    f_mc   = ROOT.TFile(subDirectory+"/eff_DY.root")
    histos = {}
    for i in range(0,f_data.GetListOfKeys().Capacity()):                                                                                                       
      histos[f_data.GetListOfKeys().At(i).GetName()] = copy.deepcopy(f_data.Get(f_data.GetListOfKeys().At(i).GetName()))
    for i in range(0,f_mc.GetListOfKeys().Capacity()):                                                                                                       
      histos[f_mc.GetListOfKeys().At(i).GetName()] = copy.deepcopy(f_mc.Get(f_mc.GetListOfKeys().At(i).GetName()))
    histos_class = {}
    for i in range(0,f_data.GetListOfKeys().Capacity()):
      histos_class[f_data.GetListOfKeys().At(i).GetName()[5:]] = f_data.GetListOfKeys().At(i).GetClassName()
    print(histos_class)

    for aName in histos_class:
      if not histos_class[aName] == "TH1F":
        continue
      fig, ax = plt.subplots(2,1)
      data_bins, data_errors = getBinsAndErrors(histos["data_"+aName])
      mc_bins  , mc_errors   = getBinsAndErrors(histos["DY_" +aName])
      ax[0].errorbar(getPos(histos["data_"+aName]), 
        data_bins, 
        fmt='', 
        #color = colorDict[aRun], 
        ms=3, 
        marker='o' , 
        ls='none', 
        xerr=getWidth(histos["data_"+aName]), 
        yerr=data_errors, 
        label= "Data")
      ax[0].errorbar(getPos(histos["DY_"+aName]), 
        mc_bins, 
        fmt='', 
        #color = colorDict[aRun], 
        ms=3, 
        marker='o' , 
        ls='none', 
        xerr=getWidth(histos["DY_"+aName]), 
        yerr=mc_errors, 
        label= "MC")
      ax[0].set_xticks(getMargin(histos["data_"+aName]))
      ax[1].set_xticks(getMargin(histos["data_"+aName]))
      for i in [0,1]:
        if 'pt' in aName:
          ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.0f'))
        elif 'eta' in aName:
          ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.1f'))
        else:
            ax[i].xaxis.set_major_formatter(FormatStrFormatter('%5.0f'))
      ax[0].set_xlim(getMargin(histos["data_"+aName])[0],getMargin(histos["data_"+aName])[-1] )
      ax[0].set_ylim(min(min(min(data_bins),min(mc_bins)),0.8), 1.1)
      ax[0].set_title(aName.split("_")[-1])
      ax[0].set_ylabel('efficiency')
      ratios = []
      for i in range(0, len(data_bins)):
        ratios.append(data_bins[i]/mc_bins[i])
      ax[1].errorbar(getPos(histos["data_"+aName]), ratios, fmt='', ms=3, marker='o' , ls='none', xerr=getWidth(histos["data_"+aName]))
      ax[1].set_ylim(min(min(ratios),0.95),max(max(ratios),1.05))
      ax[1].set_xlim(getMargin(histos["data_"+aName])[0],getMargin(histos["data_"+aName])[-1] )
      ax[1].set_ylabel('Data/MC')
      ax[1].set_xlabel(aName.split("_")[1])
      ax[0].grid(True)
      ax[1].grid(True)
      ax[0].legend(loc='lower right',frameon=False)
      plt.savefig(subDirectory+"/eff1D_"+aName+'.png')
      plt.cla()
      plt.close()
    del f_data
    del f_mc



if __name__ == '__main__':
  files = os.listdir(os.getcwd()+"/config")
  #labels = []
  for aFile in files:
    f = open("config/"+aFile)
    config = yaml.load(f)
    yaml.dump(config)
    label = str(config['label'])
    year = str(config['year'])
    samples = config['sample']
    if not 'data' in samples:
      samples['data'] = ''
    pdfs = config['pdfs']
    obs = config['observable']
    obs2D = config['observable2D']
    flags = config['flags']
    main()
