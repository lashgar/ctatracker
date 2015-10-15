
__global__ void executeSecondLayer(float *Layer2_Neurons_GPU, float *Layer2_Weights_GPU,float *Layer3_Neurons_GPU)
{
	int blockID=blockIdx.x;
	int pixelX=threadIdx.x;
	int pixelY=threadIdx.y;


	int weightBegin=blockID*26*6;
	int windowX=pixelX*2;
	int windowY=pixelY*2;
    
	float result=0;

	
	result+=Layer2_Weights_GPU[weightBegin];
	
	if(blockID==1 && pixelX==0 && pixelY==0)
	{
		result+=0;
	}

	++weightBegin;

	for (int i=0; i<25; ++i )
    {
        result+=Layer2_Neurons_GPU[(windowX + 13*windowY +kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6];
        result+=Layer2_Neurons_GPU[(169 + windowX + 13*windowY +kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6+1];
	result+=Layer2_Neurons_GPU[(338 + windowX + 13*windowY + kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6+2];
        result+=Layer2_Neurons_GPU[(507 + windowX + 13*windowY + kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6+3];
        result+=Layer2_Neurons_GPU[(676 + windowX + 13*windowY + kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6+4];
        result+=Layer2_Neurons_GPU[(845 + windowX + 13*windowY + kernelTemplate2[i])+(13*13*6*blockIdx.y)]*Layer2_Weights_GPU[weightBegin+i*6+5];
	}

	result=(1.7159*tanhf(0.66666667*result));

	Layer3_Neurons_GPU[(5*5*blockID+pixelY*5+pixelX)+(1250*blockIdx.y)]=result;
}

