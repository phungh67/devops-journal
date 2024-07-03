resource "aws_vpc" "main-vpc" {
  cidr_block = var.vpc-main-cidr
  tags = {
    "Name"      = "${var.name-prefix}-main-vpc"
    "Terraform" = "managed"
    "Default"   = "false"
  }
}

resource "aws_subnet" "public-subnets" {
  vpc_id = aws_vpc.main-vpc.id
  count  = length(var.public-subnet-cidr)
  cidr_block = element(var.public-subnet-cidr, count.index)
  tags = {
    "Name" = "{var.name-prefix}-pub-00${count.index + 1}"
    "Terraform" = "managed"
  }
}
