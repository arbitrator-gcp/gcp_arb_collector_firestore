deploy a virtual environment
```
python3.7 -m venv /home/phil/vscode_proj/gcp_arb_collector_firebase/.envfirebase
source /home/phil/vscode_proj/gcp_arb_collector_firebase/.envfirebase/bin/activate
```

```
gcloud functions deploy collector --runtime python37 --trigger-http

gcloud functions deploy collector --runtime python37 --trigger-topic collector
```
