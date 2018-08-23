#include <stdint.h>
#include <stdbool.h>

int work[10];

int32_t
f7_load_store_branches(int32_t a, int32_t b, bool selector)
{
  int32_t result;

  if (selector) {
    result = work[a] + b;
  } else {
    work[b] = a;
    result = a + b;
  }

  return result;
}

