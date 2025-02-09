# Lipo Solar AI Core Forecast
### Registry url
`484907517561.dkr.ecr.ap-northeast-2.amazonaws.com/lipo-solar-prediction:latest`


## To build inference_code
```
cd ./inference_code

docker buildx build -t lipo-solar-prediction:latest . --output type=docker,oci-mediatypes=false --provenance=false                                                                                                                    
```

After building the inference image, push it to aws registry.
First, login to aws cli
```
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 484907517561.dkr.ecr.ap-northeast-2.amazonaws.com
```

Tag image
```
docker tag lipo-solar-prediction:latest 484907517561.dkr.ecr.ap-northeast-2.amazonaws.com/lipo-solar-prediction:latest

```

Finally, push the image to registry
```
docker push 484907517561.dkr.ecr.ap-northeast-2.amazonaws.com/lipo-solar-prediction:latest
```

## Training the model
Source: [Fake RUL model](https://colab.research.google.com/drive/1009ddqnexg653eyXr6hzjnfHkE4AIwtH?usp=sharing#scrollTo=cMK-sNNEuikk)

After training, save model 
```
model_path = "model.pt"
torch.save(model.state_dict(), model_path)
```

Download model from colab, then compress the model. For example, SOH Predictor Model
```
tar -czvf rul_predictor.tar.gz model.pt
```

Then, upload the compressed model to s3 bucket. 

## To deploy

Navigate to [Models panel](https://ap-northeast-2.console.aws.amazon.com/sagemaker/home?region=ap-northeast-2#/models)  on aws console and create a new model.
