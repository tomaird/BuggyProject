char previousInstr = 'T';
int boxNum = 0;

#define loopTime 10

//Standard PWM DC control; 1 = left, 2 = right
int E1 = 5;     //M1 Speed Control
int E2 = 6;     //M2 Speed Control
int M1 = 4;    //M1 Direction Control
int M2 = 7;    //M2 Direction Control

//Pin assignment - Movement
int FLPin = 2; //FrontLeft
int FRPin = 3;
int MLPin = 0;
int ALPin = 1;
int ARPin = 4;
int encoderPinL = 11;
int encoderPinR = 10;
int reedPin = 9;
int S1Pin = 12; //Switch 1 control pin
int S2Pin = 13; //Switch 2 control pin
//Pin assignment - Sensing
int switch1 = 15; // p1 and Gnd
int switch2 = 3; // Gnd and P2
int switch3 = 16; // for the boost converter and 5V with resistor supply @@@@@ dangerous @@@@@@@
int switch4 = 2; // to open circuit so no current flows to ground
int switch5 = 14; // for P2 to measure across high impedance 
int switch6 = 13; // switch between light sensors and black box sensors for p1

int P1 = 0;
int P2 = 5;
int Gnd = 4;

//Encoder count variables
int counterL = 0;
int counterR = 0;
int curStateL;
int curStateR;
int lastStateL;
int lastStateR;

//Light Sensor starting values
int FLStartVal; //front left
int FRStartVal; //front right
int MLStartVal; //middle left
int MRStartVal; //middle right
int ALStartVal; //additional left
int ARStartVal; //additional right

//Light sensor current values
int FLCurVal; //front left
int FRCurVal; //front right
int MLCurVal; //middle left
int MRCurVal; //middle right
int ALCurVal; //additional left
int ARCurVal; //additional right
int ARLow; //thersholds for comparison
int ARHigh;
int ALLow;
int ALHigh;

//Boundary value
int passedBoundary = 0;
int previous = 0; //0 for forwards, 1 for backwards

 //Reed value (for knowing when a box is reached)
int reedVal;

//Motor Control Values (possibly should be DEFINES instead of ints??)
int moveSpeed = 70; //Normal movement speed
int leftMoveSpeed = 71;
int rightMoveSpeed = 67;
int leftMoveSpeedBackward = 75;
int rightMoveSpeedBackward = 67;
int leftRotateSpeed = 70;
int rightRotateSpeed = 65;
int adjSpeed = 60; //Adjustment speed
int adjTime = 5; //Adjustment time (ms) - how often to poll sensors while doing an adjustment movement
int stopTime = 50;

//Colour values
static int blackMax = 1023;
static int blackMin = 401;
static int whiteMax = 400;
static int whiteMin = 0;
static int blackMinFrontMiddle = 101;
static int whiteMaxFrontMiddle = 100;

int sensorValueP1 = 0;
int sensorValueGnd = 0;
int sensorValueP2 = 0;
double array[4];

int OUT_PIN = 0;
int IN_PIN = 0;
const float IN_STRAY_CAP_TO_GND = 24.48;
const float IN_CAP_TO_GND = IN_STRAY_CAP_TO_GND;
const float R_PULLUP = 34.8;
const int MAX_ADC_VALUE = 1023;


void setup() {
	Serial1.begin(38400);
	pinMode(FLPin, OUTPUT);
	pinMode(FRPin, OUTPUT);
	pinMode(MLPin, OUTPUT);
	pinMode(ARPin, OUTPUT);
	pinMode(ALPin, OUTPUT);
	pinMode(switch1, OUTPUT);
	pinMode(switch2, OUTPUT);
	pinMode(switch4, OUTPUT);
	digitalWrite(switch4, LOW);
	pinMode(P1, INPUT); // gnd
	pinMode(P2, INPUT); // p2
	pinMode(Gnd, INPUT); // p1
}

