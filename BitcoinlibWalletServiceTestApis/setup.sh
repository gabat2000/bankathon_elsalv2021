sudo lsblk
sudo file -s /dev/xvdf
sudo mkdir /plane
sudo mount /dev/xvdf /plane
sudo blkid
sudo vim /etc/fstab

UUID=6d9b1162-507e-4df4-8cad-5e570525c812  /plane  xfs  defaults,nofail  0  2

sudo adduser plane
sudo chown -R plana:plane /plane
sudo ufw status
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow https
sudo apt update
sudo apt -y upgrade
#sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
#curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
#sudo apt -y install nodejs
#sudo apt -y  install gcc g++ make
#sudo apt install nodejs npm
#npm install bitcoinjs-lib
#npm install ecpair bip32 
sudo apt install build-essential python-dev python3-dev libgmp3-dev


sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 5003
sudo iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 443 -j REDIRECT --to-ports 5003

sudo su plane
pip3 install bitcoinlib
pip3 install faunadb
pip3 install -U cryptography
pip3 install flask
pip3 install flask_cors
pip3 install jproperties

cd /plane
mkdir wallet
cd /plane/wallet
mkdir log

ssh -i "c:/Users/gabat/Documents/Plan A/AWS/PAB/Key/plana-key-ca.pem" ubuntu@ec2-99-79-143-96.ca-central-1.compute.amazonaws.com
https://github.com/chadidbarnero/bankathon_elsalv2021
