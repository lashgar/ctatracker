__global__
void kernel(float* dA, float* dB, float* dC, int dim)
{
    unsigned int idx = threadIdx.x + blockIdx.x*blockDim.x;
    unsigned int idy = threadIdx.y + blockIdx.y*blockDim.y;
    if(idx<dim && idy<dim)
        dC[idx+idy*dim]=dA[idx+idy*dim]+dB[idx+idy*dim];
}