void loop(void)
{
	if (Serial1.available()) {
		char val = Serial1.read();
		if (val != -1)
		{
			switch (val)
			{
			case 't':
				printSensorVals();
				break;
			case 'y':
				printAnalogVals();
				break;
			case 'F':
				previousInstr = 'F';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				forwardOne();
				Serial1.println("F Done");
				break;
			case 'B':
				previousInstr = 'B';
				backwardOne();
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				Serial1.println("B Done");
				break;
			case 'R':
				previousInstr = 'R';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				rotateRight90();
				delay(10);
				forwardSlightly();
				forwardSlightly();
				Serial1.println("R Done");
				break;
			case 'L':
				previousInstr = 'L';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				rotateLeft90();
				delay(10);
				forwardSlightly();
				Serial1.println("L Done");
				break;
			case 'Q':
				previousInstr = 'Q';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				rotateLeft90();
				delay(10);
				rotateLeft90();
				delay(10);
				forwardSlightly();
				delay(10);
				forwardSlightly();
				Serial1.println("1 Done");
				break;
			case 'V':
				previousInstr = 'V';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				rotateLeft90();
				rotateLeft90();
				rotateLeft90();
				rotateLeft90();
				rotateLeft90();
				forwardOne();
				rotateLeft90();
				rotateLeft90();
				forwardSlightly();
				forwardSlightly();
				forwardOne();
				Serial1.println("V Done");
				break;
			case 'S':
				previousInstr = 'S';
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				forwardBox();
				Serial1.println("S Done");
				break;
			case 'T':
				Serial1.println("Connection Established");
				break;
			case '1':
				boxNum = 1;
				Serial1.println("1 Done");
				break;
			case '2':
				boxNum = 2;
				Serial1.println("2 Done");
				break;
			case '3':
				boxNum = 3;
				Serial1.println("3 Done");
				break;
			case '4':
				boxNum = 4;
				Serial1.println("4 Done");
				break;
			case '5':
				boxNum = 5;
				Serial1.println("5 Done");
				break;
			case '6':
				boxNum = 6;
				Serial1.println("6 Done");
				break;
			case '7':
				boxNum = 7;
				Serial1.println("7 Done");
				break;
			case 'f':
				digitalWrite(S1Pin, HIGH);
				digitalWrite(S2Pin, HIGH);
				if (boxNum == 1) { box1(1); }
				if (boxNum == 2) { box2(1); }
				if (boxNum == 3) { box3(1); }
				if (boxNum == 4) { box4(1); }
				if (boxNum == 5) { box5(1); measureCapacitance(1); }
				if (boxNum == 6) { box6(); measureCapacitance(1); }
				if (boxNum == 7) { box7(1); measureCapacitance(1); }
				Serial1.println(">");
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				backwardOne();
				Serial1.println("f Done");
				break;
			case 'b':
				digitalWrite(S1Pin, HIGH);
				digitalWrite(S2Pin, HIGH);
				if (boxNum == 1) { box1(0); }
				if (boxNum == 2) { box2(0); }
				if (boxNum == 3) { box3(0); }
				if (boxNum == 4) { box4(0); }
				if (boxNum == 5) { box5(0); measureCapacitance(0); }
				if (boxNum == 6) { box6(); measureCapacitance(0); }
				if (boxNum == 7) { box7(0); measureCapacitance(0); }
				Serial1.println(">");
				digitalWrite(S1Pin, LOW);
				digitalWrite(S2Pin, LOW);
				backwardOne();
				Serial1.println("b Done");
				break;


			}
		}
	}
}

//Sensor test - print current values repeatedly (digital)
void printSensorVals()
{
	while (1)
	{
		readCurVals();
		Serial.print(MLCurVal);
		Serial.print("\t");
		Serial.print(ALCurVal);
		Serial.print("\t");
		Serial.print(FLCurVal);
		Serial.print("\t");
		Serial.print(FRCurVal);
		Serial.print("\t");
		Serial.print(ARCurVal);
		Serial.print("\t");
		Serial.print(MRCurVal);
		Serial.print("\t");
		Serial.println(" ");
		Serial.print("ReedVal = ");
		Serial.println(reedVal);
		delay(10 * loopTime);
	}
}

