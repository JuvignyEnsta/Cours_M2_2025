from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank 
nbp  = comm.size

if nbp == 2:
    jeton : int = 42
    if rank == 0:
        comm.send(jeton, dest=1)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 1")
    else:
        jeton = comm.recv(source=0)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 0")   
elif nbp == 4: # Hypercube dimension 2
    jeton : int = 42
    if rank == 0:
        comm.send(jeton, dest=1)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 1")
        comm.send(jeton, dest=2)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 2")
    elif rank == 1:
        jeton = comm.recv(source=0)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 0")
        comm.send(jeton, dest=3)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 3")
    elif rank == 2:
        jeton = comm.recv(source=0)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 0")
    else: # rank == 3
        jeton = comm.recv(source=1)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 1")
elif nbp == 8: # Hypercube de dimension 3
    jeton : int = 42
    if rank == 0:
        comm.send(jeton, dest=1)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 1")
        comm.send(jeton, dest=2)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 2")
        comm.send(jeton, dest=4)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 4")
    elif rank == 1:
        jeton = comm.recv(source=0)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 0")
        comm.send(jeton, dest=3)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 3")
        comm.send(jeton, dest=5)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 5")
    elif rank == 2:
        jeton = comm.recv(source=0)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 0")
        comm.send(jeton, dest=6)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 6")
    elif rank == 3:
        jeton = comm.recv(source=1)
        print(f"Processus {rank} recoit le jeton {jeton} du processus 1")
        comm.send(jeton, dest=7)
        print(f"Processus {rank} envoie le jeton {jeton} au processus 7")
    else:
        jeton = comm.recv(source=rank-4)
        print(f"Processus {rank} recoit le jeton {jeton} du processus {rank-4}")
else:
    from math import log2
    dim = int(log2(nbp)+0.1)
    jeton : int = 42
    for d in range(dim):
        if rank < 2**d: 
            comm.send(jeton, dest=rank+2**d)
            print(f"Processus {rank} envoie le jeton {jeton} au processus {rank+2**d}")
        elif rank < 2**(d+1):
            jeton = comm.recv(source=rank-2**d)
            print(f"Processus {rank} recoit le jeton {jeton} du processus {rank-2**d}")
print(f"Fin du processus {rank}")