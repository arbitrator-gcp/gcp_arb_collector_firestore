gcloud config set project arbitrator-251115

deploy a virtual environment
```
python3.7 -m venv /home/phil/vscode_proj/gcp_arb_collector_firebase/.envfirebase
source /home/phil/vscode_proj/gcp_arb_collector_firebase/.envfirebase/bin/activate
pip install google-cloud-firestore
```

```
gcloud functions deploy collector --memory=128MB --runtime python37 --trigger-http

gcloud functions deploy collector --memory=128MB --runtime python37 --trigger-topic exch_collector_topic	
```
