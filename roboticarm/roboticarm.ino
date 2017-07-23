#include <Servo.h> 
 
Servo shoulder;  // create servo object to control a shoulder servo 
Servo elbow;  // create servo object to control a elbow servo 
Servo wrist;  // create servo object to control a wrist servo
Servo gripper;  // create servo object to control a gripper servo 
               
int value=0;// variable to store the servo position 
char ReceivedLetter;            // Character received from Serial.                                |
String message;                 // String(message) received from Serial.                          | 
String Receivednumber;          // Number received in form of a string from Serial.               | Serial Declarations.
int Original_number;            // Final Integer value of the number received from the Serial.    |                             //                                                                  |

void setup() 
{ 
  shoulder.attach(9);  // attaches the shoulder servo on pin 9 to the servo object 
  elbow.attach(10);  // attaches the elbow servo on pin 10 to the servo object
  wrist.attach(11);  // attaches the wrist servo on pin 11 to the servo object  
  gripper.attach(12);  // attaches the gripper servo on pin 12 to the servo object 
  Serial.begin(9600);
} 
 
void loop() 
{ 
  while(Serial.available()>0)
  {
    message = Serial.readStringUntil('\n');         // Storing the String received in variable message.
    ReceivedLetter=message.charAt(0);               // Taking the Letter received from the String in Variable ReceivedLetter.
    Receivednumber = message.substring(1);          // Extracting the Numerical value from the message.
    Original_number = Receivednumber.toInt();       // Decoding the real value of the number from the message.
    Serial.println(Original_number);
    if (ReceivedLetter == 'S')
    {
      shoulder.write(Original_number);
      delay(50);
    }
    else if (ReceivedLetter == 'E')
    {
      elbow.write(Original_number);
      delay(50);
    }
    else if (ReceivedLetter == 'W')
    {
      wrist.write(Original_number);
      delay(50);
    }
    else if (ReceivedLetter == 'G')
    {
      gripper.write(Original_number);
      delay(50);
    }
  delay(20);      
    
  }
}
  
  
  
  

