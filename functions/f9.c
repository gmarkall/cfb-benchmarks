#include <stdint.h>
#include <stdbool.h>

int32_t
f9_nested_code(int32_t a, int32_t b, int32_t c, bool selector1, bool selector2)
{
  int result;

  if (selector1) {
    result = a + b;
    if (selector2)
      result += c;
  } else {
    result = a + 3;
  }

  return result;
}
