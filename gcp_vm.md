# Deploying model on GCP virtual machine

## Steps to deploy

1. **Create a Google Cloud Platform account**

2. **Install Cloud SDK**

Follow the the steps for installing cloud SDK:
<https://cloud.google.com/sdk/install>

3. **After installing Cloud SDK, initialize it**

```sh
# Run the following command to initialize
# This will ask you to link your Google Cloud Platform account
gcloud init
```

4. **Create and configure GCP project**

```sh
# This commands creates a project with the name `brain-opera-deployment`
gcloud projects create brain-opera-deployment

# Set your working project
gcloud config set project brain-opera-deployment

# If the above project name is taken, choose a differet project name
# Note: project names need to be unique across GCP

# Set compute zone
gcloud config set compute/zone asia-southeast1-b
```

5. **Set quota for GPU**

First, go to the _Compute Engine_ tab and initialize it. Wait for it to complete.

The default GPU quota for a GCP account with free credits is 0.
A request for an increase in this quota is necessary to use GPUs.

Go to <https://console.cloud.google.com/iam-admin/quotas>.
Make sure that `brain-opera-deployment` is chosen as the project in the header, as shown in the image below.
Filter metric by `GPUs (all regions)`. If the limit is 0, tick the checkbox and click on the `Edit Quotas` button at the top.

![GCP quota](images/gcp_quota.png)

Fill in the necessary info and request for the limit to be raised to 1.
An email will be sent to you for the quota request.
The wait time is usually a few hours before the quota request is granted.

6. **Set firewall rules**

```sh
gcloud compute --project=brain-opera-deployment firewall-rules create brain-opera-port8000 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8000 --source-ranges=0.0.0.0/0 --target-tags=port8000
```

7. **Create VM**

```sh
export IMAGE_FAMILY="tf-1-14-cu100"
export ZONE="asia-southeast1-b"
export INSTANCE_NAME="brain-opera-gpt2"
export INSTANCE_TYPE="n1-standard-2"

gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --image-family=$IMAGE_FAMILY \
        --image-project=deeplearning-platform-release \
        --maintenance-policy=TERMINATE \
        --accelerator="type=nvidia-tesla-p4,count=1" \
        --machine-type=$INSTANCE_TYPE \
        --boot-disk-size=200GB \
        --metadata="install-nvidia-driver=True" \
        --tags=port8000
```

8. **Setup VM**

```sh
# Copy model from local directory to VM
gcloud compute scp --recurse ./checkpoint brain-opera-gpt2:~/checkpoint
```

```sh
# SSH into machine
gcloud compute --project "brain-opera-deployment" ssh --zone "asia-southeast1-b" "brain-opera-gpt2"

# Clone repo
git clone https://github.com/jonheng/brain-opera-gpt2-deployment.git

# Move model into repo
mv checkpoint/ brain-opera-gpt2-deployment/checkpoint

# Go to cloned repo
cd brain-opera-gpt2-deployment/

# Install python3-venv, enter Y when prompted
sudo apt-get install python3-venv

# Install required libraries
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start server
gunicorn -b :8000 server:app
```

9. **Final test**

Check your application IP

```sh
gcloud compute instances list
```

Test that the connection works

10. **Clean up**

```sh
# To delete the vm instance
gcloud compute instances delete brain-opera-gpt2

# To delete entire project
gcloud projects delete brain-opera-deployment
```
