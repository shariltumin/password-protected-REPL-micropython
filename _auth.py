N=input
G=b'\x00'
F=SystemExit
C='Authentication failed'
B='auth'
A=print
from time import sleep as Z
from machine import Pin as X
from os import stat as O,remove as P
from cryptolib import aes
def D(w,p):return w+p*((16-len(w)%16)%16)
H,Q=7,32
R=b'bkjask\xd1jddye\x03987rjh\x08da\xfawdkj3e\x0aencwdj\x23hwqwek\xf1lDDJW\x98QEQ122'
I=D(R[H:H+Q],b'\xaa')
J=aes(I,1)
S=aes(I,1)
K=b'yl\xdc\x9d\\Z\xd6\x89\xdb\xff\x93\xe9vF\xd4U'
try:
	X=O(B)
	with open(B,'rb')as E:T=E.read()
	if S.decrypt(T).rstrip(G)!=K:P(B);A('Authentication data failed');raise F(C)
except:
	L=0
	while L<3:
		try:
			U=N('\r\nuid: ');V=N('pwd: ');W=f">>{U}||{V}<<".encode();M=J.encrypt(D(W,G))
			if M==K:
				with open(B,'wb')as E:E.write(J.encrypt(D(M,G)))
				A('Authenticated!!');break
			else:A('Wrong ID and/or PWD');L+=1
		except:A('Authentication failed due to error');raise F(C)
	else:A(C);raise F(C)
finally:
   try:
      c=0;x = X(23, X.IN, X.PULL_UP)
      while x.value():
         if c>5: raise F(C)
         c+=1;Z(1)
   except: raise F(C)
