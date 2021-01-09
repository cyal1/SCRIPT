
alias iptool="python /Users/cyan/Github/SCRIPT/iptool.py"

alias favicon="python /Users/cyan/Github/FavFreak/favfreak.py"

alias favicon="python /Users/cyan/Github/FavFreak/favfreak.py"

alias dirsearch="python /Users/cyan/Github/dirsearch/dirsearch.py"

alias smuggler="python /Users/cyan/Github/smuggler/smuggler.py"

alias wxunpack="node /Users/cyan/Tools/wxappUnpacker/wuWxapkg.js"

alias persionGen="python3 /Users/cyan/Github/RGPerson/RGPerson.py"

alias upper="perl -ne 'print uc'"

alias lower="perl -ne 'print lc'"

alias title_case="python3 -c \"import sys; print(sys.stdin.read().title(),end='')\""
alias pinyin="python3 -c \"from pypinyin import lazy_pinyin;import sys;print(''.join(lazy_pinyin(sys.stdin.read())),end='')\""

export SPRING=/Users/cyan/Github/topNameIntruder/spring-boot.txt
export WEB=/Users/cyan/Github/dirsearch/db/dicc.txt
export CHINESE_NAME=/Users/cyan/Github/topNameIntruder/chinese-name-top500-pinyin.txt
export PWDTOP1000=/Users/cyan/Github/topNameIntruder/weakpwdtop1000.txt
# export USERNAME=

# export ZSH_DISABLE_COMPFIX=true
export PATH=/Users/cyan/go/bin:$PATH
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/Users/cyan/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=()

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# brew-zsh-completions
#if type brew &>/dev/null; then
#FPATH=$(brew --prefix)/share/zsh-completions:$FPATH

#autoload -Uz compinit
#compinit
#fi

source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /Users/cyan/go/src/github.com/ffuf/pencode/pencode-completion.zsh
source /Users/cyan/go/src/github.com/tomnomnom/gf/gf-completion.zsh

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

export HOMEBREW_NO_AUTO_UPDATE=true

# pyenv
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
# ---

proxysys(){
 if [ ${1}x = "offx" ] ;then
  networksetup -setwebproxystate "Wi-fi" off
  networksetup -setsecurewebproxystate "Wi-fi" off
 elif [ $# -eq 2 ];then
  networksetup -setwebproxy  "Wi-fi" $1 $2
  networksetup -setsecurewebproxy "Wi-fi" $1 $2
 else
  echo "Usage:"
  echo " $0 off  # turn off http(s) proxy"
  echo " $0 IP PORT # set http(s) proxy IP:PORT"
  return -1
 fi
 networksetup -getwebproxy "Wi-Fi"
 networksetup -getsecurewebproxy "Wi-Fi"
}


# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"
