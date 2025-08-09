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

variable "GMAIL_TOKEN"{

} 
variable "GMAIL_REFRESH_TOKEN" {

}
variable "GMAIL_CLIENT_ID" {

}
variable "GMAIL_CLIENT_SECRET " {

}
variable "ecr_uri" {
  
}
