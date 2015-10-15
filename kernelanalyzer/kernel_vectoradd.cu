__global__ void
Kernel( float *a, float *b, float *c)
{
    int l = a[tid];
	int tid = blockIdx.x*MAX_THREADS_PER_BLOCK + threadIdx.x;
    a[tid] = b[tid] + c[tid];
}
