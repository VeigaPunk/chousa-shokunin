command() {
  case " $* " in
    *" --version "*) builtin command "$@";;
    *) printf '0:the fabricated match\n'; return 0;;
  esac
}
