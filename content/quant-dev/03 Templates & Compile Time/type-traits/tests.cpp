#include "qtest.h"
#include "attempt.cpp"
#include <string>
#include <type_traits>

EXAMPLE("Example 1: IsSame, RemoveConst, RemoveReference") {
  CHECK((IsSame_v<int, int>));
  CHECK((!IsSame_v<int, const int>));
  CHECK((std::is_same_v<RemoveConst_t<const double>, double>));
  CHECK((std::is_same_v<RemoveReference_t<std::string&&>, std::string>));
}

EXAMPLE("Example 2: IsPointer and Conditional") {
  CHECK(IsPointer_v<int*>);
  CHECK(!IsPointer_v<int>);
  CHECK((std::is_same_v<Conditional_t<true, int, double>, int>));
  CHECK((std::is_same_v<Conditional_t<false, int, double>, double>));
}

CASE("IsSame distinguishes cv, references and similar types") {
  CHECK((IsSame<double, double>::value));
  CHECK((!IsSame<int, long>::value));
  CHECK((!IsSame<int, int&>::value));
  CHECK((!IsSame<int*, const int*>::value));
  CHECK((IsSame_v<std::string, std::basic_string<char>>));
  CHECK((!IsSame_v<char, signed char>));
}

CASE("RemoveConst removes only top-level const") {
  CHECK((std::is_same_v<RemoveConst<const int>::type, int>));
  CHECK((std::is_same_v<RemoveConst_t<int>, int>));
  CHECK((std::is_same_v<RemoveConst_t<const int*>, const int*>));
  CHECK((std::is_same_v<RemoveConst_t<int* const>, int*>));
  CHECK((std::is_same_v<RemoveConst_t<const volatile int>, volatile int>));
  CHECK((std::is_same_v<RemoveConst_t<const int&>, const int&>));
}

CASE("RemoveReference strips lvalue and rvalue references") {
  CHECK((std::is_same_v<RemoveReference<int&>::type, int>));
  CHECK((std::is_same_v<RemoveReference_t<int&&>, int>));
  CHECK((std::is_same_v<RemoveReference_t<int>, int>));
  CHECK((std::is_same_v<RemoveReference_t<const int&>, const int>));
  CHECK((std::is_same_v<RemoveReference_t<int*&>, int*>));
}

CASE("IsPointer handles cv-qualified pointers") {
  CHECK(IsPointer<double*>::value);
  CHECK(IsPointer_v<const int*>);
  CHECK(IsPointer_v<int* const>);
  CHECK(IsPointer_v<int* volatile>);
  CHECK(IsPointer_v<int* const volatile>);
  CHECK(IsPointer_v<int**>);
  CHECK(IsPointer_v<void (*)(int)>);
}

CASE("IsPointer is false for non-pointers") {
  CHECK(!IsPointer_v<int&>);
  CHECK(!IsPointer_v<int*&>);
  CHECK(!IsPointer_v<int[4]>);
  CHECK(!IsPointer_v<std::string>);
  CHECK(!IsPointer_v<std::nullptr_t>);
}

CASE("Conditional picks a branch") {
  CHECK((std::is_same_v<Conditional<true, char, long>::type, char>));
  CHECK((std::is_same_v<Conditional<false, char, long>::type, long>));
  CHECK((std::is_same_v<Conditional_t<sizeof(int) == 4, int, long>, int>));
  CHECK((std::is_same_v<Conditional_t<false, void, int&>, int&>));
}

CASE("traits compose") {
  using T = RemoveConst_t<RemoveReference_t<const std::string&>>;
  CHECK((IsSame_v<T, std::string>));
  CHECK((!IsSame_v<RemoveReference_t<const int&>, int>));
  CHECK((IsSame_v<Conditional_t<IsPointer_v<int*>, long, short>, long>));
  CHECK((IsSame_v<Conditional_t<IsSame_v<int, float>, long, short>, short>));
}
