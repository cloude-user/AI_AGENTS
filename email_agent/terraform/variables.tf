variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "schedule_expression" {
  description = "Cron schedule for Lambda"
  type        = string
  default     = "rate(1 day)"
}
