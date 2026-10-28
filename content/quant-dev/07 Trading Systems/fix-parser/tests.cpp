#include "qtest.h"
#include "attempt.cpp"
#include <cstdio>
#include <ostream>
#include <random>

std::ostream& operator<<(std::ostream& o, FixError e) {
  const char* names[] = {"Ok", "Malformed", "BadBodyLength", "BadChecksum"};
  return o << names[static_cast<int>(e)];
}

// '|' -> SOH, so test messages stay readable.
static std::string soh(std::string s) {
  for (char& c : s) if (c == '|') c = '\x01';
  return s;
}

// Builds a valid message around a body like "35=D|55=ABC|": computes 9 and 10.
static std::string build(const std::string& body, const std::string& begin = "FIX.4.4") {
  std::string b = soh(body);
  std::string m = soh("8=" + begin + "|9=" + std::to_string(b.size()) + "|") + b;
  unsigned sum = 0;
  for (unsigned char c : m) sum += c;
  char cs[8];
  std::snprintf(cs, sizeof cs, "%03u", sum % 256);
  return m + soh("10=" + std::string(cs) + "|");
}

EXAMPLE("Example 1: a new order single") {
  std::string msg = soh("8=FIX.4.4|9=57|35=D|49=ALPHA|56=XCHG|11=ord1|55=ABC|54=1|38=100|44=25.5|10=216|");
  ParseResult r = parse_fix(msg);
  CHECK_EQ(r.error, FixError::Ok);
  CHECK_EQ(r.message.msg_type(), std::string("D"));
  CHECK_EQ(r.message.get(55), std::optional<std::string>("ABC"));
  CHECK_EQ(r.message.get(44), std::optional<std::string>("25.5"));
  CHECK(!r.message.get(99).has_value());
  CHECK_EQ(r.message.fields.size(), 11u);
}

EXAMPLE("Example 2: heartbeat, wrong length, wrong checksum, missing SOH") {
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=163|")).error, FixError::Ok);
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=6|35=0|10=163|")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=164|")).error, FixError::BadChecksum);
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=163")).error, FixError::Malformed);
}

CASE("fields keep wire order, duplicates, and '=' inside values") {
  std::string m = build("35=8|58=a=b|448=P1|448=P2|");
  ParseResult r = parse_fix(m);
  CHECK_EQ(r.error, FixError::Ok);
  std::vector<std::pair<int, std::string>> expect = {
      {8, "FIX.4.4"}, {9, "26"}, {35, "8"}, {58, "a=b"}, {448, "P1"}, {448, "P2"}};
  CHECK_EQ(r.message.fields.size(), 7u);
  for (std::size_t i = 0; i < expect.size(); ++i) CHECK_EQ(r.message.fields[i], expect[i]);
  CHECK_EQ(r.message.fields[6].first, 10);
  CHECK_EQ(r.message.get(448), std::optional<std::string>("P1"));
  CHECK_EQ(r.message.get(58), std::optional<std::string>("a=b"));
}

CASE("the helper's messages parse for many bodies") {
  for (int i = 0; i < 200; ++i) {
    std::string body = "35=" + std::string(1, static_cast<char>('A' + i % 26)) + "|";
    for (int k = 0; k < i % 7; ++k) body += std::to_string(100 + k) + "=v" + std::to_string(i * k) + "|";
    ParseResult r = parse_fix(build(body, i % 2 ? "FIXT.1.1" : "FIX.4.2"));
    CHECK_EQ(r.error, FixError::Ok);
    CHECK_EQ(r.message.msg_type(), std::string(1, static_cast<char>('A' + i % 26)));
    CHECK_EQ(r.message.fields.size(), static_cast<std::size_t>(4 + i % 7));
  }
}

