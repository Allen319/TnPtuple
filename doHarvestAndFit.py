#!/usr/bin/env python3
import sys, getopt
import re
import os
import yaml

def prepare_job_script():
    plotDirectory = jobsDirectory +"/"+year+"/plots"
    if not os.path.exists(plotDirectory):
      os.makedirs(plotDirectory)
    os.system("cp "+baseDir+"/env.sh " + jobsDirectory)
    #os.system("cp "+baseDir+"/fit.py " + jobsDirectory)
    if not "data" in samples:
      samples.append("data")
    for fileName in samples:
      for aModel in pdfs:
        if not os.path.exists(plotDirectory+"/"+aModel):
          os.makedirs(plotDirectory+"/"+aModel)
        scriptFile = open(jobsDirectory+'/jobs/'+'fithis_'+year+fileName+aModel+'.sh','w')
        scriptLines = ''
        scriptLines += ('export INITDIR='+baseDir+'\n')
        scriptLines += ('cd $INITDIR\n')
        scriptLines += '. ./env.sh ;\n'
        scriptLines += ("date;\n")
        scriptLines += (baseDir+"/python/fit.py -i "+jobsDirectory+"/"+year+"/histograms/"+fileName+".root"+" -y "+baseDir+"/config/"+aFile+" -o "+plotDirectory+"/"+aModel+"/"+" -s "+fileName +" -f "+aModel+";\n")
			#scriptLines += ("./fit.py -i "+subDirectory+fileName+".root" +" -s "+fileName+" -y "+baseDir+"/config/"+aFile+" -f "+aModel+" -o "+subDirectory+fileName+"_eff.root;\n")
        scriptFile.write(scriptLines)
        scriptFile.close()
        jobsFiles = open(jobsDirectory+"/jobs/sendFitJobs.cmd","a")
        jobsFiles.write("qsub  "+jobsDirectory+'/jobs/fithis_'+year+fileName+aModel+'.sh\n')
        jobsFiles.close()

def main():
    global jobsDirectory
    global baseDir
    baseDir = os.getcwd()
    jobsDirectory = baseDir+"/outputs/"+label 
    print(jobsDirectory +"/"+year+"/histograms/data.root")
    if not os.path.exists(jobsDirectory +"/"+year+"/histograms/data.root"):
      os.system("hadd "+jobsDirectory +"/"+year+"/histograms/data.root "+jobsDirectory +"/"+year+"/histograms/"+"Run*.root")
    prepare_job_script()

if __name__ == '__main__':
  files = os.listdir(os.getcwd()+"/config")
  for aFile in files:
    f = open("config/"+aFile)
    config = yaml.load(f)
    yaml.dump(config)

    label = str(config['label'])
    year =  str(config['year'])
    samples = config['sample']
    print(samples)
    pdfs = config['pdfs']
    main()  
  os.system("big-submission "+jobsDirectory+"/jobs/sendFitJobs.cmd")	
