#!/usr/bin/env bash
# showutc'yi ~/.local/bin altına bağlar; terminalden "showutc" ile çalışır.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bin_dir="${HOME}/.local/bin"

if ! python3 -c "import tkinter" 2>/dev/null; then
  echo "Tk bulunamadı. Debian/Ubuntu: sudo apt install python3-tk" >&2
  exit 1
fi

mkdir -p "${bin_dir}"
chmod +x "${here}/showutc.py"
ln -sf "${here}/showutc.py" "${bin_dir}/showutc"
echo "Kuruldu: ${bin_dir}/showutc"

case ":${PATH}:" in
  *":${bin_dir}:"*) ;;
  *) echo "Uyarı: ${bin_dir} PATH'te değil. ~/.bashrc'ye ekleyin: export PATH=\"\$HOME/.local/bin:\$PATH\"" ;;
esac
