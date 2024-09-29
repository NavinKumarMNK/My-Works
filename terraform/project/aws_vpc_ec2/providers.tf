# terraform providers
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws" # like an import
    }
  }
}

provider "aws" {
  region                   = "ap-south-1"
  shared_credentials_files = ["~/.aws/mnk_credentials"] # import the credentials file
  profile                  = "navinkumar"
}
