---
title: "Yubikey and Gpg Agent Fuzziness and Chrome Stealing Its Exclusive Access"
date: 2025-11-13T18:58:35+01:00
draft: true
description: ""
---

My Linux workstation relies on `gpg-agent` for SSH auth so I can use the keys stored on my YubiKey. Recently Chrome began taking over the token for WebAuthn/passkey flows; I am not sure whether Chrome, `gpg-agent`, or both components insist on exclusive access, but the result is that `ssh-add -L` and every Git operation hang until I restart half the stack.

Instead of manually killing Chrome, sending `HUP` to `gpg-agent`, and re-seating the key every time, I automated the cleanup:

1. [`dot.tasks/install_yubikey_replug_sudo`](https://github.com/norrs/dotfiles/blob/main/dot.tasks/install_yubikey_replug_sudo) sets up the privileged bits. It installs a tiny helper called `yubikey-replug-helper` (a wrapper around `pkill scdaemon && udevadm trigger`), ensures the binary lives in `~/dot.local/bin/`, and drops a sudoers entry so the helper can cycle USB power without prompting for a password.
2. [`dot.local/bin/fix-gpgagent`](https://github.com/norrs/dotfiles/blob/main/dot.local/bin/fix-gpgagent) is the user-facing command. It invokes the helper via sudo, waits for the stick to re-enumerate, restarts `gpg-agent` with `gpgconf --kill`, and finally re-runs `ssh-add -L` so terminals notice the revived smartcard.

After running the installer once, `fix-gpgagent` becomes a single command I can trigger whenever the stack wedges, and my terminals immediately regain access to the hardware token. It is admittedly a hack, but it has made the workflow tolerable again while I wait for the upstream components to coordinate lock handling.
