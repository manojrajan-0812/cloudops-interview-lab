terraform {
  backend "gcs" {
    bucket = "interview-lab-tfstate"
    prefix = "interview-api/state"
  }
}
