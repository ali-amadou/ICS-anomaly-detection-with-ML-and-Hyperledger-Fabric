import numpy as np
STATES=['Soumise','En_attente','Validee','Confirmee','Rejetee']
P=np.array([[0,.95,0,0,.05],[0,.05,.85,0,.10],[0,0,.05,.90,.05],[0,0,0,1,0],[0,0,0,0,1]],float)

def main():
    assert np.allclose(P.sum(1),1)
    Q=P[:3,:3]; R=P[:3,3:]
    N=np.linalg.inv(np.eye(3)-Q); B=N@R; t=N@np.ones(3)
    print('='*68); print('DTMC ABSORBANTE - TRANSACTION BLOCKCHAIN'); print('='*68)
    print('\nMatrice P :'); print(P)
    print('\nMatrice Q :'); print(Q)
    print('\nMatrice R :'); print(R)
    print('\nMatrice fondamentale N=(I-Q)^-1 :'); print(N)
    print('\nPROBABILITES D ABSORPTION')
    for i,s in enumerate(STATES[:3]): print(f'{s:<12} -> Confirmee : {B[i,0]*100:6.2f} % | Rejetee : {B[i,1]*100:6.2f} %')
    print('\nNOMBRE MOYEN D ETAPES')
    for s,x in zip(STATES[:3],t): print(f'{s:<12} : {x:.3f}')
    print('\nEtat initial = Soumise')
    print(f'Confirmation : {B[0,0]*100:.2f} %')
    print(f'Rejet        : {B[0,1]*100:.2f} %')
    print(f'Etapes moy.  : {t[0]:.3f}')
    print('\nSommes des probabilites :', [round(x.sum(),6) for x in B])
    print('='*68)
if __name__=='__main__': main()
