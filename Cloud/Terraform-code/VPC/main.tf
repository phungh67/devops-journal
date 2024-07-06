resource "aws_vpc" "main-vpc" {
  cidr_block = var.vpc-main-cidr
  tags = {
    "Name"      = "${var.name-prefix}-main-vpc"
    "Terraform" = "managed"
    "Default"   = "false"
  }
}

resource "aws_subnet" "public-subnets" {
  vpc_id            = aws_vpc.main-vpc.id
  count             = length(var.public-subnet-cidr)
  cidr_block        = element(var.public-subnet-cidr, count.index)
  availability_zone = element(var.az-list, count.index)
  tags = {
    "Name"      = "${var.name-prefix}-pub-00${count.index + 1}"
    "Terraform" = "managed"
  }
}

resource "aws_subnet" "private-subnets" {
  vpc_id            = aws_vpc.main-vpc.id
  count             = length(var.private-subnet-cidr)
  cidr_block        = element(var.private-subnet-cidr, count.index)
  availability_zone = element(var.az-list, count.index)
  tags = {
    "Name"      = "${var.name-prefix}-pri-00${count.index + 1}"
    "Terraform" = "managed"
  }
}

resource "aws_internet_gateway" "main-gw" {
  vpc_id = aws_vpc.main-vpc.id
  tags = {
    "Name"      = "${var.name-prefix}-main-gw"
    "Terraform" = "managed"
  }
}

resource "aws_eip" "main-nat-eip" {
  domain = "vpc"
  tags = {
    "Name"      = "${var.name-prefix}-nat-eip"
    "Terraform" = "managed"
  }
}

resource "aws_nat_gateway" "main-nat-gw" {
  allocation_id = aws_eip.main-nat-eip.id
  subnet_id     = aws_subnet.public-subnets[0]
  tags = {
    "Name"      = "${var.name-prefix}-main-nat-gw"
    "Terraform" = "managed"
  }
  depends_on = [aws_vpc.main-vpc, aws_subnet.public-subnets]
}

resource "aws_route_table" "pub-route-table" {
  vpc_id = aws_vpc.main-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main-gw.id
  }
  tags = {
    "Name"      = "${var.name-prefix}-public-route-table"
    "Terraform" = "managed"
  }
}

resource "aws_route_table_association" "public-rtb-association" {
  count          = length(var.public-subnet-cidr)
  subnet_id      = element(aws_subnet.public-subnets[*].id, count.index)
  route_table_id = aws_route_table.pub-route-table.id
}

resource "aws_route_table" "pri-route-table" {
  vpc_id = aws_vpc.main-vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main-nat-gw.id
  }
  tags = {
    "Name"      = "${var.name-prefix}-private-route-table"
    "Terraform" = "managed"
  }
}
resource "aws_route_table_association" "private-rtb-association" {
  count          = length(var.private-subnet-cidr)
  subnet_id      = element(aws_subnet.private-subnets[*].id, count.index)
  route_table_id = aws_route_table.pri-route-table.id
}

