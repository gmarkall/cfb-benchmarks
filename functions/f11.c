#include <stdint.h>
#include <stdbool.h>

int32_t
f11_double_nesting(int32_t a, int32_t b, int32_t c, bool selector1, bool selector2, bool selector3)
{
  int result = 0;

  if (selector1) {
    result = a + b;
    if (selector2) {
      result += c;
      if (selector3)
        result += b * 10;
    }
  }

  return result;
}

