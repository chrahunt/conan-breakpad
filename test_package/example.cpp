#ifndef __linux__
#error "Only Linux is supported"
#endif

#include "client/linux/handler/exception_handler.h"
#include "common/linux/http_upload.h"

static bool dumpCallback(const google_breakpad::MinidumpDescriptor& descriptor,
void* context, bool succeeded) {
  printf("Dump path: %s\n", descriptor.path());
  // Without this, the message wasn't getting seen by our check in
  // the conanfile.
  fflush(stdout);
  return succeeded;
}

void crash() { volatile int* a = (int*)(NULL); *a = 1; }

int main(int argc, char* argv[]) {
  google_breakpad::MinidumpDescriptor descriptor("/tmp");
  google_breakpad::ExceptionHandler eh(descriptor, NULL, dumpCallback, NULL, true, -1);
  crash();
  return 0;
}
