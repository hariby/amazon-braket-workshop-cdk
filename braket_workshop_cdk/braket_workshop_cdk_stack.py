from aws_cdk import (
    aws_iam as iam, 
    aws_secretsmanager as secretsmanager, 
    aws_cloudformation as cfn, 
    core
)
import aws_cdk.aws_sagemaker as sagemaker

life_cycle_config_script = core.Fn.base64("""
#!/usr/bin/env bash
sudo -u ec2-user -i <<EOS
TMPDIR=$(mktemp -d)
cd "$TMPDIR"

aws s3 cp s3://braketnotebookcdk-notebooklccs3bucketb3089b50-68b4kazkyfol/notebook/braket-notebook-lcc.zip braket-notebook-lcc.zip
unzip braket-notebook-lcc.zip
./install.sh

nohup rm -fr "$TMPDIR" &
EOS"""
)

class BraketWorkshopNotebookStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, notebook_role_arn: str, partition_remainder: int, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        braket_notebook_life_cycle_config = sagemaker.CfnNotebookInstanceLifecycleConfig(
            self, "BraketNotebookInstanceLifecycleConfigOnStart", 
            on_start=[{"content": life_cycle_config_script}]
            )
        
        # Create SageMaker Notebook
        num_users = int(self.node.try_get_context("num_users"))
        for i in range(num_users//3): 
            sagemaker.CfnNotebookInstance(
                self, f"BraketNotebook{i*3+partition_remainder}", 
                notebook_instance_name=f"amazon-braket-workshop-user-{i*3+partition_remainder}", 
                instance_type="ml.t3.medium", 
                role_arn=notebook_role_arn, 
                lifecycle_config_name=braket_notebook_life_cycle_config.attr_notebook_instance_lifecycle_config_name
            )

class BraketWorkshopIAMStack(core.Stack):
    
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create IAM User/Group 
        workshop_user_group = iam.Group(
            self, "BraketWorkshopGroup", 
            group_name="BraketWorkshopGroup"
        )
            
        workshop_user_group_policy_doc = iam.PolicyDocument()
        
        workshop_user_group_policy_statement_sagemaker = iam.PolicyStatement(
            sid="SageMakerActions", 
            actions=[
                "sagemaker:DeleteNotebookInstance",
                "sagemaker:StopNotebookInstance",
                "sagemaker:CreatePresignedNotebookInstanceUrl",
                "sagemaker:CreateNotebookInstanceLifecycleConfig",
                "sagemaker:ListNotebookInstances",
                "sagemaker:CreateNotebookInstance"
            ], 
            resources=["*"]
        )
            
        workshop_user_group_policy_statement_iam = iam.PolicyStatement(
            sid="IamPassRole", 
            actions=[
                "iam:PassRole"
            ], 
            resources=["arn:aws:iam::*:role/AmazonBraketServiceSageMakerNotebookRole-*"]
        )
        
        workshop_user_group_policy_doc.add_statements(
            workshop_user_group_policy_statement_sagemaker
        )
        
        workshop_user_group_policy_doc.add_statements(
            workshop_user_group_policy_statement_iam
        )
        
        workshop_user_group_policy = iam.Policy(
            self, id="BraketWorkshopUserGroupIAMPolicy", 
            document=workshop_user_group_policy_doc, 
            groups=[workshop_user_group], 
            policy_name="BraketWorkshopUserGroupIAMPolicy"
        )
            
        workshop_user_group.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBraketFullAccess")
        )
        
        workshop_user_group.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsReadOnlyAccess")
        )
        
        workshop_user_group.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("IAMUserChangePassword")
        )
        
        user_password = core.CfnParameter(self, "DefaultUserPassword", 
            description='The default password of WorkshopUsers which will be required for initial login.', 
            max_length=128,
            min_length=8,
            no_echo=True
        )
        
        num_users = int(self.node.try_get_context("num_users"))
        for i in range(num_users): 
            iam_user = iam.User(
                self, f"WorkshopUser{i}", 
                user_name=f"WorkshopUser-{i}", 
                groups=[workshop_user_group], 
                password=core.SecretValue(user_password), 
                password_reset_required=True
            )
        
        # Create IAM Role for Notebook 
        braket_notebook_role = iam.Role(
            self, "AmazonBraketServiceSageMakerNotebookRole-", 
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"), 
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBraketFullAccess")
            ], 
            role_name="AmazonBraketServiceSageMakerNotebookRole-ForBraketWorkshop"
        )
        
        # Passing to notebook stacks
        self.braket_notebook_role = braket_notebook_role
        
        sagemaker_notebook_policy_doc = iam.PolicyDocument()
        
        sagemaker_notebook_policy_statement_s3 = iam.PolicyStatement(
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ], 
            resources=[
                "arn:aws:s3:::amazon-braket-*",
                "arn:aws:s3:::braketnotebookcdk-*"
            ]
        )
        
        sagemaker_notebook_policy_statement_cwlogs = iam.PolicyStatement(
            actions=[
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:CreateLogGroup"
            ], 
            resources=[
                "arn:aws:logs:*::log-group:/aws/sagemaker/*"
            ]
        )
        
        sagemaker_notebook_policy_statement_braket = iam.PolicyStatement(
            actions=["braket:*"], 
            resources=["*"]
        )
        
        sagemaker_notebook_policy_doc.add_statements(sagemaker_notebook_policy_statement_s3)
        sagemaker_notebook_policy_doc.add_statements(sagemaker_notebook_policy_statement_cwlogs)
        sagemaker_notebook_policy_doc.add_statements(sagemaker_notebook_policy_statement_braket)
        
        braket_notebook_policy = iam.Policy(
            self, id="AmazonBraketServiceSageMakerNotebookPolicy", 
            document=sagemaker_notebook_policy_doc, 
            roles=[braket_notebook_role], 
            policy_name="AmazonBraketServiceSageMakerNotebookPolicy"
        )
        
        
        # Create IAM Policy to disable QPU
        braket_disable_qpu_policy_doc = iam.PolicyDocument()
        
        braket_disable_qpu_allow_read_only_tasks = iam.PolicyStatement(
            sid="ExplicitAllowReadOnlyActionsOnAllTasks", 
            actions=[
                "braket:GetQuantumTask",
                "braket:ListTagsForResource"
            ], 
            resources=["arn:aws:braket:*:*:quantum-task/*"]
        )
        
        braket_disable_qpu_allow_read_only_resources = iam.PolicyStatement(
            sid="ExplicitAllowReadOnlyActionsOnAllResources", 
            actions=[
                "braket:GetDevice",
                "braket:SearchDevices",
                "braket:SearchQuantumTasks"
            ], 
            resources=["*"]
        )
        
        braket_disable_qpu_deny_create_task = iam.PolicyStatement(
            sid="ExplicitDenyCreateQuantumTask", 
            effect=iam.Effect.DENY, 
            actions=[
                "braket:CreateQuantumTask"
            ], 
            resources=["arn:aws:braket::*:device/qpu/*"]
        )
        
        braket_disable_qpu_policy_doc.add_statements(braket_disable_qpu_allow_read_only_tasks)
        braket_disable_qpu_policy_doc.add_statements(braket_disable_qpu_allow_read_only_resources)
        braket_disable_qpu_policy_doc.add_statements(braket_disable_qpu_deny_create_task)
        
        disable_qpu = bool(self.node.try_get_context("disable_qpu"))
        if disable_qpu: 
            # Attatch the Disable QPU Policy to the IAM Role
            braket_disable_qpu_policy = iam.Policy(
                self, id="AmazonBraketDisableQPUPolicy", 
                document=braket_disable_qpu_policy_doc, 
                roles=[braket_notebook_role], 
                policy_name="AmazonBraketDisableQPUPolicy"
            )