CASE("structural errors are Malformed") {
  const char* bad[] = {
      "",
      "|",
      "8=FIX.4.4|9=5|35=0|10=163||",          // empty field
      "8=FIX.4.4|9=5|35=0|10163|",            // no '='
      "8=FIX.4.4|9=5|=0|10=163|",             // empty tag
      "8=FIX.4.4|9=5|35=|10=163|",            // empty value
      "8=FIX.4.4|9=5|3a=0|10=163|",           // non-digit tag
      "8=FIX.4.4|9=5|035=0|10=163|",          // leading zero
      "8=FIX.4.4|9=5|35=0|1234567890=x|10=163|",  // tag too long
      "9=5|8=FIX.4.4|35=0|10=163|",           // wrong order
      "8=FIX.4.4|9=5|49=X|35=0|10=163|",      // 35 not third
      "8=FIX.4.4|9=5|35=0|55=X|",             // no checksum
      "8=FIX.4.4|9=5|35=0|10=111|55=X|10=163|",  // 10 twice
      "8=FIX.4.4|9=5|35=0|9=5|10=163|",       // 9 twice
      "8=FIX.4.4|9=5|10=163|",                // too few fields
  };
  for (const char* s : bad) CHECK_EQ(parse_fix(soh(s)).error, FixError::Malformed);
}

CASE("body length errors, including non-numeric lengths") {
  std::string good = build("35=D|55=XYZ|");
  CHECK_EQ(parse_fix(good).error, FixError::Ok);
  // rebuild with a wrong 9 but a checksum that matches the wrong text, so only the length is wrong
  auto with_len = [](const std::string& len) {
    std::string m = soh("8=FIX.4.4|9=" + len + "|35=D|55=XYZ|");
    unsigned sum = 0;
    for (unsigned char c : m) sum += c;
    char cs[8];
    std::snprintf(cs, sizeof cs, "%03u", sum % 256);
    return m + soh("10=" + std::string(cs) + "|");
  };
  CHECK_EQ(parse_fix(with_len("12")).error, FixError::Ok);
  CHECK_EQ(parse_fix(with_len("11")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(with_len("13")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(with_len("1x")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(with_len("-12")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(with_len("99999999999999999999")).error, FixError::BadBodyLength);
  CHECK_EQ(parse_fix(with_len("012")).error, FixError::Ok);  // leading zeros in a value are fine
}

CASE("checksum must be exactly three digits and correct") {
  std::string good = build("35=0|");
  CHECK_EQ(good, soh("8=FIX.4.4|9=5|35=0|10=163|"));
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=0163|")).error, FixError::BadChecksum);
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=63|")).error, FixError::BadChecksum);
  CHECK_EQ(parse_fix(soh("8=FIX.4.4|9=5|35=0|10=1a3|")).error, FixError::BadChecksum);
  // high bytes must be summed as unsigned
  std::string hi = build("35=D|58=\xC3\xA9\xFF|");
  CHECK_EQ(parse_fix(hi).error, FixError::Ok);
}

CASE("any single corrupted byte of a valid message is rejected") {
  std::mt19937 rng(5);
  std::string good = build("35=D|49=ALPHA|56=XCHG|11=ord1|55=ABC|54=1|38=100|44=25.5|");
  CHECK_EQ(parse_fix(good).error, FixError::Ok);
  for (std::size_t i = 0; i < good.size(); ++i) {
    for (int k = 0; k < 4; ++k) {
      std::string m = good;
      char c = static_cast<char>(std::uniform_int_distribution<int>(0, 255)(rng));
      if (c == m[i]) continue;
      m[i] = c;
      CHECK(parse_fix(m).error != FixError::Ok);
    }
    CHECK(parse_fix(std::string_view(good).substr(0, i)).error != FixError::Ok);  // truncations too
  }
}

CASE("a 60 KB message parses quickly, 200 times") {
  std::string body = "35=W|";
  while (body.size() < 60000) body += "270=12345.678|271=1000|";
  std::string m = build(body);
  for (int i = 0; i < 200; ++i) {
    ParseResult r = parse_fix(m);
    CHECK_EQ(r.error, FixError::Ok);
    CHECK_EQ(r.message.msg_type(), std::string("W"));
  }
}
