NAME MY_PROGRAM
DATA SEGMENT
DIVID DW 60H
MESS  DB 'INTERRUPT!',13,10,'$'
DATA  ENDS
STACK SEGMENT PARA STACK
      DB 100 DUP(?)
      STACK ENDS
CODE  SEGMENT
      ASSUME CS:CODE,DS:DATA,ES:DATA,SS:STACK
START:
     MOV AX,DATA
      MOV DS,AX
      MOV ES,AX


     MOV DX,3FBH
     MOV AL,80H
     OUT DX,AL
     MOV AX,DIVID
     MOV DX,3F8H
     OUT DX,AL
     MOV AL,AH
     MOV DX,3F9H
     OUT DX,AL
     MOV AL,0BH
     OUT DX,AL
     MOV AL,13H
     MOV DX,3FCH
     OUT DX,AL
     MOV AL,0
     MOV DX,3F9H
     OUT DX,AL
WAIT:
     MOV AH,1
     INT 16H
     MOV AH,0
     INT 16H
     MOV DX,3F8H
     OUT DX,AL
     MOV DX,3F8H
     IN AL,DX
     MOV AH,0EH
     INT 10H
	 CMP AL,20H
	 JNZ WAIT
     MOV AH,4CH
     INT 21H 
CODE  ENDS
END   START
     



   