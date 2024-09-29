# Terraform Tutorial

After installing the terraform, `brew install terraform`, you can define the `providers.tf` that we will be using it contains the information about the which provider we are going to use and its region, credentials and profile. And also contain declaration of terraform
```hcl
# terraform providers
terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws" 
        }
    }
}

provider "aws" {
    region = "ap-south-1"
    shared_credentials_files = ["~/.aws/credentials"]  
    profile = <profile>
}
```

you can start a project using the below command.
```bash
$ terraform init
```
This will create a `terraform.lock.hcl` file, this is helpful to reproduce the tf environment.

### Creating Resources

To create resource we need to define it in the `main.tf`. We can use any name for the resource but it should be unique.
```hcl
resource "aws_vpc" "mnk_vpc" {
    cidr_block = "10.123.0.0/16"  # CIDR block for the VPC. - A range of IP addresses that are used to identify a network or subnet.
    enable_dns_hostnames = true  # Enables DNS hostnames in the VPC. 
    enable_dns_support = true

    tags = {
        name = "dev"
    }
}
```

To view the plan of the resources, we need to use the below command
```bash
$ terraform plan
```


After defining a resource, you can see its output by using the below command.
```bash
$ terraform apply -auto-approve
```

### Destroying Resources

To destroy resources we need to use the below command.
```bash
$ terraform destroy -auto-approve
```

### Applying Changes

If you have made any changes in the `main.tf` file, then you can apply it by using the below command.
```bash
$ terraform apply -auto-approve
```

### View State
To show the state of the specific resource, we should use the below command 
```bash
$ terraform state show <resource>.<uid>
```

### Format the code
The below command will format the terraform code.
```bash
$ terraform fmt
```

### Replace the service
You may want to replace any services because simply applying through `terraform apply` wont work if there is not change in state (this is the case if any `provisioner` is added, so you may need to replace it). For that we can use the below command 
```bash
$ terraform apply -replace <resource>.<uid>
```

### Console
Opens a managed shell in your terminal. This is very helpful when you want to check the output of any resource.
```bash
$ terraform console
```

To overwrite variables
```bash
$ terraform console -var="host_os=ubuntu"
```

To overwrite variable file to use `(.tfvar)`
```bash
$ terraform console -var-file="<file>.tfvars"
```