#!/usr/bin/env python3
import sys, getopt
import re
import os
import yaml

def prepare_job_script():
    plotDirectory = jobsDirectory +"/"+year
    if not os.path.exists(plotDirectory):
      os.makedirs(plotDirectory)
    if not os.path.exists(jobsDirectory +"/jobs"):
      os.makedirs(jobsDirectory +"/jobs")
    os.system("cp "+baseDir+"/bin/example_ntuple " + jobsDirectory)
    os.system("cp "+baseDir+"/env.sh " + jobsDirectory)
    subDirectory = jobsDirectory +"/"+year+"/histograms"
    if not os.path.exists(subDirectory):
      os.makedirs(subDirectory)
    for fileName in samples:
      scriptFile = open(jobsDirectory+'/jobs/'+'mkhis_'+year+fileName+'.sh','w')
      scriptLines = ''
      scriptLines += ('export INITDIR='+jobsDirectory+'\n')
      scriptLines += ('cd $INITDIR\n')
      scriptLines += '. ./env.sh ;\n'
      scriptLines += ("date;\n")
      scriptLines += ("./example_ntuple input="+baseDir+"/samples/"+year+fileName+".root"+" config="+baseDir+"/config/"+aFile+" output="+subDirectory+"/"+fileName+".root;\n")
			#scriptLines += ("./fit.py -i "+subDirectory+fileName+".root" +" -s "+fileName+" -y "+baseDir+"/config/"+aFile+" -f "+aModel+" -o "+subDirectory+fileName+"_eff.root;\n")
      scriptFile.write(scriptLines)
      scriptFile.close()
      jobsFiles = open(jobsDirectory+"/jobs/sendJobs.cmd","a")
      jobsFiles.write("qsub  "+jobsDirectory+'/jobs/mkhis_'+year+fileName+'.sh\n')
      jobsFiles.close()

def main():
    global jobsDirectory
    global baseDir
    baseDir = os.getcwd()
    jobsDirectory = baseDir+"/outputs/"+label 
    if not os.path.exists(jobsDirectory):
      os.makedirs(jobsDirectory)
    if not os.path.exists(jobsDirectory+"/jobs"):
      os.makedirs(jobsDirectory+"/jobs")
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
    os.system("big-submission "+jobsDirectory+"/jobs/sendJobs.cmd")	
