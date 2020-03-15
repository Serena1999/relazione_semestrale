#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <array>
#include <chrono>
#include <thread>
#include <random>
#include <tuple>
#include <limits>

extern double m_2pi;
extern double normFactor;


#define DEFAULT_INPUT_FILE_NAME "file2C.txt"
#define DEFAULT_OUTPUT_FILE_NAME "file2Py.txt"
#define DEFAULT_MAX_RATIO 3.0
#define DEFAULT_OUTLIERS_SIGMA 3.0
#define DEFAULT_MIN_V 0.2
#define DEFAULT_NSKIP 1000

#define BAR_PRINT_EVERY 100



// ================================
//            CLASSI
// ================================

// rappresenta una riga del file
class Row
{
public:
	double V = 0, errV = 0, stdV = 0, I = 0, errI = 0, stdI = 0;
};

// rappresenta una serie di dati,
// in pratica è solo un std::vector<Row> a cui ho aggiunto le funzioni max e min
class RunData :
	public std::vector<Row>
{
public:

	// aggiorna max e min
	void update(void)
	{
		m_min = std::numeric_limits<double>::max();
		m_max = std::numeric_limits<double>::min();

		for (auto r : *this)
		{
			m_min = fmin(m_min, r.V);
			m_max = fmax(m_max, r.V);
		}
	}

	double min(void) const { return m_min; }
	double max(void) const { return m_max; }

private:
	double m_min = 0, m_max = 0;
};

//using Row = std::array<double, 6>;// una riga è formata da 6 numeri e una ciambella
//using RunData = std::vector<Row>;// rappresenta un blocco di dati (1 run)
using RunSet = std::vector<RunData>;// rappresetna un insieme di run

RunSet readFile(std::string fileName);

// stampa una riga
std::ostream& operator<<(std::ostream& stream, const Row& row);

// stampa un blocco
std::ostream& operator<<(std::ostream& stream, const RunData& data);

// stampa un insieme di blocchi separati da "#=======..."
std::ostream& operator<<(std::ostream& stream, const RunSet& set);

// ================================
//            FUNZIONI
// ================================

// serve per disegnare una barra di avanzamento su console
class ProgressBar
{
public:
	ProgressBar(int size = 50) : m_size(size) { drawLine(); }// inizia la barra
	~ProgressBar() { this->operator()(1); std::cout << std::endl; }// termina la barra

	void operator()(float progress)
	{
		m_progress = progress;
		carriageReturn();
		drawLine();
	}
private:
	float m_progress = 0;
	const int m_size;

	void drawLine()
	{
		std::cout << "[";
		for (int i = 0; i < m_size; i++)
		{
			if (i <= (int)(m_size * m_progress))
				std::cout << '=';
			else
				std::cout << ' ';
		}
		printf("] %.2f %%", m_progress * 100);
	}

	void carriageReturn(void)
	{
		std::cout << "\r";
	}
};

// quadrato di un DOUBLE (non mettere in template!)
inline double sqr(double x) { return x * x; }

// funzione gaussiana centrata in zero
inline double gaussian(double x, double sx) { return normFactor * exp(-sqr(x/sx) * 0.5) / sx; }

// ritorna media, varianza y, marianza su media
std::tuple<double, double, double> meanSigma(double x, const RunData& runData);

// ritorna vero se la varianza della media dei dati "from" all'indice "index" e < di quella di "to" * maxRatio
bool isPointSignificant(int index, const RunData& from, const RunData& to, double maxRatio, double outSigma);

// seleziona i dati
std::tuple<RunData, RunData> selectData(const RunSet& set, double maxRatio = DEFAULT_MAX_RATIO, double minV = DEFAULT_MIN_V, double outSigma = DEFAULT_OUTLIERS_SIGMA, int Nskip = DEFAULT_NSKIP);

#endif // !FUNCTIONS_H