//Print current values once (digital)
void instantVals()
{
	readCurVals();
	Serial.print(MLCurVal);
	Serial.print("\t");
	Serial.print(ALCurVal);
	Serial.print("\t");
	Serial.print(FLCurVal);
	Serial.print("\t");
	Serial.print(FRCurVal);
	Serial.print("\t");
	Serial.print(ARCurVal);
	Serial.print("\t");
	Serial.print(MRCurVal);
	Serial.print("\t");
	Serial.println(" ");
}

//Print analog sensor values forever
void printAnalogVals()
{
	while (1)
	{
		readAnalogVals();
		Serial.print(MLCurVal);
		Serial.print("\t");
		Serial.print(ALCurVal);
		Serial.print("\t");
		Serial.print(FLCurVal);
		Serial.print("\t");
		Serial.print(FRCurVal);
		Serial.print("\t");
		Serial.print(ARCurVal);
		Serial.print("\t");
		Serial.print(MRCurVal);
		Serial.print("\t");
		Serial.println(" ");
		Serial.print("ReedVal = ");
		Serial.println(reedVal);
		delay(10 * loopTime);
	}
}

/*
Movement Instructions
*/

void forwardOne() //moves forward until either a boundary or a box is detected 
{
	int oneDone = 0;
	int bothDone = 0;
	reedVal = 0;
	int leftright = 0;
	//int left = 0;
	int go = 0;

	//startPositionCheck(); //Checks buggy is on intersection at start
	readStartVals();
	while (reedVal == 0)
	{

		motorsForward(leftMoveSpeed, rightMoveSpeed);
		curStateL = digitalRead(encoderPinL);
		curStateR = digitalRead(encoderPinR);

		if ((curStateL != lastStateL))
		{
			if (oneDone == 0) //Left done
			{
				motorsForward(0, rightMoveSpeed);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
				go = go + 1;
			}
		}
		if ((curStateR != lastStateR))
		{
			if (oneDone == 0) //Right done
			{
				motorsForward(leftMoveSpeed, 0);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
				go = go + 1;
				leftright = 0;
			}

		}


		lastStateL = curStateL;
		lastStateR = curStateR;
		//One optical encoder increment passed, correct any deviations
		readAnalogVals();
		if ((MLCurVal < 400) && (MLStartVal == 1))//sensors on middle of the buggy change, boundary reached - stop
		{
			motorsStop();
			break;
		}
		else if ((MLCurVal > 401) && (MLStartVal == 0)) //sensors on middle of the buggy change, boundary reached - stop
		{
			motorsStop();
			break;
		}
		if (go >= 2)
		{
			delay(1);//NB
			readAnalogVals();
			ARLow = (ARCurVal - 350);
			ARHigh = (ARCurVal + 100);
			ALLow = (ALCurVal - 350);
			ALHigh = (ALCurVal + 100);

			/*else*/ if (FRCurVal > ARHigh || FRCurVal < ARLow) //if front right is not equal to outer right, then must have drifted left     
			{

				delay(5);
				int adjustingright = 0;
				leftright = leftright + 1;
				if (leftright < 5)
				{
					while (adjustingright < 20)
					{
						motorsRotateRight(adjSpeed, adjSpeed); //Rotate right slightly
						delay(adjTime);
						adjustingright = adjustingright + 1;
					}
					motorsStop();
					delay(stopTime);
				}
				else {
					forwardSlightly();//leftright = 0;//do nothing
				}
			}
			else if (FLCurVal > ALHigh || FLCurVal < ALLow) //must have drifted right 
			{
				delay(5);
				int adjustingleft = 0;
				leftright = leftright + 1;
				if (leftright < 5)
				{
					while (adjustingleft < 20)
					{
						motorsRotateLeft(adjSpeed, adjSpeed); //Rotate left slightly
						delay(adjTime);
						adjustingleft = adjustingleft + 1;
					}
					motorsStop();
					delay(stopTime);
				}
				else {//must have had error at boundary
					forwardSlightly();//leftright = 0;//do nothing 
				}
			}
			else
			{
				leftright = 0;//do nothing
			}
			go = 0;
		}
	}
	oneDone = 0; //reset values
	bothDone = 0;
	motorsStop();
	previous = 0;
}

