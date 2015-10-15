template <class T, unsigned int blockSize>
__global__ void
FUNC(reduce5)(T *g_idata, T *g_odata, unsigned int n)
{
    SharedMemory<T> smem;
    T *sdata = smem.getPointer();

    // perform first level of reduction,
    // reading from global memory, writing to shared memory
    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x*(blockSize*2) + threadIdx.x;
    unsigned int j = blockIdx.x*(blockSize*2) + threadIdx.x, k = threadIdx.x;
  int index_e = cols * BLOCK_SIZE * by + BLOCK_SIZE * bx + cols * ty + BLOCK_SIZE;

    sdata[tid] = (i < n) ? g_idata[i] : 0;
    if (i + blockSize < n) 
        sdata[tid] += g_idata[i+blockSize];  

}


