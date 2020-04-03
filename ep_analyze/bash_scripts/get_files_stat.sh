#! /usr/bin/env bash




# find /mnt -path '*/c' -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat


sudo find /mnt -maxdepth 1 -path '*/c' -o -path '*/System\ Volume\ Information*' -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat

sudo find /mnt -maxdepth 1 \( -path '*/c' -o -path '*/System\ Volume\ Information*' \) -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat

`sudo find /mnt \( -path '*/c' -o -path '*/System\ Volume\ Information' \) -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat`