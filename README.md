# ssh-kinit.py
SSH to another host and run kinit if there is no ticket or it has expired.

# Prerequisites
OS: Ubuntu

You must have installed python3-paramiko and python3-pykeepass.
```sh
sudo apt install python3-paramiko python3-pykeepass
```

# How to use

Prepare config.json
```sh
cp config.json.example config.json
```

Change KeePass filename (filename) and add Keyfile path (keyfile) if you need
keyfile. Under hosts you must edit hostname, KeePass entry (keepass_entry) and
REALM (realm). REALM value must be upper case (EXAMPLE.COM).

If you specify key "disable" with value "1" this host will be disabled.

    config.json
```
{
    "keepass": {
        "filename": "/home/username/path_to_db.kdbx",
        "keyfile": ""
    },
    "ssh": {
        "DEFAULT": {
            "port": "22",
            "timeout": "3"
        }
    },
    "hosts": {
        "hostname1-realm0-tier1": {
            "keepass_entry": "IdM: EXAMPLE.COM Admin 1",
            "realm": "EXAMPLE.COM"
        },
        "hostname2-realm0-tier2": {
            "keepass_entry": "IdM: EXAMPLE.COM Admin 2",
            "realm": "EXAMPLE.COM"
        },
        "hostname-realm1-tier2": {
            "keepass_entry": "AD: EXAMPLE2.COM Tier 2",
            "realm": "EXAMPLE2.COM",
            "disabled": "1"
        }
    }
}
```

