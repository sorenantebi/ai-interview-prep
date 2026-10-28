#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

enum class FixError { Ok, Malformed, BadBodyLength, BadChecksum };

struct FixMessage {
    std::vector<std::pair<int, std::string>> fields;
    std::optional<std::string> get(int tag) const { return std::nullopt; }
    std::string msg_type() const { return ""; }
};

struct ParseResult {
    FixError error;
    FixMessage message;
};

ParseResult parse_fix(std::string_view raw) { return {FixError::Ok, {}}; }
