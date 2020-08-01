#include <iostream>
#include <vector>

#include <TROOT.h>
#include <TH1F.h>
#include <TH1I.h>
#include <TCanvas.h>
#include <TFile.h>

#include "Ntuple.h"
#include "ArgParser.h"
#include "SmartSelectionMonitor.h"
#include "yaml-cpp/yaml.h"

int main(int argc, const char *argv[]) {
  gROOT->SetBatch(kTRUE);

	
  TString configFilePath = "../config.yaml";	
  TString sample_name = "";
	TString outputFile = "";
	//--- Parse the arguments -----------------------------------------------------
  if (argc > 1) {
    for (int i = 1; i < argc; ++i) {
      TString currentArg = argv[i];
      //--- possible options ---
      if (currentArg.BeginsWith("config=")) {
        getArg(currentArg, configFilePath);
      }
      else if (currentArg.BeginsWith("input=")) {
        getArg(currentArg, sample_name);
      }
			else if (currentArg.BeginsWith("output=")) {
				getArg(currentArg, outputFile);
			}
    }
  }


  YAML::Node config = YAML::LoadFile(configFilePath.Data());
 	double massBinning[config["mass"].size()];
	for(std::size_t i=0;i<config["mass"].size();i++)
	{
		massBinning[i] = (config["mass"][i].as<double>());
	}
	/*for (YAML::const_iterator it=config["binning"]["abseta"].begin();it!=config["binning"]["abseta"].end();++it) {
  	absetaBinning[(int)it] = (it->as<double>());
	}
 	*/
	SmartSelectionMonitor mon;	
	for(std::size_t i=0;i<config["observable"].size();i++)
	{
		std::cout<<config["observable"][i].as<std::string>()<<std::endl;
		mon.addHistogram(new TH1F(TString(config["observable"][i].as<std::string>()),TString(config["observable"][i].as<std::string>()) ,sizeof(massBinning)/sizeof(double)-1, massBinning));
	}
	for (YAML::const_iterator it=config["observable2D"].begin();it!=config["observable2D"].end();++it)
	{
		mon.addHistogram(new TH1F(TString(it->first.as<std::string>())+TString(it->second.as<std::string>()),TString(it->first.as<std::string>())+TString(it->second.as<std::string>()),sizeof(massBinning)/sizeof(double)-1, massBinning));
	}
	//mon.addHistogram(new TH1F("pt", "pt distribution",sizeof(massBinning)/sizeof(double)-1,massBinning)) ;
	//mon.addHistogram(new TH1F("abseta", "abseta distribution" ,sizeof(massBinning)/sizeof(double)-1,massBinning));
	//TH1F pt_h("pt", "pt distribution", sizeof(ptBinning)/sizeof(double)-1,ptBinning);
	//TH1F abseta_h("pt", "pt distribution", sizeof(absetaBinning)/sizeof(double)-1,absetaBinning);
  TString tree_name(config["tree_name"].as<std::string>());
  TString dir_name(config["dir_name"].as<std::string>());
  Ntuple n(tree_name.Data());
  std::cout<<(sample_name+"/"+dir_name+"/"+tree_name).View(); 
	n.add((sample_name+"/"+dir_name+"/"+tree_name).Data());
  ULong64_t entries = n.GetEntries();
  std::cout << "Entries: " << entries << std::endl;
	for (ULong64_t entry = 0; entry < entries; ++entry) {
    n.GetEntry(entry);
		bool passTag = true;
		for(YAML::const_iterator it=config["tag_selection"].begin();it!=config["tag_selection"].end();++it)
		{
			if(it->second.Type() == 3)
			{	
				if(n.val<Float_t>(it->first.as<std::string>()) < it->second[0].as<double>()) passTag = false;
				if( it->second[1].as<std::string>() != "")
				{	
					if(n.val<Float_t>(it->first.as<std::string>()) > it->second[1].as<double>())
					{
						passTag = false;
					}
				}
			}
			else if(it->second.Type() == 2)
			{
				if(n.val<Int_t>(it->first.as<std::string>()) != it->second.as<int>())
				{	
					passTag = false;
					//std::cout<< it->first.as<std::string>() << "fail" <<std::endl;
				}
			}
			else{
				std::cout<<it->first.as<std::string>()<<"errrrrrrrrrrrrrrrrrrror"<<std::endl;
			}
		}
		if (passTag == false) continue;
		
	
		for(YAML::const_iterator mother = config["flags"].begin();mother !=config["flags"].end();++mother)
		{	
			bool passProbe = true;
			
			for (YAML::const_iterator it = mother->second.begin(); it !=mother->second.end();++it)
			{
				if(it->second.Type() == 3)
				{	
					if(n.val<Float_t>(it->first.as<std::string>()) < it->second[0].as<double>()) passProbe = false;
					if( it->second[1].as<std::string>() != "")
					{	
						if(n.val<Float_t>(it->first.as<std::string>()) > it->second[1].as<double>())
						{
							passProbe = false;
						}
					}
				}
				else if(it->second.Type() == 2)
				{
					if(n.val<Int_t>(it->first.as<std::string>()) != it->second.as<int>())
					{	
						passProbe = false;
					}
				}
				else{
					std::cout<<it->first.as<std::string>()<<"errrrrrrrrrrrrrrrrrrror"<<std::endl;
				}
			}
		
			for(std::size_t i=0;i<config["observable"].size();i++)
			{
				TString obs(config["observable"][i].as<std::string>());
				for(std::size_t j=0;j<config["binning"][config["observable"][i].as<std::string>()].size()-1;j++)
				{
					if(n.val<Float_t>(config["observable"][i].as<std::string>()) > config["binning"][config["observable"][i].as<std::string>()][j].as<double>() &&
						n.val<Float_t>(config["observable"][i].as<std::string>()) < config["binning"][config["observable"][i].as<std::string>()][j+1].as<double>())
					{	
						mon.fillHisto(obs,std::to_string(j+1)+"_"+mother->first.as<std::string>()+std::to_string(passProbe),n.val<Float_t>("mass"), 1.0);
						mon.fillHisto(obs,std::to_string(j+1)+"_"+mother->first.as<std::string>()+"total",n.val<Float_t>("mass"), 1.0);
					}
				}
			}
			for (YAML::const_iterator it=config["observable2D"].begin();it!=config["observable2D"].end();++it)
			{
				TString obs(TString(it->first.as<std::string>())+TString(it->second.as<std::string>()));
				for(std::size_t i=0;i<config["binning"][it->first.as<std::string>()].size()-1;i++)
				{
					for(std::size_t j=0;j<config["binning"][it->second.as<std::string>()].size()-1;j++)
					{
						if(n.val<Float_t>(it->first.as<std::string>()) > config["binning"][it->first.as<std::string>()][i].as<double>() &&
							 n.val<Float_t>(it->first.as<std::string>()) < config["binning"][it->first.as<std::string>()][i+1].as<double>() &&
							 n.val<Float_t>(it->second.as<std::string>()) > config["binning"][it->second.as<std::string>()][j].as<double>() &&
							 n.val<Float_t>(it->second.as<std::string>()) < config["binning"][it->second.as<std::string>()][j+1].as<double>())
						{
							mon.fillHisto(obs,TString(std::to_string(i+1))+"-"+TString(std::to_string(j+1))+"_"+mother->first.as<std::string>()+std::to_string(passProbe), n.val<Float_t>("mass"), 1.0);
							mon.fillHisto(obs,TString(std::to_string(i+1))+"-"+TString(std::to_string(j+1))+"_"+mother->first.as<std::string>()+"total", n.val<Float_t>("mass"), 1.0);
						}
					}
				}
			}
		}
		//pt_h.Fill(n.val<Float_t>("pt"));
    //abseta_h.Fill(n.val<Float_t>("abseta"));
  }
	TFile *f1 = new TFile(outputFile,"recreate");
	mon.Write();
	f1->Close();
	/*
  TCanvas c("c", "c", 400, 400);
  pt_h.Draw();
  c.SaveAs("pt.pdf");
  c.Clear();
  abseta_h.Draw();
  c.SaveAs("abseta.pdf");
	*/
	
	return 0;
}
