#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Installing Tarn Package Manager..."

# 1. 检查 Termux 环境
if [ ! -d "$PREFIX" ]; then
    echo "❌ Error: Termux environment not found!"
    exit 1
fi

# 2. 下载核心引擎
TARN_URL="https://raw.githubusercontent.com/termux-tarn/tarn/main/tarn.py"
TARGET="$PREFIX/bin/tarn"

echo "Downloading core engine..."
if command -v curl >/dev/null 2>&1; then
    curl -sL "$TARN_URL" -o "$TARGET"
else
    echo "❌ Error: curl is not installed. Please run 'pkg install curl' first."
    exit 1
fi

# 3. 赋予执行权限
chmod +x "$TARGET"

# 4. 提示用户
if [ -f "$TARGET" ]; then
    echo "✅ Installation successful!"
    echo "👉 Run 'tarn update' to fetch the package index."
else
    echo "❌ Installation failed. Please check your network."
fi
