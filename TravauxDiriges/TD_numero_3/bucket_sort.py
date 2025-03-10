import numpy as np
from mpi4py import MPI
import time
N = 65_536

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank

filename = f"Output{rank:03d}.txt"
out      = open(filename, mode='w')

reste = N%nbp
NLoc  = N//nbp + (1 if rank < reste else 0)
#values = np.random.randint(-32768, 32768, size=NLoc,dtype=np.int64)
values = np.random.normal(size=NLoc)
out.write(f"Valeurs initiales : {values}\n")

values.sort()

# Prends les nbp+1 quantils du tableau trié :
quantils = np.quantile(values, np.linspace(0, 1, nbp+1))
print(f"Quantils : {quantils}")

glob_quantil = np.empty(nbp*(nbp+1), dtype=np.double)
globCom.Allgather(quantils, glob_quantil)
glob_quantil.sort()
print(f"Quantils globaux : {glob_quantil}")
quantils = np.quantile(glob_quantil, np.linspace(0, 1, nbp+1))
print(f"Quantils finaux : {quantils}")

local_buckets = [ 
    values[(values >= quantils[i])& (values < quantils[i+1])] for i in range(nbp)]

bucket_lst = globCom.alltoall(local_buckets)
bucket = np.concatenate(bucket_lst)
bucket.sort(kind='mergesort')

# Vérification
print("bucket is sorted:", np.all(bucket[:-1] <= bucket[1:]))
print(f"{rank} : bucket = {bucket[0]}...{bucket[-1]}")
print(f"{rank} : bucket shape = {bucket.shape}")