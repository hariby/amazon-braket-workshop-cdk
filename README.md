
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

Check your AWS Account ID (12-digit numbers) or Alias to create a sign-in URL for participants: 
https://*account-ID-or-alias*.signin.aws.amazon.com/console

### How to login (for Participants)
Workshop admin will provide 3 informations: 
- Login URL, which contains Account ID (12 digits) or account alias, 
- IAM user name: `WorkshopUser-n` (n = 0, ..., N), and 
- Password. 

The users will be asked to update password when the initial login. 
The default password policy enforces the following conditions as in the [document](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html#default-policy-details):

- Minimum password length of 8 characters and a maximum length of 128 characters. 
- Minimum of three of the following mix of character types: uppercase, lowercase, numbers, and `! @ # $ % ^ & * ( ) _ + - = [ ] { } | '` symbols. 
- Not be identical to your AWS account name or email address. 
