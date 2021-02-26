# This code gets the Project ID from gcloud
export PROJECT_ID=`gcloud config get-value project`
echo Project ID: $PROJECT_ID

# export variables
export IMG_PREP=gcr.io/$PROJECT_ID/kf-preprocess:v1
export IMG_TRAIN=gcr.io/$PROJECT_ID/kf-train:v1
export IMG_TEST=gcr.io/$PROJECT_ID/kf-test:v1

# build and push preprocess image
docker build -t $IMG_PREP scripts/preprocess/.
gcloud docker -- push $IMG_PREP

# build and push train image
docker build -t $IMG_TRAIN scripts/train/.
gcloud docker -- push $IMG_TRAIN

# build and push test image
docker build -t $IMG_TEST scripts/test/.
gcloud docker -- push $IMG_TEST