100    	MOV   	SI，200 
103 	MOV 	CX，10 
106		MOV 	AL，0 
108 	MOV  	[SI ]，AL 
10A 	INC 	SI 
10B 	INC 	AL 
10D		DEC 	CX 
10E 	JNZ 	108 
110 	INT 	3
