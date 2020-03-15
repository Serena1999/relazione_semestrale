EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R1
U 1 1 5E2FB6F4
P 6500 1950
F 0 "R1" H 6570 1996 50  0000 L CNN
F 1 "0.22-220k" H 6570 1905 50  0000 L CNN
F 2 "" V 6430 1950 50  0001 C CNN
F 3 "~" H 6500 1950 50  0001 C CNN
	1    6500 1950
	1    0    0    -1  
$EndComp
Text GLabel 7400 1100 1    50   Input ~ 0
T1
Wire Wire Line
	7200 1900 7200 2000
Wire Wire Line
	7650 1900 7650 1950
Connection ~ 7650 1900
Wire Wire Line
	7600 1900 7650 1900
Wire Wire Line
	7650 1850 7650 1900
$Comp
L power:GND #PWR?
U 1 1 5E305DF8
P 7200 2000
F 0 "#PWR?" H 7200 1750 50  0001 C CNN
F 1 "GND" H 7205 1827 50  0000 C CNN
F 2 "" H 7200 2000 50  0001 C CNN
F 3 "" H 7200 2000 50  0001 C CNN
	1    7200 2000
	1    0    0    -1  
$EndComp
$Comp
L Transistor_BJT:TIP41 Q2
U 1 1 5E301623
P 7400 1800
F 0 "Q2" H 7591 1846 50  0000 L CNN
F 1 "BC547B" H 7591 1800 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 7650 1725 50  0001 L CIN
F 3 "https://www.centralsemi.com/get_document.php?cmp=1&mergetype=pd&mergepath=pd&pdf_id=tip41.PDF" H 7400 1800 50  0001 L CNN
	1    7400 1800
	0    1    1    0   
$EndComp
$Comp
L Transistor_FET:IRF6617 Q1
U 1 1 5E2FF19F
P 7650 2150
F 0 "Q1" H 7854 2196 50  0000 L CNN
F 1 "IRFZ44N" H 7854 2105 50  0000 L CNN
F 2 "Package_DirectFET:DirectFET_ST" H 7650 2150 50  0001 C CIN
F 3 "https://www.infineon.com/dgdl/irf6617pbf.pdf?fileId=5546d462533600a4015355e853f21a17" H 7650 2150 50  0001 L CNN
	1    7650 2150
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5E3155A4
P 7650 1700
F 0 "R2" H 7720 1746 50  0000 L CNN
F 1 "1k" H 7720 1655 50  0000 L CNN
F 2 "" V 7580 1700 50  0001 C CNN
F 3 "~" H 7650 1700 50  0001 C CNN
	1    7650 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 1200 7400 1100
Wire Wire Line
	7400 1500 7400 1600
$Comp
L Device:R R3
U 1 1 5E3066C0
P 7400 1350
F 0 "R3" V 7193 1350 50  0000 C CNN
F 1 "1k" V 7284 1350 50  0000 C CNN
F 2 "" V 7330 1350 50  0001 C CNN
F 3 "~" H 7400 1350 50  0001 C CNN
	1    7400 1350
	1    0    0    -1  
$EndComp
$Comp
L Transistor_BJT:TIP42 Q4
U 1 1 5E335CC9
P 9850 1650
F 0 "Q4" H 10041 1696 50  0000 L CNN
F 1 "TIP32C" H 10041 1605 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 10100 1575 50  0001 L CIN
F 3 "https://www.centralsemi.com/get_document.php?cmp=1&mergetype=pd&mergepath=pd&pdf_id=TIP42.PDF" H 9850 1650 50  0001 L CNN
	1    9850 1650
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R4
U 1 1 5E33BCC7
P 9850 2100
F 0 "R4" H 9920 2146 50  0000 L CNN
F 1 "1k" H 9920 2055 50  0000 L CNN
F 2 "" V 9780 2100 50  0001 C CNN
F 3 "~" H 9850 2100 50  0001 C CNN
	1    9850 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9850 1950 9850 1850
$Comp
L Device:R R5
U 1 1 5E33E725
P 10300 2550
F 0 "R5" V 10507 2550 50  0000 C CNN
F 1 "1k" V 10416 2550 50  0000 C CNN
F 2 "" V 10230 2550 50  0001 C CNN
F 3 "~" H 10300 2550 50  0001 C CNN
	1    10300 2550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9850 2250 9850 2350
$Comp
L power:GND #PWR?
U 1 1 5E33FCAE
P 9850 2850
F 0 "#PWR?" H 9850 2600 50  0001 C CNN
F 1 "GND" H 9855 2677 50  0000 C CNN
F 2 "" H 9850 2850 50  0001 C CNN
F 3 "" H 9850 2850 50  0001 C CNN
	1    9850 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	9850 2750 9850 2850
