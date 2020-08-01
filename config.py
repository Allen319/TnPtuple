import yaml

config  ={}
config['year'] = 2016
config['label'] = 'muonID'
config['sample'] = ['DY','RunF','RunE','RunB','RunC','RunD','RunG','RunH']
config['observable'] = ['pt','abseta','eta']
config['observable2D'] = {'eta':'pt','abseta':'pt'}
config['mass'] = [ 70 + 0.5*i for i in range(0, 121)]
config['binning'] = {'pt':[20, 25, 30, 40, 50, 60, 120, 200],
                     'abseta':[0.0,0.9,1.2,2.1,2.4],
										 'eta':[-2.4,-2.1,-1.2,-0.9,0.0,0.9,1.2,2.1,2.4]}
config['tree_name'] = 'fitter_tree'
config['dir_name'] = 'tpTree'
config['tag_selection'] = { 'pair_probeMultiplicity':1,
														'tag_pt':[29.0,''],
														'tag_abseta':[0.0,2.4],
														'tag_combRelIsoPF04':[0.0,0.15],
														'pair_deltaR':[0.4,''],
														'mass':[70.0,130],
														'tag_IsoMu27':1,
														'tag_glbChi2':[0.0, 10.0],
														'tag_glbValidMuHits':[0,''],
														'tag_numberOfMatchedStations':[1,''],
														'tag_dxyPVdzmin':[0.0, 0.2],
														'tag_dzPV':[0.0, 0.5],
														'tag_tkValidPixelHits':[0,''],
														'tag_tkTrackerLay':[5,''],
														}
config['flags']= {'tight':{'Tight2012':1,
														'pt':[10.0, ''],
														'abseta':[0.0, 2.4]
													},
									'medium':{'Medium':1,
														'pt':[10.0, ''],
                            'abseta':[0.0, 2.4],
														},

									'mediumPrompt':{'Medium':1,
														'dxyPVdzmin':[0.0, 0.02],
														'dzPV':[0.0, 0.1],
														'pt':[10.0, ''],
                            'abseta':[0.0, 2.4],
														},
									}

config['pdfs'] = {
			"voigtPlusExpo":[
											"mass[90,70,130]",
											"Voigtian::signalPass(mass, mean1p[90,80,100], width1p[2.495], sigma1p[3,1,20])",
											"Voigtian::signalFail(mass, mean1f[90,80,100], width1f[3,1,2], sigma1f[3,0,20])",
											"Exponential::backgroundPass(mass, lp[0,-10,10])",
											"Exponential::backgroundFail(mass, lf[0,-10,10])",
											"efficiency[0.9,0,1]",
											"signalFractionInPassing[0.9]"],
			"vpvPlusExpo" : [
											"mass[90,70,130]",
											"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
											"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
											"SUM::signalPass(vPropp[0.8,0,1]*signal1,signal2)",
										  "Voigtian::theSig1f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[2,1,3])",
											"Voigtian::theSig2f(mass, mean2f[90,80,100], width2f, sigma2f2[4,2,10])",
											"SUM::signalFail(vPropf[0.8,0,1]*theSig1f,theSig2f)",
											"Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
											"Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
											"efficiency[0.9,0,1]",
											"signalFractionInPassing[0.9]",
											],
			"vpvPlusExpoMin70":[
											"mass[90,70,130]",
											"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
											"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
											"SUM::signalPass(vPropp[0.8,0,1]*signal1,signal2)",
										  "Voigtian::theSig1f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[2,1,3])",
											"Voigtian::theSig2f(mass, mean2f[90,80,100], width2f, sigma2f2[4,2,10])",
											"SUM::signalFail(vPropf[0.8,0,1]*theSig1f,theSig2f)",
											"Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
											"Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
											"efficiency[0.9,0.7,1]",
											"signalFractionInPassing[0.9]",
												],
			"vpvPlusCheb" :[
											"mass[90,70,130]",
											"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
											"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
											"SUM::signalPass(vPropp[0.8,0,1]*signal1,signal2)",
										  "Voigtian::theSig1f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[2,1,3])",
											"Voigtian::theSig2f(mass, mean2f[90,80,100], width2f, sigma2f2[4,2,10])",
											"SUM::signalFail(vPropf[0.8,0,1]*theSig1f,theSig2f)",
											"RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
											"RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})",
											"efficiency[0.9,0.7,1]",
											"signalFractionInPassing[0.9]",
										],
			"vpvPlusCMS" : [
											"mass[90,70,130]",
											"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
											"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
											"SUM::signalPass(vPropp[0.8,0,1]*signal1,signal2)",
										  "Voigtian::theSig1f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[2,1,3])",
											"Voigtian::theSig2f(mass, mean2f[90,80,100], width2f, sigma2f2[4,2,10])",
											"SUM::signalFail(vPropf[0.8,0,1]*theSig1f,theSig2f)",
											"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
											"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)",
											"efficiency[0.9,0.7,1]",
											"signalFractionInPassing[0.9]",
											],
			"vpvPlusCMSbeta0p2" : [
											"mass[90,70,130]",
											 "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
											 "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])",
											 "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])",
											 "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)",
											 "SUM::signalPass(vPropp[0.8,0,1]*signal1,signal2)",
										  "Voigtian::theSig1f(mass, mean2f[90,80,100], width2f[3,1,2], sigma2f[2,1,3])",
											"Voigtian::theSig2f(mass, mean2f[90,80,100], width2f, sigma2f2[4,2,10])",
											"SUM::signalFail(vPropf[0.8,0,1]*theSig1f,theSig2f)",
											 "efficiency[0.9,0.7,1]",
											 "signalFractionInPassing[0.9]",
											],
											}
print(yaml.dump(config))
with open('config'+str(config['year'])+'.yaml', 'w') as f:
  yaml.dump(config, f)