void forwardBox() //moves forward until either a boundary or a box is detected 
{
	int oneDone = 0;
	int bothDone = 0;
	reedVal = 0;
	int leftright = 0;
	int go = 0;

	readStartVals();
	while (reedVal == 0)
	{
		motorsForward(leftMoveSpeed, rightMoveSpeed);
		curStateL = digitalRead(encoderPinL);
		curStateR = digitalRead(encoderPinR);

		if ((curStateL != lastStateL))
		{
			if (oneDone == 0) //Left done
			{
				motorsForward(0, rightMoveSpeed);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
				go = go + 1;
			}
		}
		if ((curStateR != lastStateR))
		{
			if (oneDone == 0) //Right done
			{
				motorsForward(leftMoveSpeed, 0);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
				go = go + 1;
				leftright = 0;
			}
		}

		lastStateL = curStateL;
		lastStateR = curStateR;
		//One optical encoder increment passed, correct any deviations
		readAnalogVals();
		if ((MLCurVal < 400) && (MLStartVal == 1))//sensors on middle of the buggy change, boundary reached - stop
		{
			motorsStop();
			break;
		}
		else if ((MLCurVal > 401) && (MLStartVal == 0)) //sensors on middle of the buggy change, boundary reached - stop
		{
			motorsStop();
			break;
		}
		if (go>=1)
		{
			delay(1);//NB
			readAnalogVals();
			ARLow = (ARCurVal - 350);
			ARHigh = (ARCurVal + 100);
			ALLow = (ALCurVal - 350);
			ALHigh = (ALCurVal + 100);
			/*else*/ if (FRCurVal > ARHigh || FRCurVal < ARLow) //if front right is not equal to outer right, then must have drifted left     
			{
				delay(5);
				int adjustingright = 0;
				leftright = leftright + 1;
				if (leftright < 5)
				{
					while (adjustingright < 20)
					{
						motorsRotateRight(adjSpeed, adjSpeed); //Rotate right slightly
						delay(adjTime);
						adjustingright = adjustingright + 1;
					}
					motorsStop();
					delay(stopTime);
				}
				else {
					forwardSlightly();//leftright = 0;//do nothing
				}
			}
			else if (FLCurVal > ALHigh || FLCurVal < ALLow) //must have drifted right 
			{
				delay(5);
				int adjustingleft = 0;
				leftright = leftright + 1;
				if (leftright < 5)
				{
					while (adjustingleft < 20)
					{
						motorsRotateLeft(adjSpeed, adjSpeed); //Rotate left slightly
						delay(adjTime);
						adjustingleft = adjustingleft + 1;
					}
					motorsStop();
					delay(stopTime);
				}
				else {//must have had error at boundary
					forwardSlightly();//leftright = 0;//do nothing 
				}
			}
			else
			{
				leftright = 0;//do nothing
			}
			go = 0;
		}
	}
	oneDone = 0; //reset values
	bothDone = 0;
	motorsStop();
	previous = 0;
}