Wire Wire Line
	10050 1550 10250 1550
Text GLabel 10550 2550 2    50   Input ~ 0
T2
$Comp
L Device:R R6
U 1 1 5E3476B9
P 9450 1550
F 0 "R6" V 9243 1550 50  0000 C CNN
F 1 "4.7k" V 9334 1550 50  0000 C CNN
F 2 "" V 9380 1550 50  0001 C CNN
F 3 "~" H 9450 1550 50  0001 C CNN
	1    9450 1550
	0    1    1    0   
$EndComp
Wire Notes Line
	9000 1150 10500 1150
Wire Notes Line
	10500 1150 10500 3100
Wire Notes Line
	10500 3100 9000 3100
Wire Notes Line
	9000 3100 9000 1150
Wire Notes Line
	7950 1150 7050 1150
Wire Notes Line
	7050 1150 7050 2750
Wire Notes Line
	7050 2750 7950 2750
Wire Notes Line
	7950 2750 7950 1150
Text Notes 7200 2850 0    50   ~ 0
circuito switch\n
Text Notes 9250 1100 0    50   ~ 0
circuito di carica / scarica
Wire Wire Line
	8450 1550 8450 1900
Wire Wire Line
	8450 1550 8050 1550
Wire Wire Line
	8050 1550 8050 2250
Wire Wire Line
	8050 2250 7850 2250
Connection ~ 8450 1550
Wire Wire Line
	8450 2200 8450 2900
$Comp
L power:GND #PWR?
U 1 1 5E351772
P 8450 2900
F 0 "#PWR?" H 8450 2650 50  0001 C CNN
F 1 "GND" H 8455 2727 50  0000 C CNN
F 2 "" H 8450 2900 50  0001 C CNN
F 3 "" H 8450 2900 50  0001 C CNN
	1    8450 2900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5E2F41B6
P 6500 2900
F 0 "#PWR?" H 6500 2650 50  0001 C CNN
F 1 "GND" H 6505 2727 50  0000 C CNN
F 2 "" H 6500 2900 50  0001 C CNN
F 3 "" H 6500 2900 50  0001 C CNN
	1    6500 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 2900 6500 2700
$Comp
L Diode:1N4007 D1
U 1 1 5E2F497A
P 6500 2450
F 0 "D1" V 6546 2371 50  0000 R CNN
F 1 "1N4007" V 6455 2371 50  0000 R CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 6500 2275 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88503/1n4001.pdf" H 6500 2450 50  0001 C CNN
	1    6500 2450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7450 2250 7000 2250
Wire Wire Line
	7000 2250 7000 1550
Wire Wire Line
	7000 1550 6500 1550
Text GLabel 6200 1700 0    50   Input ~ 0
OUT2
Wire Wire Line
	6200 1700 6500 1700
Wire Wire Line
	6500 1550 6500 1700
Wire Wire Line
	6500 1700 6500 1800
Connection ~ 6500 1700
Text GLabel 6200 2200 0    50   Input ~ 0
OUT1
Wire Wire Line
	6200 2200 6500 2200
Wire Wire Line
	6500 2100 6500 2200
Connection ~ 6500 2200
Wire Wire Line
	6500 2200 6500 2300
$Comp
L Transistor_BJT:TIP41 Q5
U 1 1 5E387BA0
P 9350 2300
F 0 "Q5" H 9541 2346 50  0000 L CNN
F 1 "TIP31C" H 9541 2300 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 9600 2225 50  0001 L CIN
F 3 "https://www.centralsemi.com/get_document.php?cmp=1&mergetype=pd&mergepath=pd&pdf_id=tip41.PDF" H 9350 2300 50  0001 L CNN
	1    9350 2300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5E39095A
P 9450 2600
F 0 "#PWR?" H 9450 2350 50  0001 C CNN
F 1 "GND" H 9455 2427 50  0000 C CNN
F 2 "" H 9450 2600 50  0001 C CNN
F 3 "" H 9450 2600 50  0001 C CNN
	1    9450 2600
	1    0    0    -1  
$EndComp
Text GLabel 8950 2600 0    50   Input ~ 0
T3
Wire Notes Line
	5700 800  10950 800 
Wire Notes Line
	10950 800  10950 3300
Wire Notes Line
	10950 3300 5700 3300
Wire Notes Line
	5700 3300 5700 800 
Text Notes 7900 750  0    50   ~ 0
circuito gestione diodo
Wire Wire Line
	10550 2550 10450 2550
Wire Wire Line
	9600 1550 9650 1550
Wire Wire Line
	9450 2500 9450 2600
Wire Wire Line
	9450 2050 9450 2100
Text GLabel 5050 2200 2    50   Input ~ 0
OUT1
Text GLabel 8450 1350 1    50   Input ~ 0
OUT3
Wire Wire Line
	8450 1350 8450 1550
