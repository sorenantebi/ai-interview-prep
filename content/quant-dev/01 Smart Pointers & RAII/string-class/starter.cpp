#include <cstddef>
#include <cstring>
#include <utility>

class String {
public:
    String() {}
    String(const char* s) {}
    String(const String& other) {}
    String(String&& other) noexcept {}
    String& operator=(const String& other) { return *this; }
    String& operator=(String&& other) noexcept { return *this; }
    ~String() {}

    std::size_t size() const noexcept { return 0; }
    const char* c_str() const noexcept { return ""; }
    String& operator+=(const String& other) { return *this; }

    friend bool operator==(const String& a, const String& b) noexcept { return false; }
};
