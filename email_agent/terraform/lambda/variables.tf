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
  default = "{\"token\":\"ya29.A0AS3H6NyF0WPKbOYR_UbROZjHvKtbfyzXwxGZOZdK7O3unx6Rrnd0KJSRvf508Y-m8WgHPnbkEyvSJGlkZWiR1sGBBvHDfNNbfNgUGOQMFEqILo1ynP27uBMC630_6PRwfrFzSrZ36RJAiMZKGJtCd624h0ae0OhmEtg9ua9kMZSjKafOscnUh0RrJ1bA4Nlhf9B34ZoaCgYKAZsSARYSFQHGX2MiDZQaRHbDU0doryFdSr0bvA0206\",\"refresh_token\":\"1//0ggbHHNjfWegnCgYIARAAGBASNwF-L9Irdz8ESESYFA9SkSn1YSBlPOguIji-9X_ZVK8Gf7UYV1JV8WXIKv2jtoRakjJrEeH7VfU\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"client_id\":\"670645107880-5v1ghj5o05msm5n51vagg7b1tk799jqf.apps.googleusercontent.com\",\"client_secret\":\"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\",\"scopes\":[\"https://www.googleapis.com/auth/gmail.modify\"],\"universe_domain\":\"googleapis.com\",\"account\":\"\",\"expiry\":\"2025-08-02T10:19:10Z\"}"
}
