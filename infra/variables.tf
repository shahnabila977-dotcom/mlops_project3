variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "k8s-mlops-project"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "replica_count" {
  description = "Number of replicas for deployment (3-5)"
  type        = number
  default     = 3
}
