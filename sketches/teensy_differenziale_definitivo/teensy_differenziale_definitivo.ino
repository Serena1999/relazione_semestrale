#include <ADC.h>

/*
 * Utilizzo:
 *   - seriale a 9600
 *   - mandare E per uscire dall'eventuale run corrente
 *   - Mandare R per ricominciare il nuovo run
 *   - ogni avvio inizia con "#R" e termina con "#E"
 *   - i dati sono inviati nella forma: "ADC_0_value  ADC_1_value"
 */

////////////////////////////////////////////////////////////////
// Definizione pin
const int readPin0P = A10;
const int readPin0N = A11;
const int readPin1P = A12;
const int readPin1N = A13;

const int out3Pin = A0;
const int chargePin = 15;
const int dischargePin = 16;
const int pulsePin = 13;

ADC *adc = new ADC(); // adc object

////////////////////////////////////////////////////////////////
// dichiarazione funzioni

// leggi la tensione del condensatore
float getCapVoltage(void);

// carica il condensatore a voltage, in un tempo massimo di maxSeconds
// restituisce false se non riesce nel tempo previsto
bool chargeToVoltage(float voltage, double maxSeconds = 20);

// attacca mosfet e acquisisce dati
bool acquisizione(void);

// carica il condensatore a capVoltage e chiama acquisizione()
bool acquisizione(float capVoltage);

void printData(void);

// controlla la seriale per il segnale di arresto e
// se per caso è stata raggiunta la tensione di lettura massima
bool shouldEnd(bool checkData = false);

// termina il programma e scarica il condensatore
void terminate(void);
bool shouldRestart(void);

////////////////////////////////////////////////////////////////
// variabili globali

// puntatori globali ai dati
int *ch1Data = NULL, *ch2Data = NULL;
const int nAcq = 100;// !!! DA CAMBIARE (100 ?)
float vMin = 0.1, vMax = 7.0, vStep = 0.01;// tensioni di partenza e di arrivo del condensatore, CAMBIARE!!!!!
int acqMultiplier = 1;

////////////////////////////////////////////////////////////////
//                      FUNZIONI                              //
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////
void setup() {
  // prima con questi pinMode non funzionava bene, teensy funziona diverso da arduino
  //pinMode(readPin0P, INPUT);
  //pinMode(readPin0N, INPUT);
  //pinMode(readPin1P, INPUT);
  //pinMode(readPin1N, INPUT);
  //pinMode(out3Pin, INPUT);
  pinMode(chargePin, OUTPUT); digitalWrite(chargePin, LOW);
  pinMode(dischargePin, OUTPUT); digitalWrite(dischargePin, LOW);
  pinMode(pulsePin, OUTPUT); digitalWrite(pulsePin, HIGH);

  // alloca spazio per i dati
  ch1Data = new int[nAcq];
  ch2Data = new int[nAcq];
  
  Serial.begin(9600);

  delay(5000);

  terminate();
}

int myClamp(int x)
{
  if (x > 4095)
    return x - 65535;
  return x;
}

////////////////////////////////////////////////////////////////
void loop() {
  
  for (float v = vMin; v <= vMax + vStep; v += vStep)
  {
    if (!acquisizione(v))
    {
      terminate();
      return;
    }
    printData();
    if (shouldEnd(true))
    {
      terminate();
      return;
    }
  }
  terminate();
  return;
}

////////////////////////////////////////////////////////////////
float getCapVoltage(void)
{
  // reimposta le impostazioni di ADC
  adc->setAveraging(32, ADC_0);
  adc->setResolution(12, ADC_0);
  adc->setReference(ADC_REFERENCE::REF_3V3, ADC_0);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::LOW_SPEED, ADC_0);
  adc->setAveraging(32, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setReference(ADC_REFERENCE::REF_3V3, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::LOW_SPEED, ADC_0);

  return 11.0 * 3.3 * adc->adc0->analogRead(out3Pin) / adc->adc0->getMaxValue();
}

