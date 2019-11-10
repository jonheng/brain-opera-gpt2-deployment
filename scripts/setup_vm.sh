export IMAGE_FAMILY="tf-1-14-cu100"
export ZONE="europe-west4-b"
export INSTANCE_NAME="brain-opera-gpt2"
export INSTANCE_TYPE="n1-standard-2"
export PROJECT_NAME="aibo-deployment"

gcloud config set project $PROJECT_NAME
gcloud config set compute/zone $ZONE

gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --image-family=$IMAGE_FAMILY \
        --image-project=deeplearning-platform-release \
        --maintenance-policy=TERMINATE \
        --machine-type=$INSTANCE_TYPE \
        --boot-disk-size=200GB \
        --metadata="install-nvidia-driver=True" \
        --tags=port8000

echo "Waiting for 5 minutes for VM to initialize"
sleep 300

# Copy model from local directory to VM
gcloud compute scp --recurse ./checkpoint brain-opera-gpt2:~/checkpoint

gcloud compute --project $PROJECT_NAME ssh --zone $ZONE $INSTANCE_NAME -- "$(< ./vm_commands.sh)"

echo "================SETUP COMPLETE=================="
echo "Take note of the External IP as shown below: "
gcloud compute instances list

echo "To do a final check, run the following command: curl <EXTERNAL_IP>:8000/"