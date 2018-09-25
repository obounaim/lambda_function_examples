zip_dir=$(pwd)
lib_dir="./lambda_venv/lib/python3.6/site-packages/"

cd $lib_dir
7z a "$zip_dir/fonction_lambda.zip" .
cd $zip_dir
7z a "$zip_dir/fonction_lambda.zip" main.py 
7z d "$zip_dir/fonction_lambda.zip" pip wheel setuptools
