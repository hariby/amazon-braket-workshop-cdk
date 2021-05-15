
# Welcome to Braket Workshop CDK!

This is a CDK app which creates IAM User and IAM Role for Amazon Braket Hands-on Workshop. 

## Usage

### How to deploy (for Admin)
From you favorite environment (e.g., AWS CloudShell or AWS Cloud9), 

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

After the deployment, please retrieve the initial login password from AWS SecretsManager. 
Access the secret [`BraketWorkshop/IAMUser/InitialPassword` in Management Console](https://us-west-2.console.aws.amazon.com/secretsmanager/home?region=us-west-2#!/secret?name=BraketWorkshop%2FIAMUser%2FInitialPassword) 
or you can also use the AWS CLI command: 
```
aws secretsmanager get-secret-value --secret-id BraketWorkshop/IAMUser/InitialPassword --query 'SecretString' --output text
```

Check your AWS Account ID (12-digit numbers) or Alias to create a sign-in URL for participants: 
https://*account-ID-or-alias*.signin.aws.amazon.com/console

### How to login (for Participants)
Workshop admin will provide 3 informations: 
- Login URL, which contains Account ID (12 digits) or account alias, 
- IAM user name: `WorkshopUser-n` (n = 0, ..., N), and 
- Password. 
