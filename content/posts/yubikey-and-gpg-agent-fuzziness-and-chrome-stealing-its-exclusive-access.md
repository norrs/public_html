---
title: "Yubikey and Gpg Agent Fuzziness and Chrome Stealing Its Exclusive Access"
date: 2025-11-13T18:58:35+01:00
draft: true
description: ""
---

For some time I have been annoyed at my linux PC that when I try to do a git
clone and I've configured my SSH client to use the gpg-agent for providing the
ssh-agent functionality, so things like ssh-add -L can list my keys that lives
on my physical yubikey (HSM) been a bit painful. I dont know what, but it seems
like chrome has starting for some long time ago to do exclusive access to the
yubikey, I guess it started once the browsers starting doing passkeys etc.
However this annoyed me, I hater had to kill chrome, HUP the gpg-agent, unplug
and plug the yubikey again to make it work.

So I sat down, could I just have a shortcut program which does of all these
things for me that I can run as a stand alone user everytime this happens? Yes
you can and here is the results:

You can now run
https://github.com/norrs/dotfiles/blob/master/dot.tasks/install_yubikey_replug_sudo
which installs a helper script cleverly named yubikey-replug-helper and it adds
a sudoerrs file that you can run this without password. Once this script has
been been bootstrapped, I have this following script in available in my PATH:
https://github.com/norrs/dotfiles/blob/master/dot.local/bin/fix-gpgagent and I
can now run one single command "fix-gpgagent" and it just fixes this crap I
have with exclusive lock and I can have my terminals accessing yubikey again
even after I have launched chrome.

Happy. I've seen multiple user's post this the Internet with issues about this,
but never seen a solution. This is not really a solution either, but a hack
that makes it work again for me..for now.