void backwardOne()
{
	int oneDone = 0;
	int bothDone = 0;
	reedVal = 0;
	readStartVals();
	while (1)
	{
		motorsBackwards(leftMoveSpeedBackward, rightMoveSpeedBackward);
		curStateL = digitalRead(encoderPinL);
		curStateR = digitalRead(encoderPinR);

		if ((curStateL != lastStateL))
		{
			if (oneDone == 0) //Left done
			{
				motorsBackwards(0, rightMoveSpeedBackward);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
			}
		}
		if ((curStateR != lastStateR))
		{
			if (oneDone == 0) //Right done
			{
				motorsBackwards(leftMoveSpeedBackward, 0);
				oneDone = 1;
			}
			else //Both done
			{
				motorsStop();
				delay(stopTime);
				bothDone = 1;
			}
		}
		lastStateL = curStateL;
		lastStateR = curStateR;
		//One optical encoder increment passed, correct any deviations
		if (bothDone == 1)
		{
			delay(1);//NB
			readAnalogVals();
			ARLow = (ARCurVal - 350);
			ARHigh = (ARCurVal + 100);
			ALLow = (ALCurVal - 350);
			ALHigh = (ALCurVal + 100);
			//boundary detected - apologies for confusing combination of analog/digital

			if ((MLCurVal < 400) && (MLStartVal == 1))//sensors on middle of the buggy change, boundary reached - stop
			{
				motorsStop();
				break;
			}
			else if ((MLCurVal > 401) && (MLStartVal == 0))
			{
				motorsStop();
				break;
			}
			else if ((FRCurVal > ARHigh || FRCurVal < ARLow) && (FLCurVal > ALHigh || FLCurVal < ALLow)) //protect from wobble error at boundary - just move forward NB problematic
			{
				//do nothing
			}
			else if (FRCurVal > ARHigh || FRCurVal < ARLow) //if front right is not equal to outer right, then must have drifted left     
			{
				delay(5);
				int adjustingright = 0;
				while (adjustingright < 20)
				{
					motorsRotateRight(adjSpeed, adjSpeed); //Rotate right slightly
					delay(adjTime);
					adjustingright = adjustingright + 1;
				}

				motorsStop();
				delay(stopTime);

			}
			else if (FLCurVal > ALHigh || FLCurVal < ALLow) //must have drifted right 
			{
				delay(5);
				int adjustingleft = 0;
				while (adjustingleft < 20)
				{
					motorsRotateLeft(adjSpeed, adjSpeed); //Rotate left slightly
					delay(adjTime);
					adjustingleft = adjustingleft + 1;
				}

				motorsStop();
				delay(stopTime);

			}
			else
			{
				//do nothing
			}
		}
	}
	oneDone = 0; //reset values
	bothDone = 0;
	motorsStop();
	previous = 1;
}

void rotateLeft90()

{
	int oneDone = 0;
	int bothDone = 0;
	readStartVals();
	while (1)
	{
		motorsRotateLeft(leftRotateSpeed, rightRotateSpeed);
		readCurVals();

		curStateL = digitalRead(encoderPinL);
		curStateR = digitalRead(encoderPinR);

		if ((curStateL != lastStateL))
		{
			if (oneDone == 0) //Left done
			{
				motorsForward(0, rightRotateSpeed);
				oneDone = 1;
			}
			else //Both done
			{
				bothDone = 1;
			}
		}
		if ((curStateR != lastStateR))
		{
			if (oneDone == 0) //Right done
			{
				motorsForward(leftRotateSpeed, 0);
				oneDone = 1;
			}
			else //Both done
			{
				bothDone = 1;
			}
		}

		lastStateL = curStateL;
		lastStateR = curStateR;

		//One optical encoder increment passed
		if (bothDone == 1)
		{
			//Reached boundary, stop
			if ((ALCurVal != ALStartVal) && (FLCurVal != FLStartVal))
			{
				motorsStop();
				delay(stopTime);
				readCurVals();

				//Overshot boundary, rotate back slightly
				while (ARCurVal != FRCurVal)//overshot left
				{
					motorsRotateRight(0.8 * leftRotateSpeed, 0.8 * rightRotateSpeed); //Rotate right slightly
					readCurVals();
					delay(adjTime);
				}
				motorsStop();
				break;
			}
			//Not reached boundary, continue rotating
			motorsStop();
			delay(stopTime);
			motorsRotateLeft(leftRotateSpeed, rightRotateSpeed);
			oneDone = 0;
			bothDone = 0;
		}
	}


}

void forwardSlightly()
{
	int forwardSlightly = 0;
	while (forwardSlightly < 50)
	{
		motorsForward(75, 67);
		delay(adjTime);
		forwardSlightly = forwardSlightly + 1;
	}

	motorsStop();
}

