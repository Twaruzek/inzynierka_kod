int AC_LOAD = 3;    // Output to Opto Triac pin
int  dimming=100;
byte bufferek[8] ;// Dimming level (0-128)  0 = ON, 128 = OFF
String data="100";
float y;
void setup()
{
  Serial.begin(115200);
  pinMode(AC_LOAD, OUTPUT);// Set AC Load pin as output
  attachInterrupt(0, zero_crosss_int, RISING);  // Choose the zero cross interrupt # from the table above
  
}
void serialEvent(){
  while(Serial.available()){
    data = Serial.readStringUntil("/n");
    if(data.length()<=3){
    dimming=data.toInt();
    Serial.println(dimming);
    }
}
}
//the interrupt function must take no parameters and return nothing
void zero_crosss_int()  //function to be fired at the zero crossing to dim the light
{
        float dimtime = (96*dimming); 
        float x = 0;// For 60Hz =>65   
        Serial.println(dimtime); 
        x=micros()-y;// Wait till firing the TRIAC 
        Serial.println(x);   
         if(x>=(dimtime-1000.0)&&x<(dimtime+10.0)){
          digitalWrite(AC_LOAD, HIGH);  
          Serial.println("FAAAAAAAAAAAAK");// Fire the TRIAC
         }
        if(x>=dimtime+10.0){
          digitalWrite(AC_LOAD, LOW);
          Serial.println(x);
          y=micros();
          Serial.println(x);
         }         // triac On propogation delay 
         // (for 60Hz use 8.33) Some Triacs need a longer period   // No longer trigger the TRIAC (the next zero crossing will swith it off) TRIAC

  // Firing angle calculation : 1 full 50Hz wave =1/50=20ms 
  // Every zerocrossing thus: (50Hz)-> 10ms (1/2 Cycle) 
  // For 60Hz => 8.33ms (10.000/120)
  // 10ms=10000us
  // (10000us - 10us) / 128 = 75 (Approx) For 60Hz =>65
}

void loop() {

    //dimming=data.toInt();
    //Serial.println(dimming);
}
