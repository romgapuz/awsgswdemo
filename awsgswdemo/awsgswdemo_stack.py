from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_rds as rds,
    core
)

class AwsgswdemoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            cidr="10.10.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="PublicSubnet",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE,
                    name="PrivateSubnet",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="DBSubnet",
                    cidr_mask=24
                )
            ],
            # nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=2,
        )

        self.rds = rds.DatabaseInstance(
            self,
            "RDS",
            instance_identifier="wordpress-db",
            master_username="master",
            master_user_password=core.SecretValue.plain_text("password"),
            database_name="wordpress",
            engine_version="10.4.8",
            engine=rds.DatabaseInstanceEngine.MARIADB,
            vpc=self.vpc,
            vpc_placement={
                "subnet_type": ec2.SubnetType.ISOLATED,
            },
            port=3306,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        self.rds.connections.allow_from(
            ec2.Peer.ipv4("10.10.0.0/16"),
            ec2.Port.tcp(3306),
            "Allow http from internet"
        )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        # Instance
        self.ec2instance = ec2.Instance(self, "Instance",
            instance_name="wordpress",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=amzn_linux,
            vpc=self.vpc,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PUBLIC,
            },
            role=role,
            key_name="oregon"
        )

        self.ec2instance.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            "Allow http from internet"
        )

        self.ec2instance.user_data.add_commands(
            "dbhost=\"" + self.rds.db_instance_endpoint_address + "\"",
            "wordpressdb=\"wordpress\"",
            "SQLUser=\"master\"",
            "SQLPass=\"password\"",
            "yum upgrade -y",
            "yum install -y httpd php php-mysql wget curl",
            "yum upgrade -y httpd php php-mysql wget curl",
            "cd /var/www/html",
            "wget https://wordpress.org/wordpress-5.1.6.tar.gz",
            "tar -xzf wordpress-5.1.6.tar.gz",
            "cd wordpress",
            "mv -f * ../",
            "cd ..",
            "rm -f wordpress-5.1.6.tar.gz",
            "rm -rf ./wordpress",
            "rm -f index.html",
            "WPSalts=$(curl https://api.wordpress.org/secret-key/1.1/salt/)",
            "cat > ./wp-config.php <<-EOF",
            "<?php",
            "define('DB_NAME', '$wordpressdb');",
            "define('DB_USER', '$SQLUser');",
            "define('DB_PASSWORD', '$SQLPass');",
            "define('DB_HOST', '$dbhost');",
            "define('DB_CHARSET', 'utf8');",
            "define('DB_COLLATE', '');",
            "$WPSalts",
            "\\$table_prefix  = 'wp_';",
            "define('WP_DEBUG', false);",
            "if ( !defined('ABSPATH') )",
            "    define('ABSPATH', dirname(__FILE__) . '/');",
            "require_once(ABSPATH . 'wp-settings.php');",
            "EOF",
            "if ! groupadd www",
            "then ",
            "   /usr/sbin/groupadd www",
            "fi",
            "usermod -a -G www apache",
            "chown -R apache /var/www",
            "chgrp -R www /var/www",
            "chmod 2775 /var/www",
            "find /var/www -type d -exec sudo chmod 2775 {} \\;",
            "find /var/www -type f -exec sudo chmod 0664 {} \\;",
            "sed -i -e 's/AllowOverride None/AllowOverride All/g' /etc/httpd/conf/httpd.conf",
            "service httpd start",
            "service mysqld restart",
            "chkconfig httpd on",
            "chkconfig mysqld on"
        )

        core.CfnOutput(
            self,
            "Output",
            value=self.vpc.vpc_id
        )