void rotateRight90()
{

	int oneDone = 0;
	int bothDone = 0;

	readStartVals();
	while (1)
	{
		motorsRotateRight(leftRotateSpeed, rightRotateSpeed);
		readCurVals();

		curStateL = digitalRead(encoderPinL);
		curStateR = digitalRead(encoderPinR);

		if ((curStateL != lastStateL))
		{
			if (oneDone == 0) //Left done
			{
				motorsForward(0, rightRotateSpeed);
				oneDone = 1;
			}
			else //Both done
			{
				bothDone = 1;
			}
		}
		if ((curStateR != lastStateR))
		{
			if (oneDone == 0) //Right done
			{
				motorsForward(leftRotateSpeed, 0);
				oneDone = 1;
			}
			else //Both done
			{
				bothDone = 1;
			}
		}

		lastStateL = curStateL;
		lastStateR = curStateR;

		//One optical encoder increment passed
		if (bothDone == 1)
		{
			//Reached boundary, stop
			if ((ARCurVal != ARStartVal) && (FRCurVal != FRStartVal))
			{
				motorsStop();
				delay(stopTime);
				readCurVals();

				//Overshot boundary, rotate back slightly
				while (ALCurVal != FLCurVal) //must have overshot right 
				{
					motorsRotateLeft(0.8 * leftRotateSpeed, 0.8 * rightRotateSpeed); //Rotate right slightly
					readCurVals();
					delay(adjTime);
				}
				motorsStop();
				break;
			}
			//Not reached boundary, continue rotating
			motorsStop();
			delay(stopTime);
			motorsRotateRight(leftRotateSpeed, rightRotateSpeed);
			oneDone = 0;
			bothDone = 0;
		}
	}

}

/*
Light Sensor Functions
*/

void readStartVals()
{
	FLStartVal = calculateColour(analogRead(FLPin));
	FRStartVal = calculateColour(analogRead(FRPin));
	MLStartVal = calculateColour(analogRead(MLPin));
	ALStartVal = calculateColour(analogRead(ALPin));
	ARStartVal = calculateColour(analogRead(ARPin));
}

void readCurVals()
{
	FLCurVal = calculateColourFront(analogRead(FLPin));
	FRCurVal = calculateColourFront(analogRead(FRPin));
	MLCurVal = calculateColour(analogRead(MLPin));
	ALCurVal = calculateColour(analogRead(ALPin));
	ARCurVal = calculateColour(analogRead(ARPin));
	reedVal = digitalRead(reedPin);
}

void readAnalogVals()
{
	FLCurVal = analogRead(FLPin);
	FRCurVal = analogRead(FRPin);
	MLCurVal = analogRead(MLPin);
	ALCurVal = analogRead(ALPin);
	ARCurVal = analogRead(ARPin);
	reedVal = digitalRead(reedPin);
}

int calculateColour(int sensorVal)
{
	if (sensorVal >= blackMin)
		return 1; //Black
	else if (sensorVal <= whiteMax)
		return 0; //White
	else
		return 2; //Failure
}

int calculateColourFront(int sensorVal)
{
	if (sensorVal >= blackMinFrontMiddle)
		return 1; //Black
	else if (sensorVal <= whiteMaxFrontMiddle)
		return 0; //White
	else
		return 2; //Failure
}



//Calculates whether front of buggy has passed boundary yet
void calculateBoundary()
{
	readCurVals();

	if ((ALCurVal == ALStartVal) && (ARCurVal != ARStartVal)) // left has not crossed and right has
	{
		{

			motorsRotateLeft(adjSpeed, adjSpeed); //Rotate left slightly
			readCurVals();

			while (ALCurVal == ALStartVal)
			{
				readCurVals();
				delay(adjTime);
			}
			motorsStop();
			delay(stopTime);
			passedBoundary = 1;
		}
	}
	else if ((ALCurVal != ALStartVal) && (ARCurVal == ARStartVal)) //left has crossed boundary and right has not
	{
		{
			motorsRotateRight(adjSpeed, adjSpeed); //Rotate right slightly
			readCurVals();
			while (ARCurVal == ARStartVal)
			{
				readCurVals();
				delay(adjTime);
			}
			motorsStop();
			delay(stopTime);
			passedBoundary = 1;
		}
	}

	else if ((ALCurVal != ALStartVal) && (ARCurVal != ARStartVal)) //Both FL and FR sensors are opposite to start
	{
		passedBoundary = 1;
	}
	else if ((ALCurVal == ALStartVal) && (ARCurVal == ARStartVal)) //FL and FR are same as start
	{
		passedBoundary = 0;
	}
}

