export SVN_EDITOR=vim

eval "`dircolors -b`"
alias ls='ls --color=auto'
alias ll='ls -l'
alias grep='grep --color=auto'
alias Grep=grep
alias snv=svn

shopt -s histappend
export HISTCONTROL=ignoredups
export HISTIGNORE="pwd:exit:bg:fg"
HISTFILESIZE=1000000000
HISTSIZE=1000000

# shorten current dir
short (){
    link='/tmp/S'`head -1 /dev/urandom | od -N 2 -tx2 | awk '{ print $2 }'`
    [ -e $link ] && sudo rm $link
    ln -s "`pwd`" $link
    cd $link
}
# object-c env
#. /usr/share/GNUstep/Makefiles/GNUstep.sh
#alias cn='zhcon --utf8'

export PYTHONPATH=$HOME/web/:$HOME/web/waf:/opt:/opt/waf
export LANG=zh_CN.UTF8
export PATH="/sbin:/usr/sbin:$PATH"
export PS1='(\D{%H:%M:%S}) \[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\]'