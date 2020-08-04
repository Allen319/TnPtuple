#!/usr/bin/env python3
import ROOT, array
ROOT.gROOT.LoadMacro('libCpp/RooCMSShape.cc+')
ROOT.gROOT.SetBatch(1)

import sys, getopt
import yaml
import copy

def do1DFit(rootFileName, obs, aBin, flag, theWorkSpace, outputDir):

	theWorkSpace.factory("expr::nSignalPass('efficiency*fSigAll*numTot', efficiency, fSigAll[0.9,0,1],numTot[1,0,1e10])") 
	theWorkSpace.factory("expr::nSignalFail('(1-efficiency)*fSigAll*numTot', efficiency, fSigAll,numTot)") 
	theWorkSpace.factory("expr::nBkgPass('effBkg*(1-fSigAll)*numTot', effBkg[0.9,0,1],fSigAll,numTot)") 
	theWorkSpace.factory("expr::nBkgFail('(1-effBkg)*(1-fSigAll)*numTot', effBkg,fSigAll,numTot)") 
	theWorkSpace.factory("SUM::passing(nSignalPass*signalPass,nBkgPass*backgroundPass)") 
	theWorkSpace.factory("SUM::failling(nSignalFail*signalFail,nBkgFail*backgroundFail)") 
	theWorkSpace.factory("expr::nPass('nSignalPass+nBkgPass',nSignalPass,nBkgPass)") 
	theWorkSpace.factory("expr::nFail('nSignalFail+nBkgFail',nSignalFail,nBkgFail)") 
	theWorkSpace.factory("SUM::tot(nPass*passing, nFail*failling)") 
	theWorkSpace.factory("SUM::bgExtended(nBkgPass*backgroundPass,theZero[0]*backgroundFail)") 

	TnPcat = ROOT.RooCategory("TnP","TnP")  
	TnPcat.defineType("passing")  
	TnPcat.defineType("failling")  


	simPdf= ROOT.RooSimultaneous("simPdf","simultaneous pdf",TnPcat)  
	simPdf.addPdf(theWorkSpace.pdf("passing"),"passing")  
	simPdf.addPdf( theWorkSpace.pdf("failling"),"failling")  

	rootFile = ROOT.TFile(rootFileName)
	nameofHisto = obs+"_"+str(aBin)+"_"+flag 
	histoPass = rootFile.Get(nameofHisto+"1") 
	histoFail = rootFile.Get(nameofHisto+"0") 
	histoAll = rootFile.Get(nameofHisto+"total") 
	print(histoFail)
	dataPass= ROOT.RooDataHist("dataPass","dataPass", ROOT.RooArgList(theWorkSpace.var("mass")),histoPass) 
	dataFail = ROOT.RooDataHist("dataFail","dataFail", ROOT.RooArgList(theWorkSpace.var("mass")),histoFail) 
	dataAll = ROOT.RooDataHist("dataAll","dataAll", ROOT.RooArgList(theWorkSpace.var("mass")),histoAll) 


	combData = ROOT.RooDataHist("combData","combined data", ROOT.RooArgList(theWorkSpace.var("mass")),ROOT.RooFit.Index(TnPcat),ROOT.RooFit.Import("passing", dataPass),ROOT.RooFit.Import("failling", dataFail))  


	simPdf.fitTo(combData)  
	simPdf.fitTo(combData)  
	simPdf.fitTo(combData)  


	xframe = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Passing"),ROOT.RooFit.Bins(50))  
	dataPass.plotOn(xframe) 
	theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.LineColor(ROOT.kGreen)) 
	#cmdArg1 = ROOT.RooLinkedList();
	#cmdArg1.Add(ROOT.RooFit.Components(ROOT.RooArgSet(theWorkSpace.pdf("backgroundPass"))))
	#cmdArg1.Add(ROOT.RooFit.LineStyle(ROOT.kDashed))
	#cmdArg1.Add(ROOT.RooFit.LineColor(ROOT.kGreen))
	
	theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.Components("backgroundPass"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen)) 
	#theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.Components(ROOT.RooArgSet(theWorkSpace.pdf("backgroundPass")))) 
	#theWorkSpace.pdf("passing").plotOn(xframe, cmdArg1)
	xframe2 = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Failling"),ROOT.RooFit.Bins(50))  
	dataFail.plotOn(xframe2) 
	theWorkSpace.pdf("failling").plotOn(xframe2,ROOT.RooFit.LineColor(ROOT.kRed)) 
	theWorkSpace.pdf("failling").plotOn(xframe2,ROOT.RooFit.Components("backgroundFail"), ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 

	xframe3 = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Total"),ROOT.RooFit.Bins(50))  
	dataAll.plotOn(xframe3) 
	theWorkSpace.pdf("tot").plotOn(xframe3,ROOT.RooFit.LineColor(ROOT.kBlue)) 


	numTot = theWorkSpace.var("numTot").getVal() 
	fSigAll = theWorkSpace.var("fSigAll").getVal() 
	efficiency = theWorkSpace.var("efficiency").getVal() 
	effBkg = theWorkSpace.var("effBkg").getVal() 

	theEfficiency = theWorkSpace.var("efficiency").getVal() 
	theEffError = theWorkSpace.var("efficiency").getError() 


	nbPass =  (efficiency*fSigAll*numTot+effBkg*(1-fSigAll)*numTot) 
	nbFail = ((1-efficiency)*fSigAll*numTot + (1-effBkg)*(1-fSigAll)*numTot) 

	print("nb pass ", nbPass)
	print("nbfail ",nbFail)


	c0 = ROOT.TCanvas("c0","coucou",800,800) 
	c0.SetFillColor(0) 
	c0.Divide(2,2) 

	c0.cd(1) 
	xframe.Draw() 

	c0.cd(2) 
	xframe2.Draw() 

	c0.cd(3) 
	xframe3.Draw() 

	c0.Print(outputDir+"/"+rootFileName.split("/")[-1][:-5]+"_"+nameofHisto+".png") 
	rootFile.Close()
	return (theEfficiency,theEffError)

def do2DFit(rootFileName, histoNames, obs1, obs2, firstBin, secondBin, flag, theWorkSpace, outputDir):

	theWorkSpace.factory("expr::nSignalPass('efficiency*fSigAll*numTot', efficiency, fSigAll[0.9,0,1],numTot[1,0,1e10])") 
	theWorkSpace.factory("expr::nSignalFail('(1-efficiency)*fSigAll*numTot', efficiency, fSigAll,numTot)") 
	theWorkSpace.factory("expr::nBkgPass('effBkg*(1-fSigAll)*numTot', effBkg[0.9,0,1],fSigAll,numTot)") 
	theWorkSpace.factory("expr::nBkgFail('(1-effBkg)*(1-fSigAll)*numTot', effBkg,fSigAll,numTot)") 
	theWorkSpace.factory("SUM::passing(nSignalPass*signalPass,nBkgPass*backgroundPass)") 
	theWorkSpace.factory("SUM::failling(nSignalFail*signalFail,nBkgFail*backgroundFail)") 
	theWorkSpace.factory("expr::nPass('nSignalPass+nBkgPass',nSignalPass,nBkgPass)") 
	theWorkSpace.factory("expr::nFail('nSignalFail+nBkgFail',nSignalFail,nBkgFail)") 
	theWorkSpace.factory("SUM::tot(nPass*passing, nFail*failling)") 
	theWorkSpace.factory("SUM::bgExtended(nBkgPass*backgroundPass,theZero[0]*backgroundFail)") 

	TnPcat = ROOT.RooCategory("TnP","TnP")  
	TnPcat.defineType("passing")  
	TnPcat.defineType("failling")  


	simPdf= ROOT.RooSimultaneous("simPdf","simultaneous pdf",TnPcat)  
	simPdf.addPdf(theWorkSpace.pdf("passing"),"passing")  
	simPdf.addPdf( theWorkSpace.pdf("failling"),"failling")  
	rootFile = ROOT.TFile(rootFileName)
	nameofHisto = obs1+obs2+"_"+str(firstBin)+"-"+str(secondBin)+"_"+flag 
	print(nameofHisto+"0")
	if nameofHisto+"0" in histoNames:
		histoFail = copy.deepcopy(rootFile.Get(nameofHisto+"0"))
	else:
		histoFail = copy.deepcopy(rootFile.Get(nameofHisto+"total"))
		histoFail.Scale(0.0)
		histoFail.SetEntries(0)
	if nameofHisto+"1" in histoNames:
		histoPass = rootFile.Get(nameofHisto+"1") 	
	else:	
		histoPass = copy.deepcopy(rootFile.Get(nameofHisto+"total"))
		histoPass.Scale(0.0)
		histoPass.SetEntries(0)
	histoAll = rootFile.Get(nameofHisto+"total") 
	dataPass= ROOT.RooDataHist("dataPass","dataPass", ROOT.RooArgList(theWorkSpace.var("mass")),histoPass) 
	dataFail = ROOT.RooDataHist("dataFail","dataFail", ROOT.RooArgList(theWorkSpace.var("mass")),histoFail) 
	dataAll = ROOT.RooDataHist("dataAll","dataAll", ROOT.RooArgList(theWorkSpace.var("mass")),histoAll) 


	combData = ROOT.RooDataHist("combData","combined data", ROOT.RooArgList(theWorkSpace.var("mass")),ROOT.RooFit.Index(TnPcat),ROOT.RooFit.Import("passing", dataPass),ROOT.RooFit.Import("failling", dataFail))  


	simPdf.fitTo(combData)  
	simPdf.fitTo(combData)  
	simPdf.fitTo(combData)  


	xframe = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Passing"),ROOT.RooFit.Bins(50))  
	dataPass.plotOn(xframe) 
	theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.LineColor(ROOT.kGreen)) 
	#cmdArg1 = ROOT.RooLinkedList();
	#cmdArg1.Add(ROOT.RooFit.Components(ROOT.RooArgSet(theWorkSpace.pdf("backgroundPass"))))
	#cmdArg1.Add(ROOT.RooFit.LineStyle(ROOT.kDashed))
	#cmdArg1.Add(ROOT.RooFit.LineColor(ROOT.kGreen))
	
	theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.Components("backgroundPass"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen)) 
	#theWorkSpace.pdf("passing").plotOn(xframe,ROOT.RooFit.Components(ROOT.RooArgSet(theWorkSpace.pdf("backgroundPass")))) 
	#theWorkSpace.pdf("passing").plotOn(xframe, cmdArg1)
	xframe2 = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Failling"),ROOT.RooFit.Bins(50))  
	dataFail.plotOn(xframe2) 
	theWorkSpace.pdf("failling").plotOn(xframe2,ROOT.RooFit.LineColor(ROOT.kRed)) 
	theWorkSpace.pdf("failling").plotOn(xframe2,ROOT.RooFit.Components("backgroundFail"), ROOT.RooFit.LineStyle(ROOT.kDashed),ROOT.RooFit.LineColor(ROOT.kRed)) 

	xframe3 = theWorkSpace.var("mass").frame(ROOT.RooFit.Title("TnP model Total"),ROOT.RooFit.Bins(50))  
	dataAll.plotOn(xframe3) 
	theWorkSpace.pdf("tot").plotOn(xframe3,ROOT.RooFit.LineColor(ROOT.kBlue)) 


	numTot = theWorkSpace.var("numTot").getVal() 
	fSigAll = theWorkSpace.var("fSigAll").getVal() 
	efficiency = theWorkSpace.var("efficiency").getVal() 
	effBkg = theWorkSpace.var("effBkg").getVal() 

	theEfficiency = theWorkSpace.var("efficiency").getVal() 
	theEffError = theWorkSpace.var("efficiency").getError() 


	nbPass =  (efficiency*fSigAll*numTot+effBkg*(1-fSigAll)*numTot) 
	nbFail = ((1-efficiency)*fSigAll*numTot + (1-effBkg)*(1-fSigAll)*numTot) 

	print("nb pass ", nbPass)
	print("nbfail ",nbFail)


	c0 = ROOT.TCanvas("c0","coucou",800,800) 
	c0.SetFillColor(0) 
	c0.Divide(2,2) 

	c0.cd(1) 
	xframe.Draw() 

	c0.cd(2) 
	xframe2.Draw() 

	c0.cd(3) 
	xframe3.Draw() 

	c0.Print(outputDir+"/"+rootFileName.split("/")[-1][:-5]+"_"+nameofHisto+".png") 
	rootFile.Close()
	return (theEfficiency,theEffError)
