import pylab as plt
import numpy as np
# initial values 
loop = 100 # number of interations
div = 1000 # divisions
# all possible values of c
c = np.linspace(-2,2,div)[:,np.newaxis] + 1j*np.linspace(-1.5,1.5,div)[np.newaxis,:]
print(c.shape)
# array of ones of same dimensions as c
ones = np.ones(c.shape, np.int32)
# Array that will hold colors for plot, initial value set here will be
# the color of the points in the mandelbrot set, i.e. where the series
# converges.
# For the code below to work, this initial value must at least be 'loop'.
# Here it is loop + 5
color = ones * loop + 5

cr = np.real(c).astype(np.float32)
ci = np.imag(c).astype(np.float32)
gpu_cr = cuda.mem_alloc(cr.nbytes)
gpu_ci = cuda.mem_alloc(ci.nbytes)

ones = np.ones(c.shape, np.int32)
color = (ones * loop + 5).astype(np.int32)

color_gpu = cuda.mem_alloc(color.nbytes)

cuda.memcpy_htod(gpu_cr, cr)
cuda.memcpy_htod(gpu_ci, ci)
cuda.memcpy_htod(color_gpu, color)

mod = SourceModule("""
__global__ void iter( int nx, int ny, int loop, float *cr, float *ci, int* color )
{
  int ind_x = threadIdx.x + blockIdx.x*blockDim.x;
  int ind_y = threadIdx.y + blockIdx.y*blockDim.y;
  if ( (ind_x < nx) && (ind_y < ny) )
  {
    int ind = ind_x + ind_y * nx;
    float zr = 0.f;
    float zi = 0.f;
    float icr = cr[ind];
    float ici = ci[ind];
    for (int iloop = 0; iloop < loop; iloop++)
    {
      float temp = zr*zr - zi*zi + icr;
      zi  = 2*zr*zi + ici;
      zr  = temp;
      if (zr*zr+zi*zi > 4)
      {
        color[ind] = iloop;
        break; 
      }
    }
  }
}
""")
func = mod.get_function("iter")
d_y = numpy.int32(c.shape[0])
d_x = numpy.int32(c.shape[1])
print(d_y, d_x)
loop32 = numpy.int32(loop)
block = (16,16,1)
grid  = ( (int(d_x)+15)//16, (int(d_y)+15)//16, 1)
func(d_x, d_y, loop32, gpu_cr, gpu_ci, color_gpu, block=block, grid=grid)

cuda.memcpy_dtoh(color, color_gpu)
plt.rcParams['figure.figsize'] = [12, 7.5]
# contour plot with real and imaginary parts of c as axes
# and colored according to 'color'
plt.contourf(c.real, c.imag, color)
plt.xlabel("Real($c$)")
plt.ylabel("Imag($c$)")
plt.xlim(-2,2)
plt.ylim(-1.5,1.5)
plt.savefig("plot.png")
plt.show()
