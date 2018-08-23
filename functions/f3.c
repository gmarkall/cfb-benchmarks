#include <stdint.h>
#include <stdbool.h>

int32_t
f3_no_else(int32_t a, int32_t b, bool selector)
{
  int result = a;

  if (selector)
    result += b;

  return result;
}
