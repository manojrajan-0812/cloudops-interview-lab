output "deploy_id" {
  description = "Stable deployment identifier"
  value       = random_string.deploy_id.result
}

output "config_file" {
  description = "Path to generated app config"
  value       = local_file.app_config.filename
}
