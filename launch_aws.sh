#!/bin/bash

aws emr create-cluster \
    --name "Spark cluster" \
    --release-label emr-5.14.0 \
    --applications Name=Spark \
    --ec2-attributes SubnetId=subnet-18171730,KeyName=feb2016-keypair \
    --instance-type m4.large --instance-count 3 --use-default-roles