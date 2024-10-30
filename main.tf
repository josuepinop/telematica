provider "aws" {
  region = "us-east-1"  # Cambia a la región que desees
}
resource "aws_key_pair" "terraform_key" {
  key_name = "id_rsa"
  public_key = file("~/.ssh/id_rsa.pub")
}
resource "aws_instance" "my_instance" {
  ami           = "ami-005fc0f236362e99f"  # Reemplaza con una AMI válida en tu región
  instance_type = "t2.micro"  # Tipo de instancia
  key_name      = "id_rsa"  # Reemplaza con el nombre de tu clave SSH
  security_groups = [aws_security_group.allow_http.name]
  user_data = <<-EOF
              #!/bin/bash
              chmod +x /tmp/install.sh
              /tmp/install.sh
              EOF
  tags = {
    Name = "MyEC2Instance"
  }
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP traffic"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Permitir acceso desde cualquier IP
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Permitir todo el tráfico de salida
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "null_resource" "provision" {
  depends_on = [aws_instance.my_instance]
  provisioner "file" {
    source      = "./install.sh"  # Ruta local al archivo install.sh
    destination = "/tmp/install.sh"
    connection {
      type        = "ssh"
      user        = "ubuntu"  # Cambia según el tipo de AMI (ej. "ubuntu", "centos", etc.)
      private_key = file("~/.ssh/id_rsa")  # Ruta a tu clave privada
      host        = aws_instance.my_instance.public_ip
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install.sh",
      "/tmp/install.sh"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"  # Cambia según el tipo de AMI
      private_key = file("~/.ssh/id_rsa")  # Ruta a tu clave privada
      host        = aws_instance.my_instance.public_ip
    }
  }
}
  
