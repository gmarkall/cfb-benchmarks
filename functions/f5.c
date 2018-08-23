#include <stdint.h>
#include <stdbool.h>

int work[10];

int32_t
f5_store_array(int32_t a, int32_t b, bool selector)
{
  int32_t result;

  if (selector) {
    work[b] = a;
    result = b + b;
  } else {
    result = a + b;
  }

  return result;
}
