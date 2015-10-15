__global__ void 
findK(	long height,
		knode *knodesD,
		long knodes_elem,
		record *recordsD,

		long *currKnodeD,
		long *offsetD,
		int *keysD, 
		record *ansD)
{

	// private thread IDs
	int thid = threadIdx.x;
	int bid = blockIdx.x;

	// processtree levels
	int i;
	for(i = 0; i < height; i++){

		if((knodesD[currKnodeD[bid]].keys[thid]) <= keysD[bid] && (knodesD[currKnodeD[bid]].keys[thid+1] > keysD[bid])){
			if(knodesD[offsetD[bid]].indices[thid] < knodes_elem){
				offsetD[bid] = knodesD[offsetD[bid]].indices[thid];
			}
		}
		__syncthreads();

		// set for next tree level
		if(thid==0){
			currKnodeD[bid] = offsetD[bid];
		}
		__syncthreads();

	}

	if(knodesD[currKnodeD[bid]].keys[thid] == keysD[bid]){
		ansD[bid].value = recordsD[knodesD[currKnodeD[bid]].indices[thid]].value;
	}

}