////////////////////////////////////////////////////////////////
bool chargeToVoltage(float voltage, double maxSeconds)
{
  unsigned long t0 = millis();
  if (getCapVoltage() < voltage)
  {
    digitalWrite(chargePin, HIGH);
    while (getCapVoltage() < voltage)
    {
      if (millis() - t0 > maxSeconds * 1000)
      {
        digitalWrite(chargePin, LOW);
        return false;
      }
      if (shouldEnd(false))
      {
        digitalWrite(chargePin, LOW);
        return false;
      }
    }
    digitalWrite(chargePin, LOW);
  }
  if (getCapVoltage() > voltage)
  {
    digitalWrite(dischargePin, HIGH);
    while (getCapVoltage() > voltage)
    {
      if (millis() - t0 > maxSeconds * 1000)
      {
        digitalWrite(dischargePin, LOW);
        return false;
      }
      if (shouldEnd(false))
      {
        digitalWrite(dischargePin, LOW);
        return false;
      }
    }
    digitalWrite(dischargePin, LOW);
  }

  delay(10);
  return true;
}

////////////////////////////////////////////////////////////////
bool acquisizione(void)
{
  // classe per il ritorno dei risultati
  ADC::Sync_result result;

  // imposta i parametri per l'acquisizione differenziale continua
  adc->setAveraging(1);
  adc->setResolution(12);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1);

  // inizia l'acquisizione analogica continua
  adc->startSynchronizedContinuousDifferential(readPin0P, readPin0N, readPin1P, readPin1N);

  // attacca il MOS-FET
  digitalWrite(pulsePin, LOW);
  delayMicroseconds(50);// TODO: vedi se va bene e mangiare un panino

  //unsigned long t0 = micros();
  for (int i = 0; i < nAcq; i++)
  {
    // aspetta che sia completa una conversione
    while(!adc->isComplete());
    result = adc->readSynchronizedContinuous();
    ch1Data[i] = myClamp((uint16_t)result.result_adc0);
    ch2Data[i] = myClamp((uint16_t)result.result_adc1);
  }
  digitalWrite(pulsePin, HIGH);
  
  //Serial.print("ci ho impiegato tot us per conversione");
  //Serial.println((float)(micros()-t0) / nAcq);

  // ferma l'acquisizione
  adc->stopSynchronizedContinuous();

  return true;
}

////////////////////////////////////////////////////////////////
bool acquisizione(float capVoltage)
{
  bool flag = true;

  // carica il condensatore e controlla se ha funzionato
  flag = chargeToVoltage(capVoltage);
  if (flag == false)
    return flag;

  return acquisizione();
}

////////////////////////////////////////////////////////////////
void printData(void)
{
  //Serial.println("# data\nch1\tch2");
  for (int i = 0; i < nAcq; i++)
  {
    Serial.print(ch1Data[i]);
    Serial.print("    ");
    Serial.println(ch2Data[i]);
  }
  Serial.println("");
}

////////////////////////////////////////////////////////////////
bool shouldEnd(bool checkData)
{
   if (Serial.available() > 0)
   {
      char c = Serial.read();
      if (c == 'e' || c == 'E')
      {
        return true;
      }
   }

   if (checkData)
      for (int i = 0; i < nAcq; i++)
        if (ch1Data[i] + ch2Data[i] >= 4095)
        {
          return true;
        }

   return false;
}

////////////////////////////////////////////////////////////////
void terminate(void)
{
  Serial.println("# programma terminato!");
  Serial.println("#E");
  digitalWrite(dischargePin, HIGH);
  while(!shouldRestart());
  Serial.println("#R");
  Serial.println("# Riavvio, attendi...");
  delay(20000);
  digitalWrite(dischargePin, LOW);
}

////////////////////////////////////////////////////////////////
bool shouldRestart(void)
{
  if (Serial.available() > 0)
   {
      char c = Serial.read();
      if (c == 'r' || c == 'R')
        return true;
   }

   return false;
}
