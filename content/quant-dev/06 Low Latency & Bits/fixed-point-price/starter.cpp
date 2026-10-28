#include <compare>
#include <cstdint>
#include <string>

class Price {
public:
    static constexpr std::int64_t kScale = 10000;

    constexpr Price() = default;
    static constexpr Price from_ticks(std::int64_t ticks) { return Price(); }
    static Price from_double(double value) { return Price(); }
    constexpr std::int64_t ticks() const { return 0; }
    double to_double() const { return 0.0; }
    std::string to_string() const { return ""; }

    constexpr Price operator+(Price other) const { return Price(); }
    constexpr Price operator-(Price other) const { return Price(); }
    constexpr Price operator*(std::int64_t qty) const { return Price(); }

    constexpr bool operator==(const Price&) const { return false; }
    constexpr std::strong_ordering operator<=>(const Price&) const { return std::strong_ordering::equal; }

private:
    std::int64_t ticks_ = 0;
};
