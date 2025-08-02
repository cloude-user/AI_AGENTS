terraform {
  backend "s3" {
    bucket = "sundeep43-cloud-terraform43"
    key = "terraform/ai_agents/email_agent.tfstate"
    region = "us-east-2"
    encrypt = true
    use_lockfile = true
  }
}