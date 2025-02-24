N=input
G=b'\x00'
A=print
from cryptolib import aes
def D(w,p):return w+p*((16-len(w)%16)%16)
H,Q=7,32
R=b'bkjask\xd1jddye\x03987rjh\x08da\xfawdkj3e\x0aencwdj\x23hwqwek\xf1lDDJW\x98QEQ122'

I=D(R[H:H+Q],b'\xaa'); J=aes(I,1); S=aes(I,1)

U=N('\r\nuid: ');V=N('pwd: ');W=f">>{U}||{V}<<".encode();M=J.encrypt(D(W,G))
A(f'K={M}')
