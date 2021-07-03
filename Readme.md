# create env
conda create --name bottlerocketv1 python=3.9 -y

# write env to file
conda env export > environment.yml

conda activate bottlerocket
conda deactivate

conda info --envs

# run env
conda activate bottlerocket
jupyter lab


