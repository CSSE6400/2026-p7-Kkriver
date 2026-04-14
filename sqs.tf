terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  shared_credentials_files = ["./credentials"]
}

resource "aws_sqs_queue" "ical_queue" {
  name = "ical"
}

output "ical_queue_url" {
  value = aws_sqs_queue.ical_queue.url
}
