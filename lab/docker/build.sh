#!/bin/bash

docker buildx build --platform linux/amd64,linux/arm64 -t acchapm1/myanalysis:1.0 .
