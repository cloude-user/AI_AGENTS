#backend image_scanning_configuration

terraform {
  backend "s3" {
    bucket = "sundeep43-cloud-terraform43"
    key = "terraform/ai_agents/email_agent_ecr.tfstate"
    region = "us-east-2"
  }
}