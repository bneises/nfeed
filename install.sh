#/bin/sh

echo -e "\nCreating /etc/nfeed       --does not overwrite existing configs \n"
mkdir -p /etc/nfeed

echo -e "\nCopying/overwriting /etc/init.d scripts\n"
cp etc/init.d/* /etc/init.d/

