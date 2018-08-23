#include <stdint.h>
#include <stdbool.h>

int32_t
f2_more_additions(int32_t a, int32_t b, int32_t c, int32_t d, bool selector)
{
  int result;

  if (selector)
    result = a + b;
  else
    result = a + b + c + d;

  return result;
}
