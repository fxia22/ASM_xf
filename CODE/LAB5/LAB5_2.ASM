DATA SEGMENT
DIVID DW 60H
DATA ENDS
STACK1 SEGMENT PARA STACK
       DB 100 DUP(?)
STACK1 ENDS
CODE SEGMENT
     ASSUME CS:CODE,DS:DATA,ES:DATA,SS:STACK1
SUB1 PROC FAR
START:
		MOV AX,DATA
      	MOV DS,AX
      	MOV AL,80H
     	MOV DX,3FBH
      	OUT DX,AL
      	MOV AX,DIVID
      	MOV DX,3F8H
      	OUT DX,AL
      	MOV AL,AH
      	MOV DX,3F9H
      	OUT DX,AL
      	MOV AL,0BH
      	OUT DX,AL
      	MOV AL,03H ; MODEM
      	MOV DX,3FCH
      	OUT DX,AL
      	MOV AL,0
      	MOV DX,3F9H
      	OUT DX,AL

WAIT_FOR:
      	MOV AH,1
      	INT 16H
      	MOV AH,0
      	INT 16H
      	MOV DX,3F8H
      	OUT DX,AL
      	CMP AL,20H
		JZ  QUIT
		JMP WAIT_FOR
		
RECEIVE:
      	MOV DX,3F8H
      	IN  AL,DX
      	AND AL,7FH
		MOV 	AH,0EH
		INT 	10H
      	CMP AL,20H
      	JNZ WAIT_FOR
      	MOV AH,4CH
      	INT 21H		

SUB1	ENDP
	CODE	ENDS
	END	START
