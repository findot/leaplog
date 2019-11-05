# leaplog

A simple Leap Motion logger.

## Installation
__Leaplog__ supports Windows, OSX, and Linux. To do so, we can't use Leap Motion versions ulterior to the __2.3.1__ release. This version was compiled for python2. This is, hence, the python version __leaplog__ uses.
1. [Download](https://developer.leapmotion.com/sdk/v2) the __Leap Motion__ client software __v2.3.1__ for your operating system and install it. Depending on the said operating system, the installation process may vary.
    1. __For windows users:__ Execute _Leap_Motion_Setup_4(...).exe_ and follow the instructions. Users who installed the _2017 Fall Creator's Update_, follow [this guide](https://forums.leapmotion.com/t/resolved-windows-10-fall-creators-update-bugfix/6585) to get the driver to work.
    2. __For OSX users:__ Execute the _Leap_Motion_Installer_release(...).dmg_ file and follow the instructions.
    3. __For Linux users:__
    On Debian-based distributions, the installer is a native _deb_ file. To install the Leap Motion on a different distribution, you'll have to either search the web for a ported package (arch users can find one on the [AUR](https://aur.archlinux.org/)) or use a package converter ([alien](https://fedora.pkgs.org/29/fedora-x86_64/alien-8.95-8.fc29.noarch.rpm.html) for fedora & Cie). Note that the _deb_ package was linked with dependencies that are now out of date so you may have to containerize the driver in a way or another (_chroot_, _docker_) to resolve dependency issues.

2. Install __leaplog__ dependencies :
    ```bash
    pip2 install --user -r requirements.txt
    ```

3. Finally, initialize the database :
    ```bash
    python2 -m leaplog initdb
    ```

## Usage

1. Start the server :
    ```bash
    python2 -m leaplog serve
    ```

2. Reach the webapp which by default listens on 0.0.0.0 at port 8000.

3. Recorded data will be saved in the _data.db_ file.

## License
The project is MIT licensed as described in the `LICENSE` file. __Leap Motion__ documentation and libraries (`lib/` and `doc/` folders) are properties of _Ultraleap Ltd_ and are, therefore, licensed under their terms.
