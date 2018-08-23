#include <stdint.h>
#include <stdbool.h>

int work[10];

int32_t
f6_array_load_store(int32_t a, int32_t b, bool selector)
{
  int32_t result;

  if (selector) {
    work[b] = a;
    result = work[a] + b;
  } else {
    result = a + b;
  }

  return result;
}
