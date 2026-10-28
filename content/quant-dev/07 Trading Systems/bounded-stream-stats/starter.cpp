#include <cstdint>
#include <optional>
#include <stdexcept>
#include <vector>

class BoundedStats {
public:
    BoundedStats(int lo, int hi) {}

    void add(int x) {}

    std::uint64_t count() const { return 0; }

    std::optional<int> percentile(double p) const { return std::nullopt; }

    std::optional<double> median() const { return std::nullopt; }

    std::optional<int> mode() const { return std::nullopt; }
};