def main(argv):
	inputfile = ''
	outputdir = ''
	yamlfile = '../config.yaml'
	samplename = 'mc'
	fitmodel = 'vpvPlusExpo' #default
	try:
		opts, args = getopt.getopt(argv,"hi:o:y:s:f:",["inputFile=","outputDir=","yamlFile=", "sampleName=","fitModel="])
	except getopt.GetoptError:
		err_line  = ""
		err_line += "test.py -h\n"
		err_line += "-i input\n"
		err_line += "-o output\n"
		err_line += "-y configFile\n"
		err_line += "-f fitModel\n"
		err_line += "-s sampleName\n"
		print(err_line)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--inputFile"):
			inputfile = arg	
		elif opt in ("-o", "--outputDir"):
			outputdir = arg
		elif opt in ("-y", "--yamlFile"):
			yamlfile = arg
		elif opt in ("-s", "--sampleName"):
			samplename = arg
		elif opt in ("-f", "--fitModel"):
			fitmodel = arg
	f1 = ROOT.TFile(inputfile)
	f2 = open(yamlfile)
	config = yaml.load(f2)
	
	theWorkSpace = ROOT.RooWorkspace("theWorkSpace")
#	theWorkSpace.factory("mass[90,70,130]")
	for aLine in config["pdfs"][fitmodel]:
		theWorkSpace.factory(aLine) 
		print(aLine)	
	
	###write all histogram names in the list###	
	histoNames = []
	for i in range(0,f1.GetListOfKeys().Capacity()):
		histoNames.append(f1.GetListOfKeys().At(i).GetName())
	f1.Close()	
	### create root file to save emeofHistofficiencies
	#f3 = ROOT.TFile(outputdir+"/eff_"+samplename+".root","update")

	### 1D fit ###
	for flag in config['flags']:
		for obs in config['observable']:
			h1 = ROOT.TH1F(samplename+'_'+obs+'_'+flag, obs+' '+flag,len(config["binning"][obs])-1, array.array("d",config["binning"][obs]))
			for aBin in range (1,len(config["binning"][obs])):		
				effs = do1DFit(inputfile , obs , aBin, flag, theWorkSpace, outputdir)
				h1.SetBinContent(aBin, effs[0])
				h1.SetBinError(aBin, effs[1])
			f3 = ROOT.TFile(outputdir+"/eff_"+samplename+".root","update")
			h1.Write()
			f3.Close()
	
	### 2D fit ###
	for flag in config['flags']:
		for obs in config['observable2D']:
			h2 = ROOT.TH2F(samplename+'_'+obs+config['observable2D'][obs]+'_'+flag, obs+' '+config['observable2D'][obs]+' '+flag, len(config["binning"][obs])-1, array.array("d",config["binning"][obs]), len(config["binning"][config['observable2D'][obs]])-1, array.array("d",config["binning"][config['observable2D'][obs]]))
			for secondBin in range (1,len(config["binning"][config['observable2D'][obs]])):
				for firstBin in range (1,len(config["binning"][obs])):
					effs = do2DFit (inputfile ,histoNames, obs, config['observable2D'][obs], firstBin, secondBin, flag, theWorkSpace, outputdir)
					h2.SetBinContent(firstBin, secondBin, effs[0] )
					h2.SetBinError(firstBin, secondBin, effs[1] )
			f3 = ROOT.TFile(outputdir+"/eff_"+samplename+".root","update")
			h2.Write()
			f3.Close()

	### 2D fit with 1D binning ###
	for flag in config['flags']:
		for obs in config['observable2D']:
			for firstBin in range (1,len(config["binning"][obs])):
				h3 = ROOT.TH1F(samplename+'_'+config['observable2D'][obs]+'_'+obs+str(firstBin)+'_'+flag, obs+'%.1f'%config["binning"][obs][firstBin-1]+'-'+'%.1f'%config["binning"][obs][firstBin]+' '+config['observable2D'][obs]+' '+flag, len(config["binning"][config['observable2D'][obs]])-1, array.array("d",config["binning"][config['observable2D'][obs]]))
				for secondBin in range (1,len(config["binning"][config['observable2D'][obs]])):
					effs = do2DFit (inputfile,histoNames, obs, config['observable2D'][obs], firstBin, secondBin, flag, theWorkSpace, outputdir)
					h3.SetBinContent(secondBin, effs[0] )
					h3.SetBinError(secondBin, effs[1] )
				f3 = ROOT.TFile(outputdir+"/eff_"+samplename+".root","update")
				h3.Write()
				f3.Close()

if __name__ == '__main__':
	main(sys.argv[1:])
