rm -r deploy.json
python concat_files.py
aws cloudformation deploy --template-file deploy.json --stack-name brockenStack
