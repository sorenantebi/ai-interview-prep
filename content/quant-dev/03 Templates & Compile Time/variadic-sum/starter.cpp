#include <cstddef>
#include <sstream>
#include <string>
#include <string_view>

template <class... Ts>
constexpr auto sum(Ts... args) {
    return 0;
}

template <class... Ts>
constexpr std::size_t count_args(const Ts&... args) {
    return 0;
}

template <class... Ts>
constexpr bool all_true(Ts... args) {
    return false;
}

template <class... Ts>
std::string join(std::string_view sep, const Ts&... args) {
    return "";
}
