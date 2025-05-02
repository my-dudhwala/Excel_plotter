#define ANALOG_PIN A0
#define SAMPLE_RATE 450.0       // Hz
#define CUTOFF_FREQ 20.0        // Change this to adjust the filter

float pi = 3.14159265;

// Coefficients
float b0, b1, b2, a1, a2;
float x[3] = {0}, y[3] = {0};

unsigned long lastSampleTime = 0;
const unsigned long sampleIntervalMicros = 1000000.0 / SAMPLE_RATE;

// void computeButterworthCoefficients(float cutoff, float fs) {
//   float PI = 3.14159265;
//   float ita = 1.0 / tan(PI * cutoff / fs);
//   float q = sqrt(2.0); // For Butterworth 2nd-order

//   float norm = 1.0 / (1.0 + q * ita + ita * ita);
//   b0 = norm;
//   b1 = 2.0 * norm;
//   b2 = norm;
//   a1 = 2.0 * (1.0 - ita * ita) * norm;
//   a2 = (1.0 - q * ita + ita * ita) * norm;
// }

void computeButterworthCoefficients(float cutoff, float fs) {
  float ita = 1.0 / tan(pi * cutoff / fs);
  float q = sqrt(2.0); // For Butterworth 2nd-order

  float norm = 1.0 / (1.0 + q * ita + ita * ita);
  b0 = norm;
  b1 = 2.0 * norm;
  b2 = norm;
  a1 = 2.0 * (1.0 - ita * ita) * norm;
  a2 = (1.0 - q * ita + ita * ita) * norm;
}


void setup() {
  Serial.begin(115200);
  computeButterworthCoefficients(CUTOFF_FREQ, SAMPLE_RATE);
}

void loop() {
  unsigned long currentMicros = micros();
  if (currentMicros - lastSampleTime >= sampleIntervalMicros) {
    lastSampleTime = currentMicros;

    // Read analog value
    float input = (float)analogRead(ANALOG_PIN);

    // Shift previous samples
    x[2] = x[1]; x[1] = x[0]; x[0] = input;
    y[2] = y[1]; y[1] = y[0];

    // Apply filter
    y[0] = b0 * x[0] + b1 * x[1] + b2 * x[2]
         - a1 * y[1] - a2 * y[2];

    // Print values
    // Serial.print((int)input);
    // Serial.print(",");
    Serial.println((int)y[0]);
  }
}