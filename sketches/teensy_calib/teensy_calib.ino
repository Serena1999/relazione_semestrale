#include <ADC.h>
/*
 * Utilizzo:
 *   - Quando si manda "V" esegue N misure e stampa media e deviazione standard
 *     nel formato: "ADC_0_m  ADC_0_std  ADC_1_m  ADC_1_std"
 *   - quando iene richiesto "H" esegue Nhisto misure e stampa l'istogramma:
 *     "
 *     ADC_0_N0000  ADC_1_N0000
 *     ADC_0_N0001  ADC_1_N0001
 *     ADC_0_N0002  ADC_1_N0002
 *     ...
 *     ADC_0_N4095  ADC_1_N4095
 *     "
 */

#define N 10000
#define Nhisto 10000000

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

int *ch1Data = NULL, *ch2Data = NULL;

int myClamp(int x)
{
  if (x > 4095)
    return x - 65535;
  return x;
}

////////////////////////////////////////////////////////////////
// dichiarazione funzioni

void getMean(void);

////////////////////////////////////////////////////////////////
//                      FUNZIONI                              //
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////
void setup() {
  // put your setup code here, to run once:
  pinMode(chargePin, OUTPUT); digitalWrite(chargePin, LOW);
  pinMode(dischargePin, OUTPUT); digitalWrite(dischargePin, LOW);
  pinMode(pulsePin, OUTPUT); digitalWrite(pulsePin, HIGH);
  
  ch1Data = new int[N];
  ch2Data = new int[N];

  Serial.begin(9600);

  delay(5000);

  adc->setAveraging(1);
  adc->setResolution(12);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1);

  adc->startSynchronizedContinuousDifferential(readPin0P, readPin0N, readPin1P, readPin1N);
}

////////////////////////////////////////////////////////////////
void loop() {
  //getMean();

  if (Serial.available())
  {
    char c = Serial.read();
    if (c == 'v' || c == 'V')
      getMean();
    if (c == 'h' || c == 'H');
      //TODO
  }
}

////////////////////////////////////////////////////////////////
void getMean(void)
{
  ADC::Sync_result result;
  
  int sum0 = 0, sum1 = 0, v0, v1;
  int64_t s0 = 0, s1 = 0;
  for (int i = 0; i < N; i++)
  {
    while(!adc->isComplete());
    result = adc->readSynchronizedContinuous();
    v0 = myClamp((uint16_t)result.result_adc0);
    v1 = myClamp((uint16_t)result.result_adc1);
    sum0 += v0;
    sum1 += v1;
    s0 += v0*v0;
    s1 += v1*v1;
  }
  double m0 = (double)sum0 / N;
  double m1 = (double)sum1 / N;
  double var0 = ((double)s0 - m0 * m0 * N) / (N - 1);
  double var1 = ((double)s1 - m1 * m1 * N) / (N - 1);

  Serial.print(m0);
  Serial.print("  ");
  Serial.print(sqrt((double)var0 + 1));
  Serial.print("  ");
  Serial.print(sqrt(((double)var0 + 1)/N));
  Serial.print("  ");
  Serial.print(m1);
  Serial.print("  ");
  Serial.print(sqrt((double)var1 + 1));
  Serial.print("  ");
  Serial.println(sqrt(((double)var1 + 1)/N));
}
