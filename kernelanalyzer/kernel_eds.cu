__global__ void sobel_gpu(QUANTUM_TYPE *img_out, QUANTUM_TYPE *img_in, int WIDTH, int HEIGHT){
	int xc,yc;
	xc=blockDim.x*blockIdx.x+threadIdx.x;
	yc=blockDim.y*blockIdx.y+threadIdx.y;
    QUANTUM_TYPE LUp,LCnt,LDw,RUp,RCnt,RDw;
	int pixel;
    int xm1=xc-1;
    int xp1=xc+1;
    int ym1=yc-1;
    int yp1=yc+1;


	if(xc<WIDTH && yc<HEIGHT){
        QUANTUM_TYPE p1=img_in[xm1+ym1*WIDTH];
        QUANTUM_TYPE p2=img_in[xm1+yc*WIDTH];
        QUANTUM_TYPE p3=img_in[xm1+yp1*WIDTH];
        QUANTUM_TYPE p4=img_in[xp1+ym1*WIDTH];
        QUANTUM_TYPE p5=img_in[xp1+yc*WIDTH];
        QUANTUM_TYPE p6=img_in[xp1+yp1*WIDTH];
        LUp = (xc-1>=0 && yc-1>=0)? p1:0;
        LCnt= (xc-1>=0)? p2:0;
        LDw = (xc-1>=0 && yc+1<HEIGHT)? p3:0;
        RUp = (xc+1<WIDTH && yc-1>=0)? p4:0;
        RCnt= (xc+1<WIDTH)? p5:0;
        RDw = (xc+1<WIDTH && yc+1<HEIGHT)? p6:0;
        pixel = -1*LUp  + 1*RUp +
                -2*LCnt + 2*RCnt +
                -1*LDw  + 1*RDw;
        pixel=(pixel<0)?0:pixel;
        pixel=(pixel>MAXRGB)?MAXRGB:pixel;
        img_out[xc+yc*WIDTH]=pixel;
	}
}
