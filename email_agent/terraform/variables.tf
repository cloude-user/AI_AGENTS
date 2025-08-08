variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "lambda_role_name" {
  type    = string
  default = "gmail-agent-lambda-role"
}

variable "ecr_repo_name" {
  type    = string
  default = "gmail-agent"
}

# Image tag variable (can be set via TF_VAR_image_tag or pipeline)
variable "image_tag" {
  type    = string
  default = "latest"
}

variable "openai_api_key" {
  type      = string
  sensitive = true
  default   = ""
}
