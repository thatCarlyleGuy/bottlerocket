

## Python Environment
### Create env
conda create --name bottlerocketv1 python=3.9 -y

### Write env to file
conda env export > environment.yml

conda activate bottlerocket
conda deactivate

conda info --envs

### Run env
conda activate bottlerocket
jupyter lab


