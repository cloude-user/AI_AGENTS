output "lambda_function_name" {
  value = aws_lambda_function.email_cleaner.function_name
}

output "lambda_role" {
  value = aws_iam_role.lambda_exec_role.arn
}
