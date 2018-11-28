# COMP550-A4Q2
Document summarization using SUMBASIC and Google News API

pip install -r requirements.txt

python sumbasic.py <method_name> "<file_n>*"

For example,
python ./sumbasic.py simplified "./docs/doc1-*.txt" > simplified-1.txt
should run the simplified version of the summarizer on the first cluster, writing the output to a text file
called simplified-1.txt.
