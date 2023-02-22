#!/bin/sh

# variables
aws_region="eu-west-1"
aws_account_id="845325376577"
aws_ecr_name="mobileapi"
aws_cluster_name="test"
aws_service_name="testservice"

# pre-build
echo "authenticating the docker cli to use the ECR registry..."
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

# build
echo "building image..."
# docker build -f project/Dockerfile --platform=linux/amd64 -t $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev ./project/

# post-build
echo "pushing image to AWS ECR..."
# docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:dev

echo "updating ECS service..."
aws ecs update-service --cluster $aws_cluster_name --service $aws_service_name --force-new-deployment

echo "done!"