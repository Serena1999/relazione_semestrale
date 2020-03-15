#include "functions.hpp"


/*

questo programma legge tutte le serie dal file di input ed esegue la selezione
scrivendo poi sul file di output i dati scelti e poi quelli scartati li mette
nel file "*.bad"

esecuzione programma:
"filtro.exe -in file_input.txt -out file_output.txt -maxRatio 3 -minV 0.2"

parametri:
	-Nskip                osa solo un dato ogni Nskip, e' usato per  fare prove veloci (default = DEFAULT_NSKIP)
    -in [file input]      nome/percorso del file di input (default = DEFAULT_INPUT_FILE_NAME)
	-out [file output]    nome/percorso del file di output (default = DEFAULT_OUTPUT_FILE_NAME)
	-maxRatio [val]       valore (numerico) per la soglia di scarto dei punti (default = DEFAULT_MAX_RATIO)
	-minV [val]           i punti con le x minori di questo valore vengono scartati (default = DEFAULT_MIN_V)
	-outSigma [val]       parametro per gli outliers (default = DEFAULT_OUTLIERS_SIGMA)

*/

int main(int argc, char** argv)
{
	std::cout << "Hello there!" << std::endl;

	std::string fileNameIn = DEFAULT_INPUT_FILE_NAME;
	std::string fileNameOut = DEFAULT_OUTPUT_FILE_NAME;
	double maxRatio = DEFAULT_MAX_RATIO;
	double outSigma = DEFAULT_OUTLIERS_SIGMA;
	double minV = DEFAULT_MIN_V;
	int Nskip = DEFAULT_NSKIP;

	// parsing parametri
	for (int i = 1; i < argc; ++i)
	{
		if (std::string(argv[i]) == "-in")
			if (i + 1 < argc)
				fileNameIn = argv[++i];

		if (std::string(argv[i]) == "-out")
			if (i + 1 < argc)
				fileNameOut = argv[++i];

		if (std::string(argv[i]) == "-maxRatio")
			if (i + 1 < argc)
				maxRatio = std::stod(argv[++i]);

		if (std::string(argv[i]) == "-minV")
			if (i + 1 < argc)
				minV = std::stod(argv[++i]);

		if (std::string(argv[i]) == "-Nskip")
			if (i + 1 < argc)
				Nskip = std::stoi(argv[++i]);

		if (std::string(argv[i]) == "-outSigma")
			if (i + 1 < argc)
				outSigma = std::stoi(argv[++i]);
	}


	// legge file di dati da analizzare
	std::cout << "Lettura file: " << fileNameIn << std::endl;
	RunSet set = readFile(fileNameIn);// set contiene tutti i dati

	// esegue la selezione dei dati
	std::cout << "Selezione dati... " << std::endl;
	auto [out, out_bad] = selectData(set, maxRatio, minV, outSigma, Nskip);

	// salva su file
	std::cout << "Salva file: " << fileNameOut << std::endl;
	std::ofstream outFile(fileNameOut, std::ifstream::out);
	outFile << out << std::endl;
	std::cout << "Salva file: " << fileNameOut+".bad" << std::endl;
	std::ofstream outFile_bad(fileNameOut + ".bad", std::ifstream::out);
	outFile_bad << out_bad << std::endl;

	std::cout << "FINE!" << std::endl;

	return 0;
}







/*
std::cout << "inizio" << std::endl;
std::default_random_engine generator;
std::uniform_real_distribution<double> distribution(5.0, 10.0);
std::this_thread::sleep_for(std::chrono::seconds((int)distribution(generator)));
std::cout << "fine" << std::endl;
return 0;
*/




