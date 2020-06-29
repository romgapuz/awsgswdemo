
# AWS Getting Started Workshop Demo

This sample app deploys a wordpress site running on Amazon EC2 and backed by MariaDB on Amazon RDS. This app uses AWS Cloud Development Kit (AWS CDK) to deploy the sample app.

When you run ```cdk deploy``` it deploys the following:

- VPC with 3 subnets (Public, Private and DB)
- Wordpress on an EC2 instance in the Public subnet
- MariaDB database on Amazon RDS

The EC2 instance is created in the public subnet intentionally so that the user can use it to demo the implementation of Auto Scaling Group and Elastic Load Balancer for high-availability setup.

NOTE: There are still hard-coded parameters (until I can clean it up) that you need to be aware, see below:

- Region in ```app.py```
- CIDR in ```awsgswdemo/awsgswdemo_stack.py```
- Key pair name in ```awsgswdemo/awsgswdemo_stack.py```
- Password in ```awsgswdemo/awsgswdemo_stack.py```

---


The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .env directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!