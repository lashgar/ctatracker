__global__ 
void euclid(char *data, float x2, float y2,float *z, int N, int W, int L_POS)
{
	int idx=blockIdx.x*blockDim.x+threadIdx.x;
	float tmp_lat=0.0, tmp_long=0.0;
	int position = ( idx * W ) + L_POS - 1;	
	
	if(idx < N) {
		char temp1[5];
		for( int i = 0 ; i < 5 ; i++ ) {
			temp1[i] = data[position+i];
		}
		char temp2[5];
		for( int i = 0 ; i < 5 ; i++ ) {
			temp2[i] = data[position+6+i];
		}
		
		int dig1, dig2, dig3, dig_1;
		if( temp1[0] == ' ' ) { dig1 = 0; }
		else {
			dig1 = temp1[0] - 48;
			tmp_lat += dig1 * 100;
		}
		if( temp1[1] == ' ' ) { dig2 = 0; }
		else {
			dig2 = temp1[1] - 48;
			tmp_lat += dig2 * 10;
		}
		if( temp1[2] == ' ' ) { dig3 = 0; }
		else {
			dig3 = temp1[2] - 48;
			tmp_lat += dig3 * 1;
		}
		dig_1 = temp1[4] - 48;
		tmp_lat += (float) dig_1 / 10;

		if( temp2[0] == ' ' ) { dig1 = 0; }
		else {
			dig1 = temp2[0] - 48;
			tmp_long += dig1 * 100;
		}
		if( temp2[1] == ' ' ) { dig2 = 0; }
		else {
			dig2 = temp2[1] - 48;
			tmp_long += dig2 * 10;
		}
		if( temp2[2] == ' ' ) { dig3 = 0; }
		else {
			dig3 = temp2[2] - 48;
			tmp_long += dig3 * 1;
		}
		dig_1 = temp2[4] - 48;
		tmp_long += (float) dig_1 / 10;

		z[idx]=sqrt(((tmp_lat-x2)*(tmp_lat-x2))+((tmp_long-y2)*(tmp_long-y2)));
	}
}


