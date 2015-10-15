__global__  __device__ void render(float4* d_debug_float4, uint* d_debug_uint, uint * result, Node * dnode, uint imageW, uint imageH, float pas, float df)
{
	uint x = __umul24(blockIdx.x, blockDim.x) + threadIdx.x;
    uint y = __umul24(blockIdx.y, blockDim.y) + threadIdx.y;
	uint tid(__umul24(threadIdx.y, blockDim.x) + threadIdx.x);

	uint id=(x + y * imageW);
	float4 pile[5];
	uint Obj, nRec(5), n(0);
	float prof, tmp;

	for( int i(0); i < nRec; ++i )
		pile[i] = make_float4(0.0f,0.0f,0.0f,1.0f);

	if( x < imageW && y < imageH )
	{
		prof = 10000.0f;
		result[id] = 0;
		float tPixel(2.0f/float(min(imageW,imageH)));
		float4 f(make_float4(0.0f,0.0f,0.0f,1.0f));
		matrice3x4 M(MView);
		Rayon R;
		R.A = make_float3(M.m[0].w,M.m[1].w,M.m[2].w);
		R.u = make_float3(M.m[0])*df
			+ make_float3(M.m[2])*(float(x)-float(imageW)*0.5f)*tPixel
			+ make_float3(M.m[1])*(float(y)-float(imageH)*0.5f)*tPixel;
		R.u = normalize(R.u);
		__syncthreads();

		for( int i(0); i < nRec && n == i; i++ ) {

			for( int j(0); j < numObj; j++ ) {
				Node nod(cnode[j]);
				Sphere s(nod.s);
				float t;
				s.C.x += pas;
				if( nod.fg )
					t = intersectionPlan(R,s.C,s.C);
				else
					t = intersectionSphere(R,s.C,s.r);

				if( t > 0.0f && t < prof ) {
					prof = t;
					Obj = j;
				}
			}
			float t = prof;
			if( t > 0.0f && t < 10000.0f ) {
				n++;
				Node nod(cnode[Obj]);
				Sphere s(nod.s);
				s.C.x += pas;
				float4 color(make_float4(s.R,s.V,s.B,s.A));
				float3 P(R.A+R.u*t), L(normalize(make_float3(10.0f,10.0f,10.0f)-P)), V(normalize(R.A-P));
				float3 N(nod.fg?getNormaleP(P):getNormale(P,s.C));
				float3 Np(dot(V,N)<0.0f?(-1*N):N);
				pile[i] = 0.05f * color;
            if( dot(Np,L) > 0.0f && notShadowRay(cnode,P,L,pas) ) {
					float3 Ri(normalize(L+V));
					//Ri = (L+V)/normalize(L+V);
					pile[i] += 0.3f * color* (min(1.0f,dot(Np,L)));

               #ifdef FIXED_CONST_PARSE
					tmp = 0.8f * pow(max(0.0f,min(1.0f,dot(Np,Ri))),50.0f);
               #else
               tmp = 0.8f * float2int_pow50(max(0.0f,min(1.0f,dot(Np,Ri))));
               #endif
					pile[i].x += tmp;
					pile[i].y += tmp;
					pile[i].z += tmp;

				}

				R.u = 2.0f*N*dot(N,V) - V;
				R.u = normalize(R.u);
				R.A = P+R.u*0.0001f;
			}
			prof = 10000.0f;
		}
      for( int i(n-1); i > 0; i-- )
				pile[i-1] = pile[i-1] + 0.8f*pile[i];
      result[id] += rgbaFloatToInt(pile[0]);
	}
}

