variable "aws_region" {
  type    = string
  default = "us-east-1"
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

variable "gmail_token"{

} 
variable "gmail_refresh_token {

}
variable "gmail_client_id {

}
variable "gmail_client_secret {

}
variable "ecr_uri" {

}