/*
Motor Control Functions
*/
void motorsStop(void)                    //Stop
{
	digitalWrite(E1, LOW);
	digitalWrite(E2, LOW);
}

void motorsForward(char leftSpeed, char rightSpeed)         //Move forward
{
	analogWrite(E1, leftSpeed);     //PWM Speed Control
	digitalWrite(M1, HIGH);
	analogWrite(E2, rightSpeed);
	digitalWrite(M2, HIGH);
}

void motorsBackwards(char leftSpeed, char rightSpeed)         //Move backward
{
	analogWrite(E1, leftSpeed);
	digitalWrite(M1, LOW);
	analogWrite(E2, rightSpeed);
	digitalWrite(M2, LOW);
}

void motorsRotateLeft(char leftSpeed, char rightSpeed)            //Turn Left
{
	analogWrite(E1, leftSpeed);
	digitalWrite(M1, LOW);
	analogWrite(E2, rightSpeed);
	digitalWrite(M2, HIGH);
}

void motorsRotateRight(char leftSpeed, char rightSpeed)            //Turn Right
{
	analogWrite(E1, leftSpeed);
	digitalWrite(M1, HIGH);
	analogWrite(E2, rightSpeed);
	digitalWrite(M2, LOW);
}


//position 1 = front (knob), 0 = back

void box1(int position) {
	digitalWrite(switch5, HIGH); // so P2 measures across high impedance
	digitalWrite(switch1, HIGH);
	digitalWrite(switch2, LOW);
	digitalWrite(switch6, LOW);
	delay(100);
	digitalWrite(switch3, HIGH); // turns the boost converter on
	delay(1000);
	sensorValueP2 = analogRead(P2);
	array[0] = sensorValueP2 * (5.0 / 1023.0);
	digitalWrite(switch3, LOW); // turns the boost converter off
	Serial1.println(array[0]);
}

void box2(int position) {
	if (position == 1) {
		//Ra
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[0] = sensorValueP1 * (5.0 / 1023.0);

		//Rb
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueGnd = analogRead(Gnd);
		array[1] = sensorValueGnd * (5.0 / 1023.0);

	}
	else if (position == 0) {
		//Ra
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[0] = sensorValueP1 * (5.0 / 1023.0);
		//Rb
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[1] = sensorValueP1 * (5.0 / 1023.0);
	}
	Serial1.println(array[0]);
	Serial1.println(array[1]);
}



void box3(int position) {
	if (position == 1) {
		// Ra
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		sensorValueGnd = analogRead(Gnd);
		// measure the voltage across Rb and thus Ra + 1k
		array[1] = sensorValueGnd * (5.0 / 1023.0);
		// measure the voltage across Ra
		array[0] = sensorValueP1 * (5.0 / 1023.0);

		// Rb
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		sensorValueP2 = analogRead(P2);
		sensorValueGnd = analogRead(Gnd);
		// measure the voltage across Rb
		array[2] = sensorValueP2 * (5.0 / 1023.0);
		// measure the total voltage across Rb + Ra
		array[3] = sensorValueP1 * (5.0 / 1023.0);
	}
	else if (position == 0) {
		// Ra
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP2 = analogRead(P2);
		sensorValueP1 = analogRead(P1);
		// measure the voltage across Rb and thus Ra + 1k
		array[0] = sensorValueP1 * (5.0 / 1023.0);
		// measure the voltage across the 1k resistor 
		array[1] = sensorValueP2 * (5.0 / 1023.0);

		// Rb
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		sensorValueP2 = analogRead(P2);
		sensorValueGnd = analogRead(Gnd);
		// find voltage across Ra
		array[2] = sensorValueP1 * (5.0 / 1023.0);
		// find voltage across Ra + Rb
		array[3] = sensorValueGnd * (5.0 / 1023.0);
	}
	Serial1.println(array[0]);
	Serial1.println(array[1]);
	Serial1.println(array[2]);
	Serial1.println(array[3]);
}



