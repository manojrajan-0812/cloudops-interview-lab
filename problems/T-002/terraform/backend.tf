terraform {
  # BUG: local backend — state lives on each engineer's laptop.
  # No locking = concurrent applies corrupt state.
  # No sharing = team members can't see current state.
  backend "local" {
    path = "terraform.tfstate"
  }
}
