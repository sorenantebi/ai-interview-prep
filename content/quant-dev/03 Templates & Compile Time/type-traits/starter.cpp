template <class T, class U>
struct IsSame {
    static constexpr bool value = false;
};

template <class T>
struct RemoveConst {
    using type = T;
};

template <class T>
struct RemoveReference {
    using type = T;
};

template <class T>
struct IsPointer {
    static constexpr bool value = false;
};

template <bool B, class T, class F>
struct Conditional {
    using type = T;
};

template <class T, class U> inline constexpr bool IsSame_v = IsSame<T, U>::value;
template <class T> using RemoveConst_t = typename RemoveConst<T>::type;
template <class T> using RemoveReference_t = typename RemoveReference<T>::type;
template <class T> inline constexpr bool IsPointer_v = IsPointer<T>::value;
template <bool B, class T, class F> using Conditional_t = typename Conditional<B, T, F>::type;
