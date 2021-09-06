import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="braket_workshop_cdk",
    version="0.0.2",

    description="A CDK Python app to create IAM User/Role for Amazon Braket Workshop",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Yoshitaka Haribara",

    package_dir={"": "braket_workshop_cdk"},
    packages=setuptools.find_packages(where="braket_workshop_cdk"),

    install_requires=[
        "aws-cdk.core==1.103.0",
        "aws-cdk.aws_iam==1.103.0",
        "aws-cdk.aws_secretsmanager==1.103.0",
        "aws-cdk.aws_s3==1.103.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
