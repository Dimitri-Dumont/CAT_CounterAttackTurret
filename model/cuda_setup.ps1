# setup_tensorflow_gpu.ps1

# Deactivate any active conda environment
Write-Host "Deactivating current conda environment..."
conda deactivate

# Remove existing environment if it exists
Write-Host "Removing existing tf-gpu environment if it exists..."
echo "y" | conda env remove -n tf-gpu

# Create new environment with Python 3.8
Write-Host "Creating new environment with Python 3.8..."
echo "y" | conda create -n tf-gpu python=3.8

# Activate the new environment
Write-Host "Activating tf-gpu environment..."
conda activate tf-gpu

# Install CUDA toolkit and cuDNN
Write-Host "Installing CUDA toolkit and cuDNN..."
echo "y" | conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1

# Install correct protobuf version
Write-Host "Installing protobuf..."
echo "y" | pip install protobuf==3.20.0

# Install TensorFlow
Write-Host "Installing TensorFlow..."
echo "y" | pip install tensorflow==2.7.0

# Set environment variables
Write-Host "Setting environment variables..."
$ENV_PATH = conda info --base
$ENV_PATH = "$ENV_PATH\envs\tf-gpu"
$env:PATH = "$ENV_PATH\Library\bin;" + $env:PATH
$env:CUDA_PATH = "$ENV_PATH\Library"
$env:CUDA_HOME = "$ENV_PATH\Library"

# Verify installation
Write-Host "`nVerifying installation..."
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__); print('GPU Available:', len(tf.config.list_physical_devices('GPU'))); print('CUDA Enabled:', tf.test.is_built_with_cuda())"

Write-Host "`nSetup complete! Environment 'tf-gpu' is ready to use."