void box4(int position) {
	if (position == 1) {
		// Ra
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		sensorValueP2 = analogRead(P2);
		array[0] = (sensorValueP1 * (5.0 / 1023.0)) - (sensorValueP2 * (5.0 / 1023.0));
		//array[0] = (sensorValueP1 * (5.0 / 1023.0));
		// Rb
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[1] = (sensorValueP1 * (5.0 / 1023.0));
	}
	else if (position == 0) {
		// Ra
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[0] = sensorValueP1 * (5.0 / 1023.0);
		// Rb
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		sensorValueP2 = analogRead(P2);
		array[1] = (sensorValueP1 * (5.0 / 1023.0)) - (sensorValueP2 * (5.0 / 1023.0));
	}
	Serial1.println(array[0]);
	Serial1.println(array[1]);
}

void box5(int position) {
	if (position == 1) {
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueGnd = analogRead(Gnd);
		array[0] = sensorValueGnd * (5.0 / 1023.0);
	}
	else if (position == 0) {
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[0] = sensorValueP1 * (5.0 / 1023.0);
	}
	Serial1.println(array[0]);
}

void box6() {
	digitalWrite(switch1, HIGH);
	digitalWrite(switch2, HIGH);
	delay(1000);
	sensorValueP1 = analogRead(P1);
	array[0] = sensorValueP1 * (5.0 / 1023.0);
	Serial1.println(array[0]);
}

void box7(int position) {
	if (position == 1) {
		digitalWrite(switch1, LOW);
		digitalWrite(switch2, HIGH);
		delay(1000);
		sensorValueGnd = analogRead(Gnd);
		array[0] = sensorValueGnd * (5.0 / 1023.0);
	}
	else if (position == 0) {
		digitalWrite(switch1, HIGH);
		digitalWrite(switch2, LOW);
		delay(1000);
		sensorValueP1 = analogRead(P1);
		array[0] = sensorValueP1 * (5.0 / 1023.0);
	}
	Serial1.println(array[0]);
}

void measureCapacitance(int position) {
	/*
	if (position == 1)
	{
		OUT_PIN = A4;
		IN_PIN = A3;
	}
	digitalWrite(switch1, LOW);
	digitalWrite(switch2, LOW);
	digitalWrite(switch3, HIGH);
	pinMode(IN_PIN, INPUT);
	digitalWrite(OUT_PIN, HIGH);
	int val = analogRead(IN_PIN);
	digitalWrite(OUT_PIN, LOW);

	if (val < 1000)
	{
		pinMode(IN_PIN, OUTPUT);

		float capacitance = (float)val * IN_CAP_TO_GND / (float)(MAX_ADC_VALUE - val);

		Serial.print(F("Capacitance Value = "));
		Serial.print(capacitance, 3);
		Serial.print(F(" pF ("));
		Serial.print(val);
		Serial.println(F(") "));
	}
	else
	{
		pinMode(IN_PIN, OUTPUT);
		delay(1);
		pinMode(OUT_PIN, INPUT_PULLUP);
		unsigned long u1 = micros();
		unsigned long t;
		int digVal;

		do
		{
			digVal = digitalRead(OUT_PIN);
			unsigned long u2 = micros();
			t = u2 > u1 ? u2 - u1 : u1 - u2;
		} while ((digVal < 1) && (t < 400000L));

		pinMode(OUT_PIN, INPUT);
		val = analogRead(OUT_PIN);
		digitalWrite(IN_PIN, HIGH);
		int dischargeTime = (int)(t / 1000L) * 5;
		delay(dischargeTime);
		pinMode(OUT_PIN, OUTPUT);
		digitalWrite(OUT_PIN, LOW);
		digitalWrite(IN_PIN, LOW);

		float capacitance = -(float)t / R_PULLUP
			/ log(1.0 - (float)val / (float)MAX_ADC_VALUE);

		Serial.print(F("Capacitance Value = "));
		if (capacitance > 1000.0)
		{
			Serial.println("0");
			//Serial.print(capacitance / 1000.0, 2);
			//Serial.print(F(" uF"));
		}
		else
		{

			array[1] = capacitance;
			Serial.print(array[1]);
			Serial.println(" nF");
			return;

		}

		;
	}
	while (millis() % 1000 != 0)
		;
		*/
}

