/*
 * Python wrapper for CAP_NET_RAW capability
 * Based on solution from here: https://stackoverflow.com/a/67733220/11442904
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/capability.h>
#include <sys/prctl.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  cap_iab_t iab = cap_iab_from_text("^cap_net_raw");
  if (iab == NULL) {
    perror("iab not parsed");
    exit(1);
  }
  if (cap_iab_set_proc(iab)) {
    perror("unable to set iab");
    exit(1);
  }
  cap_free(iab);

  // CAP_NET_RAW capability is already set, proceed to execute 'python' with
  // provided arguments
  execvp("python", argv);
  perror("execvp");
  return 1;
}
