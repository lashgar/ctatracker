////////////////////////////////////////////////////////////////////////////////
// GPU-specific common definitions
////////////////////////////////////////////////////////////////////////////////
//Data type used for input data fetches
/*
typedef uint4 data_t;

//Both map to single instructions on G8x / G9x / G10x
#define UMUL(a, b)      __umul24( (a), (b) )
#define UMAD(a, b, c) ( UMUL((a), (b)) + (c) )

//May change on future hardware, so better parametrize the code
#define SHARED_MEMORY_BANKS 16

//Threadblock size: must be a multiple of (4 * SHARED_MEMORY_BANKS)
//because of the bit permutation of threadIdx.x
#define HISTOGRAM64_THREADBLOCK_SIZE (4 * SHARED_MEMORY_BANKS)

*/

////////////////////////////////////////////////////////////////////////////////
// Merge histogram64() output
// Run one threadblock per bin; each threadbock adds up the same bin counter 
// from every partial histogram. Reads are uncoalesced, but mergeHistogram64
// takes only a fraction of total processing time
////////////////////////////////////////////////////////////////////////////////
#define MERGE_THREADBLOCK_SIZE 256

__global__ void mergeHistogram64Kernel(
    uint *d_Histogram,
    uint *d_PartialHistograms,
    uint histogramCount
){
    __shared__ uint data[MERGE_THREADBLOCK_SIZE];

    uint sum = 0;
    for(uint i = threadIdx.x; i < histogramCount; i += MERGE_THREADBLOCK_SIZE)
        sum += d_PartialHistograms[blockIdx.x + i * HISTOGRAM64_BIN_COUNT];
    data[threadIdx.x] = sum;

    for(uint stride = MERGE_THREADBLOCK_SIZE / 2; stride > 0; stride >>= 1){
        __syncthreads();
        if(threadIdx.x < stride)
            data[threadIdx.x] += data[threadIdx.x + stride];
    }

    if(threadIdx.x == 0)
        d_Histogram[blockIdx.x] = data[0];
}