Text GLabel 5050 1600 2    50   Input ~ 0
OUT3
$Comp
L Transistor_BJT:TIP41 Q3
U 1 1 5E333C7F
P 9950 2550
F 0 "Q3" H 10141 2596 50  0000 L CNN
F 1 "BC547B" H 10141 2550 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 10200 2475 50  0001 L CIN
F 3 "https://www.centralsemi.com/get_document.php?cmp=1&mergetype=pd&mergepath=pd&pdf_id=tip41.PDF" H 9950 2550 50  0001 L CNN
	1    9950 2550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8450 1550 9150 1550
Wire Wire Line
	9450 1750 9150 1750
Wire Wire Line
	9150 1750 9150 1550
Connection ~ 9150 1550
Wire Wire Line
	9150 1550 9300 1550
$Comp
L Device:R R9
U 1 1 5E3D9FFF
P 9150 2450
F 0 "R9" H 9220 2496 50  0000 L CNN
F 1 "1k" H 9220 2405 50  0000 L CNN
F 2 "" V 9080 2450 50  0001 C CNN
F 3 "~" H 9150 2450 50  0001 C CNN
	1    9150 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	9150 2600 8950 2600
$Comp
L Device:R R7
U 1 1 5E3A0871
P 9450 1900
F 0 "R7" V 9243 1900 50  0000 C CNN
F 1 "1k" V 9334 1900 50  0000 C CNN
F 2 "" V 9380 1900 50  0001 C CNN
F 3 "~" H 9450 1900 50  0001 C CNN
	1    9450 1900
	-1   0    0    1   
$EndComp
$Comp
L Device:CP C1
U 1 1 5E3DE4FF
P 8450 2050
F 0 "C1" H 8568 2096 50  0000 L CNN
F 1 "10000u" H 8568 2005 50  0000 L CNN
F 2 "" H 8488 1900 50  0001 C CNN
F 3 "~" H 8450 2050 50  0001 C CNN
	1    8450 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 1600 5050 1600
$Comp
L Device:R R?
U 1 1 5E334245
P 4550 1600
F 0 "R?" H 4620 1646 50  0001 L CNN
F 1 "10k" V 4435 1600 50  0000 C CNN
F 2 "" V 4480 1600 50  0001 C CNN
F 3 "~" H 4550 1600 50  0001 C CNN
	1    4550 1600
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5E3389C1
P 4400 1600
F 0 "#PWR?" H 4400 1350 50  0001 C CNN
F 1 "GND" H 4405 1427 50  0000 C CNN
F 2 "" H 4400 1600 50  0001 C CNN
F 3 "" H 4400 1600 50  0001 C CNN
	1    4400 1600
	0    1    1    0   
$EndComp
Text GLabel 3500 1600 0    50   Input ~ 0
A0
Text GLabel 5050 1950 2    50   Input ~ 0
OUT2
$Comp
L Device:R R?
U 1 1 5E330956
P 4850 1600
F 0 "R?" H 4920 1646 50  0001 L CNN
F 1 "100k" V 4735 1600 50  0000 C CNN
F 2 "" V 4780 1600 50  0001 C CNN
F 3 "~" H 4850 1600 50  0001 C CNN
	1    4850 1600
	0    1    1    0   
$EndComp
Wire Wire Line
	4700 1600 4700 1450
Wire Wire Line
	4700 1450 4150 1450
Wire Wire Line
	4150 1450 4150 1600
Wire Wire Line
	4150 1600 3500 1600
Connection ~ 4700 1600
Text GLabel 3500 1950 0    50   Input ~ 0
A12
Text GLabel 3500 2300 0    50   Input ~ 0
A10
Wire Notes Line
	3200 1250 5500 1250
Wire Notes Line
	5500 1250 5500 2600
Wire Notes Line
	5500 2600 3200 2600
Wire Notes Line
	3200 2600 3200 1250
Text Notes 4050 1200 0    50   ~ 0
circuito lettura
$Comp
L Device:CP C2
U 1 1 5E3DEF4B
P 9200 4250
F 0 "C2" H 9318 4296 50  0000 L CNN
F 1 "100u" H 9318 4205 50  0000 L CNN
F 2 "" H 9238 4100 50  0001 C CNN
F 3 "~" H 9200 4250 50  0001 C CNN
	1    9200 4250
	1    0    0    -1  
$EndComp
Text Notes 8150 3550 0    50   ~ 0
circuito facile
Wire Notes Line
	7100 4900 7100 3600
Wire Notes Line
	9700 4900 7100 4900
Wire Notes Line
	9700 3600 9700 4900
Wire Notes Line
	7100 3600 9700 3600
Connection ~ 8050 3850
Wire Wire Line
	7350 3850 8050 3850
