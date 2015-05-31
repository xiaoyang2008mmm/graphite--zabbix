#!/bin/bash

__create_user() {
# Create a user to SSH into as.
useradd test
SSH_USERPASS=111111
echo -e "$SSH_USERPASS\n$SSH_USERPASS" | (passwd --stdin test)
echo ssh test password: $SSH_USERPASS
}

# Call all functions
__create_user
