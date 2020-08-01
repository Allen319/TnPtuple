#include "yaml-cpp/yaml.h"
#include <iostream>

using namespace std;

int main()
{
	YAML::Emitter out;
	out << "Hello World!";

	cout << "Here's the output YAML:\n" << out.c_str() << endl;
	YAML::Node config = YAML::LoadFile("../config.yaml");
	//for(int i = 0 ; i < config["sample"].size(); i++) cout << "samples:" << config["sample"].at(i) << endl;
	/*
	for(YAML::const_iterator it= config["sample"].begin(); it != config["sample"].end();++it)
	{
		cout << "samples:" << it->first.as<string>() << endl;
	}
	*/


	return 0;
}

