variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "lambda_role_name" {
  type    = string
  default = "gmail-agent-lambda-role"
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

# Fixed: Missing closing quote
variable "gmail_token" {
  type      = string
  sensitive = true
}

# Fixed: Missing closing quote
variable "gmail_refresh_token" {
  type      = string
  sensitive = true
}

# Fixed: Missing closing quote
variable "gmail_client_id" {
  type      = string
  sensitive = true
}

# Fixed: Missing closing quote
variable "gmail_client_secret" {
  type      = string
  sensitive = true
}

variable "ecr_uri" {
  type = string
}

variable "gmail_json_token" {
  type    = string
  default = ""
}
