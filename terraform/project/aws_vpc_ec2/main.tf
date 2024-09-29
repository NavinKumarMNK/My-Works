resource "aws_vpc" "mnk_vpc" {
  cidr_block           = "10.123.0.0/16" # CIDR block for the VPC. - A range of IP addresses that are used to identify a network or subnet.
  enable_dns_hostnames = true            # Enables DNS hostnames in the VPC. 
  enable_dns_support   = true

  tags = {
    name = "dev"
  }
}

resource "aws_subnet" "mnk_public_subnet" {
  vpc_id                  = aws_vpc.mnk_vpc.id # terraform state show aws_vpc.mnk_vpc | grep "\bid"
  cidr_block              = "10.123.1.0/24"    # one of the subnets within the VPC.
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]

  tags = {
    name = "dev-public"
  }
}

resource "aws_internet_gateway" "mnk_igw" {
  vpc_id = aws_vpc.mnk_vpc.id

  tags = {
    name = "dev-igw"
  }
}

resource "aws_route_table" "mnk_public_rt" {
  vpc_id = aws_vpc.mnk_vpc.id

  tags = {
    name = "dev_public_rt"
  }
}

resource "aws_route" "default_route" {
  # This is a route, we need defined the table, gateway, and the cidr block.
  route_table_id         = aws_route_table.mnk_public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mnk_igw.id
}

resource "aws_route_table_association" "mnk_public_assoc" {
  subnet_id      = aws_subnet.mnk_public_subnet.id
  route_table_id = aws_route_table.mnk_public_rt.id
}

resource "aws_security_group" "mnk_sg" {
  name        = "dev-sg"
  description = "dev security group"
  vpc_id      = aws_vpc.mnk_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # accept connection from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # allow all outbound connections
  }

  tags = {
    name = "dev-sg"
  }
}

resource "aws_key_pair" "mnk_dev_auth" {
  key_name   = "mnk_aws"
  public_key = file("~/.ssh/mnk_aws.pub")
}

resource "aws_instance" "dev_node" {
  instance_type = "t2.micro"
  ami           = data.aws_ami.server_ami.id

  tags = {
    name = "dev-node"
  }

  key_name               = aws_key_pair.mnk_dev_auth.id
  vpc_security_group_ids = [aws_security_group.mnk_sg.id]
  subnet_id              = aws_subnet.mnk_public_subnet.id
  user_data              = file("./userdata.tpl")

  root_block_device { # ebs volume
    volume_size = 8 # size of the volume in GBs
  }

  # provisioner will not be detected as differences in the state
  provisioner "local-exec" {
    command = templatefile("${var.host_os}-ssh-config.tpl", {
      hostname     = "${self.public_ip}",
      user         = "ubuntu",
      identityfile = "~/.ssh/mnk_aws" # private key
    })
    interpreter = var.host_os == "windows" ? ["Powershell", "-Command"] : ["bash", "-c"]
  }
}
