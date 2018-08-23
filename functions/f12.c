#include <stdint.h>
#include <stdbool.h>

int32_t
f12_nesting_levels(int32_t a, int32_t b, int32_t c, bool selector1, bool selector2, bool selector3, bool selector4)
{
  int result;

  if (selector1) {
    result = a + b;
    if (selector2) {
      result += c;
      if (selector3)
        result += b * 10;
    }
  } else {
    result = a - b;
    if (selector4) {
      result -= c;
    }
  }

  return result;
}
