# Brain Opera GPT-2 deployment

## Starting gunicorn server

```sh
gunicorn -b :8000 server:app
```

## Building docker image

```sh
docker build -t brain-opera-gpt2 .
```

## Running docker image

```sh
This will run the docker image in the background
docker run -d -p 8000:8000 brain-opera-gpt2
```

## Steps to deploying

1. **Create a Google Cloud Platform account**

2. **Install Cloud SDK and enable Google Kubernetes Engine API**

Follow the the steps for installing cloud SDK and enabling Google Kubernetes Engine API
under the "Before you begin" section:
<https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster>

If you do not have kubectl, you can install it as part of the Google Cloud SDK

```sh
gcloud components install kubectl
```

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

# Set compute zone
gcloud config set compute/zone asia-southeast1-b
```

5. **Set quota for GPU**

The default GPU quota for a GCP account with free credits is 0.
A request for an increase in this quota is necessary to use GPUs.

Go to <https://console.cloud.google.com/iam-admin/quotas>.
Make sure that `brain-opera-deployment` is chosen as the project in the header, as shown in the image below.
Filter metric by `GPUs (all regions)`. If the limit is 0, tick the checkbox and click on the `Edit Quotas` button at the top.

![GCP quota](images/gcp_quota.png)

Fill in the necessary info and request for the limit to be raised to 1.
An email will be sent to you for the quota request.
The wait time is usually a few hours before the quota request is granted.

6. **Build and push image to Google Cloud Registry**

First, enable the following APIs for the project, which are needed to create a
cluster, build and publish a container into the Google Container registry.

```sh
gcloud services enable container.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

Then, update components.

```sh
# Enter [Y] when prompted
gcloud components update
```

7. **Create your GKE Cluster and GPU node pool**

```sh
# Creates a cluster named brain-opera-cluster
gcloud container clusters create brain-opera-cluster \
  --machine-type=n1-standard-2 \
  --zone=asia-southeast1-b \
  --num-nodes=1 \
  --accelerator type=nvidia-tesla-p4,count=1
```

```sh
# Set some defaults for gcloud config
gcloud config set run/cluster brain-opera-cluster
gcloud config set run/cluster_location asia-southeast1-b
```

```sh
# Install NVIDIA GPU device drivers
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
```

8. **Deploy the image to your GKE cluster**

First, build a Docker image and push it to Google Container Registry.

```sh
gcloud builds submit --tag gcr.io/brain-opera-deployment/helloworld

gcloud builds submit --tag gcr.io/brain-opera-deployment/gpt2-model
```

Next, deploy the container and various services to the GKE cluster.

```sh
# Create various parts of the kubernetes cluster individually
kubectl create -f ./kubernetes/deployment.yaml
kubectl create -f ./kubernetes/service.yaml
kubectl create -f ./kubernetes/ingress.yaml

# OR apply them all at once
kubectl apply -f kubernetes
```

The ingress step takes a while (~10mins).
Check that everything works.

```sh
# Run the following command after ~10mins
# Check that under ingress.kubernetes.io/backends, it displays: { <some_key>: "HEALTHY" }, which means everything is ok
# If is displays "UNKNOWN", wait a little longer

kubectl describe ing brain-opera-ingress
```

If everything is ok, copy and paste the IP address from the above command into your browser. You should see a page which says {'health': 'good'}.

9. **Cleaning up**

Delete the cluster.

```sh
gcloud container clusters delete brain-opera-cluster
```
