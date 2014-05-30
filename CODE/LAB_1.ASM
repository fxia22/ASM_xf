NAME    	MY_PROGRAM       	
DATA	 	SEGMENT   			
BUFFER1	DB 		0,1,2,3,4,5,6,7,8,9 
 				DB		0AH,0BH,0CH,0DH,0EH,0FH 
BUFFER2	DB	 	10H DUP(0) 
MESS		DB		'HAVE DONE',13,10,'$'
DATA	 	ENDS          			
STACK	 	SEGMENT 	PARA STACK 
 				DB 		100	 DUP(?) 
STACK 		ENDS 					
CODE 		SEGMENT 				
ASSUME 	CS:CODE,DS:DATA,ES:DATA,SS:STACK 

START: 	MOV 	AX,DATA 	
 				MOV	DS,AX 		
 				MOV 	ES,AX 
 				LEA 	SI,BUFFER1 
 				LEA 	DI,BUFFER2 
MOV 	CX,10H 
NEXT: 	MOV 	AL, [SI ] 
 				MOV  	[DI ],AL 
 				INC 	SI 
 				INC 	DI 
 				DEC 	CX 
 				JNZ 	NEXT 
 				LEA 	DX,MESS 		
 				MOV 	AH,9 			
 				INT 	21H 			
 				MOV 	AH,4CH 		
 				INT 	21H 			
CODE		ENDS 					
END 		START 				
