#include <stdint.h>
#include <stdbool.h>

int32_t
f1_simple_conditional(int32_t a, int32_t b, bool selector)
{
  int result;

  if (selector)
    result = a / b;
  else
    result = a + 3;

  return result;
}
