Install and configure these:

1. Install [syntax highlighting](https://formulae.brew.sh/formula/zsh-syntax-highlighting) and [auto suggestions](https://formulae.brew.sh/formula/zsh-autosuggestions):
```bash
brew install zsh-autosuggestions zsh-syntax-highlighting
```
2. Add to `~/.zshrc`:
```bash
# Autosuggestions (fish-like)
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh

# Syntax highlighting (green=valid, red=invalid)
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Accept suggestion with right arrow (press → to accept)
bindkey '^[[C' forward-word

# Type partial command, press ↑/↓ to search matching history.
bindkey '^[[A' history-beginning-search-backward
bindkey '^[[B' history-beginning-search-forward
```
