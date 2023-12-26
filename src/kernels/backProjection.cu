__global__ void backProject2Dto3D(float *d_x, float *d_y, float *d_depth, float *d_K, float *d_R, float *d_t, float *d_output, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
    {
        float fx = d_K[0];
        float fy = d_K[4];
        float cx = d_K[2];
        float cy = d_K[5];

        float X_cam = (d_x[i] - cx) * d_depth[i] / fx;
        float Y_cam = (d_y[i] - cy) * d_depth[i] / fy;
        float Z_cam = d_depth[i];

        if (d_R != NULL && d_t != NULL)
        {
            // Assuming R is a 3x3 matrix and t is a 3x1 vector
            float P_cam[3] = {X_cam, Y_cam, Z_cam};
            for (int j = 0; j < 3; j++)
            {
                d_output[3 * i + j] = 0;
                for (int k = 0; k < 3; k++)
                {
                    d_output[3 * i + j] += d_R[j * 3 + k] * (P_cam[k] - d_t[k]);
                }
            }
        }
        else
        {
            d_output[3 * i] = X_cam;
            d_output[3 * i + 1] = Y_cam;
            d_output[3 * i + 2] = Z_cam;
        }
    }
}



// Function to run the kernel
void runBackProject2Dto3D(float *h_output, int n) {
    float *d_output;
    cudaMalloc(&d_output, n * sizeof(float));

    // Define the execution configuration
    int blockSize = 256;
    int numBlocks = (n + blockSize - 1) / blockSize;

    // Launch the kernel
    backProject2Dto3D<<<numBlocks, blockSize>>>(d_output, n);

    // Copy the result back to the host
    cudaMemcpy(h_output, d_output, n * sizeof(float), cudaMemcpyDeviceToHost);

    // Free device memory
    cudaFree(d_output);
}
