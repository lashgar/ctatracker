__global__ void big_kernel(Cell *cells, int *cnumPars,Cell *cells2, int *cnumPars2,struct kernel_consts *dev,int *border) {

    int ix;
    int iy;
    int iz;

    int nx = blockDim.x * gridDim.x;
    int ny = blockDim.y * gridDim.y;
    int nz = blockDim.z * gridDim.z;

    ix = blockIdx.x * blockDim.x + threadIdx.x;
    iy = blockIdx.y * blockDim.y + threadIdx.y;
    iz = blockIdx.z * blockDim.z + threadIdx.z;

    //printf("x: %d : %d\n",nx,blockDim.x * gridDim.x);
    //printf("y: %d : %d\n",ny,blockDim.y * gridDim.y);
    //printf("z: %d : %d\n",nz,blockDim.z * gridDim.z);

    //move common declarations on top

    int index = (iz*ny + iy)*nx + ix;
    int np;  //internal loop limit

    //this should be moved to shared memory
    Cell &cell = cells[index];  //just a reference to the correspondig cell //FIXME

    int neighCells[27];

    //it is safe to move the call here, neighbours do not change between the two original calls

    //move this computation to cpu
    //const float tc_orig = hSq*hSq*hSq;

    const float parSize = 0.0002f;
    const float epsilon = 1e-10f;
    const float stiffness = 30000.f;
    const float damping = 128.f;

    /*
    for (i=0;i<27;i++) {
        neighCells[i] = 0xffffffff;
    }
    */
    int numNeighCells = InitNeighCellList(ix, iy, iz, neighCells,cnumPars);

    /*
    //printf("thread %d: number of neighbors: %d\n",index,numNeighCells);
    for (int i=0;i<numNeighCells;i++) {
        printf("thread %d : %d-th neighbor %d\n",index,i,neighCells[i]);
    }
    */

    ////////////////////////////////////////////////////////////////////////////////
    //void ClearParticlesMT(int i) {
    ////////////////////////////////////////////////////////////////////////////////

    /**/


    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //    for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //        for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    cnumPars[index] = 0;

    //                }  //close nested loop;



    __syncthreads();



    //} close ClearParticlesMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void RebuildGridMT(int i) {




    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    Cell const &cell2 = cells2[index];
    int np2 = cnumPars2[index];

    for (int j = 0; j < np2; ++j) {
        int ci = (int)((cell2.p[j].x - domainMin.x) / dev->delta.x);
        int cj = (int)((cell2.p[j].y - domainMin.y) / dev->delta.y);
        int ck = (int)((cell2.p[j].z - domainMin.z) / dev->delta.z);

        if (ci < 0) ci = 0; else if (ci > (nx-1)) ci = nx-1;
        if (cj < 0) cj = 0; else if (cj > (ny-1)) cj = ny-1;
        if (ck < 0) ck = 0; else if (ck > (nz-1)) ck = nz-1;

        int index2 = (ck*ny + cj)*nx + ci;
        // this assumes that particles cannot travel more than one grid cell per time step
        int np_renamed = cnumPars[index2];

        if (border[index2]) {
            //use atomic
            atomicAdd(&cnumPars[index2],1);
        } else {
            cnumPars[index2]++;
        }

        //#warning what if we exceed CELL_PARTICLES particles per cell here??
        //from what I see is that we calculate the same frame over and over
        //so every cell has at most CELL_PARTICLES particles, from the initialisation


        Cell &cell_renamed = cells[index2];
        cell_renamed.p[np_renamed].x = cell2.p[j].x;
        cell_renamed.p[np_renamed].y = cell2.p[j].y;
        cell_renamed.p[np_renamed].z = cell2.p[j].z;
        cell_renamed.hv[np_renamed].x = cell2.hv[j].x;
        cell_renamed.hv[np_renamed].y = cell2.hv[j].y;
        cell_renamed.hv[np_renamed].z = cell2.hv[j].z;
        cell_renamed.v[np_renamed].x = cell2.v[j].x;
        cell_renamed.v[np_renamed].y = cell2.v[j].y;
        cell_renamed.v[np_renamed].z = cell2.v[j].z;
        //cell_renamed.debug[np_renamed] = index2;
    }

    //                }  //close nested loops



    __syncthreads();




    //} close RebuildGridMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void InitDensitiesAndForcesMT(int i) {

    //from now on we don't change the cnumPars[index]
    np = cnumPars[index];  //internal loop limit


    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    Cell &cell = cells[index];

    //    int np = cnumPars[index];

    for (int j = 0; j < np; ++j) {
        cell.density[j] = 0.f;
        cell.a[j].x = externalAcceleration.x;
        cell.a[j].y = externalAcceleration.y;
        cell.a[j].z = externalAcceleration.z;
    }


    //                }  //close nested loops



    __syncthreads();




    //} close InitDensitiesAndForcesMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void ComputeDensitiesMT(int i) {




    //    int neighCells[27];

    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    int np = cnumPars[index];

    //    if (np == 0)  continue;
    //
    // if np==0 we do net enter the following loop

    //    int numNeighCells = InitNeighCellList(ix, iy, iz, neighCells);

    //    Cell &cell = cells[index];

    Vec3 tmp;

    for (int j = 0; j < np; ++j)
        for (int inc = 0; inc < numNeighCells; ++inc) {
            int indexNeigh = neighCells[inc];
            Cell &neigh = cells[indexNeigh];
            int numNeighPars = cnumPars[indexNeigh];
            for (int iparNeigh = 0; iparNeigh < numNeighPars; ++iparNeigh)
                if (&neigh.p[iparNeigh] < &cell.p[j]) {
                    //float distSq = (cell.p[j] - neigh.p[iparNeigh]).GetLengthSq();
                    float distSq;
                    operator_sub(&tmp,&cell.p[j],&neigh.p[iparNeigh]);
                    distSq = GetLengthSq(&tmp);
                    if (distSq < dev->hSq) {
                        float t = dev->hSq - distSq;
                        float tc = t*t*t;

                        if (border[index]) {
                            //use atomic
                            atomicAdd(&cell.density[j],tc);
                        } else {
                            cell.density[j] += tc;
                        }

                        if (border[indexNeigh]) {
                            //use atomic
                            atomicAdd(&neigh.density[iparNeigh],tc);
                        } else {
                            neigh.density[iparNeigh] += tc;
                        }
                    }
                }
            ;
        }

    //                }  //close nested loops



    __syncthreads();


    //} close ComputeDensitiesMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void ComputeDensities2MT(int i) {




    //    const float tc = hSq*hSq*hSq;


    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    Cell &cell = cells[index];

    //    int np = cnumPars[index];

    for (int j = 0; j < np; ++j) {
        cell.density[j] += dev->tc_orig;
        cell.density[j] *= dev->densityCoeff;
    }

    //                }  //close nested loops



    __syncthreads();




    //} close ComputeDensities2MT()
    ////////////////////////////////////////////////////////////////////////////////
    //void ComputeForcesMT(int i) {




    //    int neighCells[27];

    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    int np = cnumPars[index];

    //    if (np == 0)  continue;
    //
    // if np==0 we do net enter the following loop

    //    int numNeighCells = InitNeighCellList(ix, iy, iz, neighCells);

    //    Cell &cell = cells[index];

    for (int j = 0; j < np; ++j)
        for (int inc = 0; inc < numNeighCells; ++inc) {
            int indexNeigh = neighCells[inc];
            Cell &neigh = cells[indexNeigh];
            int numNeighPars = cnumPars[indexNeigh];
            for (int iparNeigh = 0; iparNeigh < numNeighPars; ++iparNeigh)
                if (&neigh.p[iparNeigh] < &cell.p[j]) {
                    //Vec3 disp = cell.p[j] - neigh.p[iparNeigh];
                    //float distSq = disp.GetLengthSq();
                    Vec3 disp;
                    operator_sub(&disp,&cell.p[j],&neigh.p[iparNeigh]);
                    float distSq = GetLengthSq(&disp);
                    if (distSq < dev->hSq) {
                        //float dist = sqrtf(std::max(distSq, 1e-12f));
                        float dist = sqrtf(fmax(distSq, 1e-12f));
                        float hmr = dev->h - dist;

                        //Vec3 acc = disp * pressureCoeff * (hmr*hmr/dist) *
                        //    (cell.density[j]+neigh.density[iparNeigh] - doubleRestDensity);

                        //acc += (neigh.v[iparNeigh] - cell.v[j]) * viscosityCoeff * hmr;
                        //acc /= cell.density[j] * neigh.density[iparNeigh];

                        Vec3 acc;
                        operator_mult(&acc,&disp, dev->pressureCoeff * (hmr*hmr/dist) *
                                      (cell.density[j]+neigh.density[iparNeigh] - doubleRestDensity));

                        operator_sub(&tmp,&neigh.v[iparNeigh],&cell.v[j]);
                        operator_mult(&tmp,&tmp,dev->viscosityCoeff * hmr);
                        operator_add(&acc,&acc,&tmp);
                        operator_div(&acc,&acc,cell.density[j] * neigh.density[iparNeigh]);

                        if (border[index]) {
                            //use atomics
#warning this works because no one reads these values at the moment ??
                            atomicAdd(&cell.a[j].x,acc.x);
                            atomicAdd(&cell.a[j].y,acc.y);
                            atomicAdd(&cell.a[j].z,acc.z);
                        } else {
                            operator_add(&cell.a[j],&cell.a[j],&acc);
                        }

                        if (border[indexNeigh]) {
                            //use atomics
#warning this works because no one reads these values at the moment ??
                            //reminder: there is no atomicSub for floats, so we add the negative value
                            atomicAdd(&neigh.a[iparNeigh].x,-acc.x);
                            atomicAdd(&neigh.a[iparNeigh].y,-acc.y);
                            atomicAdd(&neigh.a[iparNeigh].z,-acc.z);
                        } else {
                            operator_sub(&neigh.a[iparNeigh],&neigh.a[iparNeigh],&acc);
                        }
                    }
                }
        }

    //                }  //close nested loops



    __syncthreads();




    //} close ComputeForcesMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void ProcessCollisionsMT(int i) {




    //    const float parSize = 0.0002f;
    //    const float epsilon = 1e-10f;
    //    const float stiffness = 30000.f;
    //    const float damping = 128.f;

    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    Cell &cell = cells[index];

    //    int np = cnumPars[index];

    for (int j = 0; j < np; ++j) {
        //Vec3 pos = cell.p[j] + cell.hv[j] * timeStep;
        Vec3 pos;
        operator_mult(&pos,&cell.hv[j],timeStep);
        operator_add(&pos,&pos,&cell.p[j]);

        float diff = parSize - (pos.x - domainMin.x);
        if (diff > epsilon)
            cell.a[j].x += stiffness*diff - damping*cell.v[j].x;

        diff = parSize - (domainMax.x - pos.x);
        if (diff > epsilon)
            cell.a[j].x -= stiffness*diff + damping*cell.v[j].x;

        diff = parSize - (pos.y - domainMin.y);
        if (diff > epsilon)
            cell.a[j].y += stiffness*diff - damping*cell.v[j].y;

        diff = parSize - (domainMax.y - pos.y);
        if (diff > epsilon)
            cell.a[j].y -= stiffness*diff + damping*cell.v[j].y;

        diff = parSize - (pos.z - domainMin.z);
        if (diff > epsilon)
            cell.a[j].z += stiffness*diff - damping*cell.v[j].z;

        diff = parSize - (domainMax.z - pos.z);
        if (diff > epsilon)
            cell.a[j].z -= stiffness*diff + damping*cell.v[j].z;
    }

    //                }  //close nested loops



    __syncthreads();




    //} close ProcessCollisionsMT()
    ////////////////////////////////////////////////////////////////////////////////
    //void AdvanceParticlesMT(int i) {




    //    for (int iz = grids[i].sz; iz < grids[i].ez; ++iz)
    //        for (int iy = grids[i].sy; iy < grids[i].ey; ++iy)
    //            for (int ix = grids[i].sx; ix < grids[i].ex; ++ix) {

    //    int index = (iz*ny + iy)*nx + ix;

    //    Cell &cell = cells[index];

    //    int np = cnumPars[index];

    for (int j = 0; j < np; ++j) {
        //Vec3 v_half = cell.hv[j] + cell.a[j]*timeStep;
        Vec3 v_half;
        operator_mult(&v_half,&cell.a[j],timeStep);
        operator_add(&v_half,&v_half,&cell.hv[j]);

        //cell.hv[j] = v_half;
        cell.hv[j].x = v_half.x;
        cell.hv[j].y = v_half.y;
        cell.hv[j].z = v_half.z;

        //cell.v[j] *= 0.5f;
        operator_mult(&cell.v[j],&cell.v[j],0.5f);

        //cell.v[j] = cell.hv[j] + v_half;
        operator_add(&cell.v[j],&cell.hv[j],&v_half);

        //we can change v_half now, (we want to use only one tmp variable)
        //cell.p[j] += v_half * timeStep;
        operator_mult(&v_half,&v_half,timeStep);
        operator_add(&cell.p[j],&cell.p[j],&v_half);
    }

    //                }  //close nested loops



    __syncthreads();




    //} close AdvanceParticlesMT()
    ////////////////////////////////////////////////////////////////////////////////

/**/


} //close big_kernel()

