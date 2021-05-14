
# Welcome to Braket Workshop CDK!

This is a CDK app which creates IAM User and IAM Role for Amazon Braket Hands-on Workshop. 

## Usage

### How to deploy (for Admin)

```
sudo npm install -g aws-cdk

git clone https://github.com/hariby/amazon-braket-workshop-cdk.git
cd amazon-braket-workshop-cdk/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk synth
cdk deploy braket-workshop-cdk
```

### How to login (for Participants)
- Share Management Console login user: `WorkshopUserXXXXXXXXX` and password: `InitialPassword!!` with participants. 
