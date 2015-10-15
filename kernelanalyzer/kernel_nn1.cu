__global__ void executeFirstLayer(float *Layer1_Neurons_GPU,float *Layer1_Weights_GPU,float *Layer2_Neurons_GPU)
{
	int blockID=blockIdx.x;
	int pixelX=threadIdx.x;
	int pixelY=threadIdx.y;


	int weightBegin=blockID*26;
	int windowX=pixelX*2;
	int windowY=pixelY*2;

	float result=0;

	result+=Layer1_Weights_GPU[weightBegin];

	++weightBegin;

	for(int i=0;i<25;++i)
	{
		result+=Layer1_Neurons_GPU[(windowY*29+windowX+kernelTemplate[i])+(29*29*blockIdx.y)]*Layer1_Weights_GPU[weightBegin+i];
	}

	result=(1.7159*tanhf(0.66666667*result));

	Layer2_Neurons_GPU[(13*13*blockID+pixelY*13+pixelX)+(13*13*6*blockIdx.y)]=result;

}