Connection ~ 7350 4250
Wire Wire Line
	8050 4250 8050 4150
Connection ~ 8050 4250
Wire Wire Line
	7350 4250 8050 4250
Connection ~ 8050 4650
Wire Wire Line
	7350 4650 8050 4650
$Comp
L Device:Oscilloscope MES_X
U 1 1 5E37AC84
P 7350 4450
F 0 "MES_X" H 7220 4404 50  0000 R CNN
F 1 "Oscilloscope" H 7220 4495 50  0000 R CNN
F 2 "" V 7350 4550 50  0001 C CNN
F 3 "~" V 7350 4550 50  0001 C CNN
	1    7350 4450
	-1   0    0    1   
$EndComp
$Comp
L Device:Oscilloscope MES_Y
U 1 1 5E378AF4
P 7350 4050
F 0 "MES_Y" H 7480 4096 50  0000 L CNN
F 1 "Oscilloscope" H 7480 4005 50  0000 L CNN
F 2 "" V 7350 4150 50  0001 C CNN
F 3 "~" V 7350 4150 50  0001 C CNN
	1    7350 4050
	1    0    0    -1  
$EndComp
Connection ~ 9200 4650
Wire Wire Line
	8050 4650 9200 4650
Wire Wire Line
	9200 3850 9200 4100
Wire Wire Line
	9000 3850 9200 3850
Wire Wire Line
	8050 3850 8400 3850
Wire Wire Line
	8050 4350 8050 4250
$Comp
L Switch:SW_DIP_x01 SW1
U 1 1 5E3713C1
P 8700 3850
F 0 "SW1" H 8700 4025 50  0000 C CNN
F 1 "SW_DIP_x01" H 8700 4026 50  0001 C CNN
F 2 "" H 8700 3850 50  0001 C CNN
F 3 "~" H 8700 3850 50  0001 C CNN
	1    8700 3850
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 5E370938
P 8050 4000
F 0 "R8" H 8120 4046 50  0000 L CNN
F 1 "0.22" H 8120 3955 50  0000 L CNN
F 2 "" V 7980 4000 50  0001 C CNN
F 3 "~" H 8050 4000 50  0001 C CNN
	1    8050 4000
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N4007 D2
U 1 1 5E36F30A
P 8050 4500
F 0 "D2" V 8096 4421 50  0000 R CNN
F 1 "1N4007" V 8005 4421 50  0000 R CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 8050 4325 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88503/1n4001.pdf" H 8050 4500 50  0001 C CNN
	1    8050 4500
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9200 4400 9200 4650
$Comp
L power:GND #PWR?
U 1 1 5E36E5E9
P 9200 4650
F 0 "#PWR?" H 9200 4400 50  0001 C CNN
F 1 "GND" H 9205 4477 50  0000 C CNN
F 2 "" H 9200 4650 50  0001 C CNN
F 3 "" H 9200 4650 50  0001 C CNN
	1    9200 4650
	1    0    0    -1  
$EndComp
Text GLabel 6200 2700 0    50   Input ~ 0
OUT0
Wire Wire Line
	6200 2700 6500 2700
Connection ~ 6500 2700
Wire Wire Line
	6500 2700 6500 2600
Text GLabel 3500 2100 0    50   Input ~ 0
A13
Text GLabel 3500 2450 0    50   Input ~ 0
A11
Text GLabel 5050 2450 2    50   Input ~ 0
OUT0
Wire Wire Line
	3500 1950 5050 1950
Wire Wire Line
	3500 2450 5050 2450
Wire Wire Line
	3500 2300 4750 2300
Wire Wire Line
	4750 2300 4850 2200
Wire Wire Line
	4850 2200 5050 2200
Connection ~ 4850 2200
Wire Wire Line
	3500 2100 4750 2100
Wire Wire Line
	4750 2100 4850 2200
$Comp
L power:VCC #PWR?
U 1 1 5E577E93
P 10250 1550
F 0 "#PWR?" H 10250 1400 50  0001 C CNN
F 1 "VCC" H 10267 1723 50  0000 C CNN
F 2 "" H 10250 1550 50  0001 C CNN
F 3 "" H 10250 1550 50  0001 C CNN
	1    10250 1550
	0    1    1    0   
$EndComp
$Comp
L power:VCC #PWR?
U 1 1 5E57EFD6
P 7650 1400
F 0 "#PWR?" H 7650 1250 50  0001 C CNN
F 1 "VCC" H 7667 1573 50  0000 C CNN
F 2 "" H 7650 1400 50  0001 C CNN
F 3 "" H 7650 1400 50  0001 C CNN
	1    7650 1400
	1    0    0    -1  
$EndComp
Wire Wire Line
	7650 1400 7650 1550
$EndSCHEMATC
