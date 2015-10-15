__global__ void fwtBatch2Kernel(
    float *d_Output,
    float *d_Input,
    int stride){
    const int pos = blockIdx.x * blockDim.x + threadIdx.x;
    const int   N = blockDim.x *  gridDim.x * 4;
    const int offset=blockIdx.y * N;

    //float *d_Src = d_Input  + blockIdx.y * N;
    //float *d_Dst = d_Output + blockIdx.y * N;

    int lo = pos & (stride - 1);
    int i0 = ((pos - lo) << 2) + lo;
    int i1 = i0 + stride;
    int i2 = i1 + stride;
    int i3 = i2 + stride;

    float D0 = d_Input[offset+i0];
    float D1 = d_Input[offset+i1];
    float D2 = d_Input[offset+i2];
    float D3 = d_Input[offset+i3];

    float T;
    T = D0; D0        = D0 + D2; D2        = T - D2;
    T = D1; D1        = D1 + D3; D3        = T - D3;
    T = D0; d_Output[offset+i0] = D0 + D1; d_output[offset+i1] = T - D1;
    T = D2; d_Output[offset+i2] = D2 + D3; d_output[offset+i3] = T - D3;
}
