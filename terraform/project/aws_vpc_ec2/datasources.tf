data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "server_ami" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (ubuntu 24.04 amd64 - ami-0522ab6e1ddcc7055 - will be changing.)

  filter {
    name   = "name" # filter by name
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}