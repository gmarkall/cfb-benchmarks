#include <stdint.h>
#include <stdbool.h>

int32_t
f8_nested_conditionals(int32_t a, int32_t b, bool selector1, bool selector2)
{
  int result = 0;

  if (selector1) {
    if (selector2)
      result = a / b;
  } else {
    result = a + 3;
  }

  return result;
}
