variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "app_version" {
  description = "Application version tag"
  type        = string
  default     = "v1.0.0"
}

variable "replica_count" {
  description = "Number of replicas to run"
  type        = number
  default     = 2
}

variable "enable_monitoring" {
  description = "Whether to enable Prometheus scraping"
  type        = bool
  default     = true
}
