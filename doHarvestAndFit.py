#!/usr/bin/env python3
import sys, getopt
import re
import os
import yaml

def prepare_job_script():
		plotDirectory = fitJobsDirectory +"/"+year+"/plots"
		if not os.path.exists(plotDirectory):
			os.makedirs(plotDirectory)
		if not os.path.exists(fitJobsDirectory +"/fitJobs"):
			os.makedirs(fitJobsDirectory +"/fitJobs")
		os.system("cp "+baseDir+"/env.sh " + fitJobsDirectory)
#os.system("cp "+baseDir+"/fit.py " + fitJobsDirectory)
		if not "data" in samples:
			samples["data"] = ""
		for fileName in samples:
			for aModel in pdfs:
				if not os.path.exists(plotDirectory+"/"+aModel):
					os.makedirs(plotDirectory+"/"+aModel)
				if not os.path.exists(plotDirectory+"/"+aModel+"/index.php"):
					os.system("cp "+baseDir+"/index.php "+ plotDirectory+"/"+aModel+"/index.php")
				scriptFile = open(fitJobsDirectory+'/fitJobs/'+'fithis_'+year+fileName+aModel+'.sh','w')
				scriptLines = ''
				scriptLines += ('export INITDIR='+baseDir+'\n')
				scriptLines += ('cd $INITDIR\n')
				scriptLines += '. ./env.sh ;\n'
				scriptLines += ("date;\n")
				scriptLines += (baseDir+"/python/fit.py -i "+fitJobsDirectory+"/"+year+"/histograms/"+fileName+".root"+" -y "+baseDir+"/config/"+aFile+" -o "+plotDirectory+"/"+aModel+"/"+" -s "+fileName +" -f "+aModel+";\n")
				#scriptLines += ("./fit.py -i "+subDirectory+fileName+".root" +" -s "+fileName+" -y "+baseDir+"/config/"+aFile+" -f "+aModel+" -o "+subDirectory+fileName+"_eff.root;\n")
				scriptFile.write(scriptLines)
				scriptFile.close()
				fitJobsFiles = open(fitJobsDirectory+"/fitJobs/sendFitJobs.cmd","a")
				fitJobsFiles.write("qsub  "+fitJobsDirectory+'/fitJobs/fithis_'+year+fileName+aModel+'.sh\n')
				fitJobsFiles.close()

def main():
    global fitJobsDirectory
    global baseDir
    baseDir = os.getcwd()
    fitJobsDirectory = baseDir+"/outputs/"+label 
    print(fitJobsDirectory +"/"+year+"/histograms/data.root")
    if not os.path.exists(fitJobsDirectory +"/"+year+"/histograms/data.root"):
      os.system("hadd "+fitJobsDirectory +"/"+year+"/histograms/data.root "+fitJobsDirectory +"/"+year+"/histograms/"+"Run*.root")
    prepare_job_script()

if __name__ == '__main__':
	files = os.listdir(os.getcwd()+"/config")
	labels=[]
	for aFile in files:
		f = open("config/"+aFile)
		config = yaml.load(f)
		yaml.dump(config)

		label = str(config['label'])
		if not label in labels:
			labels.append(label)
		year =  str(config['year'])
		samples = config['sample']
		print(samples)
		pdfs = config['pdfs']
		main()  
	for aLabel in labels:
		os.system("big-submission "+baseDir+"/outputs/"+aLabel+"/fitJobs/sendFitJobs.cmd")	
