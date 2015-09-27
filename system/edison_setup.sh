#! / Bin / sh -x

# ================================================= ================ 
# to the set instead of configure_edison --setup processing 
# ===================== ============================================

# ------------------------------------------------- -------------- 
# 1. hostname 
#set the HOSTNAME to # edison, edison a wireless LAN access point is also set to hostapd to be in 
#. Furthermore edison.local in Bonjour to restart the mDNS so that it can be accessed by.
# If you host name access Bonjour Mac does not need anything, 
# Windows download and install Bonjour from Apple, put a per Avahi I were Linux.

HOSTNAME = "edison"

HOSTNAME_FILE = / etc / hostname
 HOSTAPD_FILE = /Etc/hostapd/hostapd.Conf
 echo  $HOSTNAME > $HOSTNAME_FILE 
hostname -F $HOSTNAME_FILE 
sed -i "s / ^ ssid =. * / ssid = $HOSTNAME /"  $HOSTAPD_FILE
systemctl restart mdns
sleep 2

# ------------------------------------------------- -------------- 
# 2. root password 
# Edison and password is broken even as it's Linux so IoT devices zombie 
# password I always set because there is a risk of being manipulated as 
# host

PASSWORD = "Passw0rdPA55Word"

# Chpasswd, the user name from the standard input: inserting the line of password this 
# initial set by the shell script that password can be set in the 
# in the # useful command 
echo  "root: $PASSWORD"  | chpasswd

# ------------------------------------------------- -------------- 
# 3. Wi-Fi 
# Wi-Fi settings, once connected by configure_edison --wifi is after be established 
# /etc/wpa_supplicant/wpa_supplicant.conf and it should be copied to the # /home/root/wpa_supplicant.conf. In this case, the raw contact note 
# continue passphrase is written.

MY_WPASUPP_FILE = /Home/root/wpa_supplicant.Conf

WPASUPP_FILE = /etc/wpa_supplicant/wpa_supplicant.conf
 \ c P $WPASUPP_FILE  $WPASUPP_FILE .Original
 \ c P $MY_WPASUPP_FILE  $WPASUPP_FILE 
# Among the wpa_supplicant.conf have written a raw PreSharedKey Kotogaa 
# Runode, root to be able to user only read and write 
chmod 600  $WPASUPP_FILE 
# Edison initially move the access point function by hostapd but, Edison 
# is required to hostapd stop if you use a # as a wireless LAN client. Auto 
# also start I stop.
systemctl stop hostapd
systemctl disable hostapd
# It will start the wireless LAN service wpa_supplicant. 
# Hostapd it is exclusively available with. It wants to automatically start the wpa_supplicant.
systemctl restart wpa_supplicant
systemctl enable wpa_supplicant
# under it command to reread the configuration without restarting the wpa_supplicant. Debugging 
# Wpa_cli reconfigure 
# wait until stability is necessary after starting the wireless LAN
sleep 5
# Get the interface name of the wireless LAN, which was started (wlan0) 
WLAN = ` wpa_cli ifname | tail -n 1 ` 
# OK The following two lines as is the case SSID connection setting is one in wpa_supplicant.conf
wpa_cli list_networks
wpa_cli select_network 0
# Since the wireless LAN is connected to the network and set the IP to a wireless LAN with DHCP 
udhcpc -i $WLAN -n


# ------------------------------------------------- -------------- 
# 4. sshd 
# Edison the sshd, which has been connected to the USB device ordinary network de at startup I reconnect to vice.

sed -i 's / ^ BindToDevice = / # BindToDevice = / g' /lib/systemd/system/sshd.Socket
sync
systemctl daemon-reload ;
systemctl restart sshd.socket

# ================================================= ================ 
# Edison default 
# time zone setting, okpg repository configuration 
# ===================== ============================================

# ------------------------------------------------- -------------- 
# set the Timezone of Edison Linux (system time locating affect at Toka ls 
# Lumpur) The following two lines deprecated 
# # rm / etc / localtime; 
# # LN -s / usr / share / zoneinfo / Asia / Tokyo / etc / localtime 
# systemd, which has been adopted by Edison to set the time zone in Timedatectl 
# incidentally ntpdate equivalent is also performed in the systemd 
# another article: http: // qiita. com / CLCL / items / e991e23f4bdbca5ff28b

TIMEZONE = "Europe/Moscow"

timedatectl set-timezone $TIMEZONE

# ------------------------------------------------- -------------- 
# / var / log / Journal is full of measures Nikkei Linux 2015.1

JURNALD_ADD = 'SystemMaxUse = 4M' ; 
JURNALD_CONF = /etc/systemd/journald.Conf
 \ g REP -e "^ $JURNALD_ADD"  $JURNALD_CONF 
if  [  $?  ==  1  ]  ;  then 
  cat << EOS >> $JURNALD_CONF 
$JURNALD_ADD 
EOS

  systemctl stop systemd-journald
  \ R M -rf / var / log / Journal / *
  systemctl start systemd-journald
fi

# ------------------------------------------------- -------------- 
# Edison for the repository registration 
# http://qiita.com/yoneken/items/1b24f0dd8ae00579a0c2

OPKG_BASEFEEDS = /etc/opkg/base-feeds.Conf
 if  [ -s! $OPKG_BASEFEEDS  ]  ;  then 
  cat << EOS> $OPKG_BASEFEEDS 
src / GZ all http://Repo.Opkg.Net/edison/repo/all 
src / GZ edison http://Repo.Opkg.Net/edison/repo/edison 
src / GZ Core2-32 http://Repo.Opkg.Net/edison/repo/core2-32 
EOS

fi

OPKG_INTELIOTDK = /Etc/opkg/intel-iotdk.Conf
 if  [ -s! $OPKG_INTELIOTDK  ]  ;  then 
  cat << EOS> $OPKG_INTELIOTDK 
src intel-iotdk http://iotdk.intel.com/repos/1.1/intelgalactic 
src intel -all http://iotdk.intel.com/repos/1.1/iotdk/all 
src intel-i586 http://iotdk.intel.com/repos/1.1/iotdk/i586 
src intel-x86 http://iotdk.intel.com/repos/1.1/iotdk/x86 
EOS

fi

# ------------------------------------------------- -------------- 
# updated full upgrade package list
opkg update
opkg upgrade


# ================================================= ================ 
# to try to put their favorite package. 
# http://Dev.Classmethod.Jp/hardware/10-edison-package-manager-opkg/ 
# ========================== =======================================

# ------------------------------------------------- -------------- 
# Git (the Toka account will Kaeyo to their s)
opkg install git
git config --global User.Email "gaiar@baimuratov.ru" 
git config --global user.name "gaiar"
git config --global color.ui auto

# ------------------------------------------------- -------------- 
# bash
opkg install bash
chsh -s /bin/bash

# ------------------------------------------------- -------------- 
# rsync
opkg install rsync

# ------------------------------------------------- -------------- 
# Vim
opkg install vim

# You can disposed to clone artifacts from github After this, you can place the module in the Toka # npm, the kick or the 
# application 
# and may or put the automatic start setting at # reboot