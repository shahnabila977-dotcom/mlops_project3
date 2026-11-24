resource "local_file" "cluster_env" {
  filename = "${path.module}/cluster.env"
  content  = <<-EOT
    PROJECT_NAME=${var.project_name}
    KUBECONFIG_PATH=${var.kubeconfig_path}
    REPLICA_COUNT=${var.replica_count}
  EOT
}
