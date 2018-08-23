#include <stdint.h>
#include <stdbool.h>

int32_t
f10_nesting_both(int32_t a, int32_t b, int32_t c, bool selector1, bool selector2, bool selector3)
{
  int result;

  if (selector1) {
    result = a + b;
    if (selector2)
      result += c;
  } else {
    result = a + 3;
    if (selector3)
      result *= b;
  }

  return result;
}

