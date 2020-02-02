#include <stdio.h>
#include <ctype.h>

int AC_LOAD = 3;    // Output to Opto Triac pin
int  dimming;
byte bufferek[8] ;// Dimming level (0-128)  0 = ON, 128 = OFF
String data="100";
void setup()
{
  Serial.begin(115200);
  pinMode(AC_LOAD, OUTPUT);// Set AC Load pin as output
  attachInterrupt(0, zero_crosss_int, RISING);  // Choose the zero cross interrupt # from the table above

}

void serialEvent(){
  if(Serial.available()){
    Serial.println("serial av");
    while(Serial.available()){     
      data=data+Serial.read();      
    } 
    Serial.println(data);
    int x=data.indexOf("33");
    int y=data.indexOf("333");
    if (x==y)
    {
      x=x+1;
    }
    if (data.substring(0,3)=="100")
    {
      data=data.substring(3,x);
    }
    else
    {
      data=data.substring(0,x);
    }
    Serial.println(data);
    int m1,m2; 
    if(data.length()==2)
    { 
      m1=0;
      m2=data.toInt()-48;
    }
    else
    { 
      m1=(data.substring(0,2).toInt()-48)*10;
      m2=data.substring(2,4).toInt()-48;
     }
     dimming = m1+m2;
     Serial.println(dimming);
    }
    data="";
    
}
//the interrupt function must take no parameters and return nothing
void zero_crosss_int()  //function to be fired at the zero crossing to dim the light
{
        int dimtime = (96*dimming);    // For 60Hz =>65    
        delayMicroseconds(dimtime);    // Wait till firing the TRIAC    
         digitalWrite(AC_LOAD, HIGH);   // Fire the TRIAC
        delayMicroseconds(10);         // triac On propogation delay 
         // (for 60Hz use 8.33) Some Triacs need a longer period
        digitalWrite(AC_LOAD, LOW);    // No longer trigger the TRIAC (the next zero crossing will swith it off) TRIAC
   
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
