#!/bin/sh 

# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# Values choosen as random

IV="10987654321098765432109876543210"
SEED="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008" # Fast seed, only one iteration

# Values expected to see. Obtained by comparing to a clean implementation (openssl). A small script to generate these values can be found in software/versat/generateTest
EXPECTED_SHA="574874084239233FD9FF32BC890242F07E83357BE1A1237CE1C6BAC8AEE1B54F"
EXPECTED_AES="4355375130f93dab841058524143602f295e1d8e7bdb76feb94134b06ef4\n7a4c3092a3990ae84a96522c0fb22cdf5dd4cba061f1d5372f70034f317f\nb1c36a5a08f28c7c808d6a0f579ebea2e5e17f95cd2780107d35dc9bd9ae\n7c7c1b2ef9b4\n"

echo -e -n $EXPECTED_AES > aesExpected.txt

# Alice generates a pair of private and public keys using McEliece. She storages the private key and publishes the public key
echo "Generating private and public keys. Takes around half a minute."
echo ""
./crypto -P priv.txt -p pub.txt -s $SEED McEliece

# Bob wants to send this message to Alice encrypted
echo -n "Test string, contains multiple characters in order to test the block stream properly" > in.txt

echo "Going to encrypt the following content:"
cat in.txt
echo ""

# He calculates an hash of the content of the message
echo ""
echo "SHA result:"
FirstSHA=$(./crypto -i in.txt SHA256)
echo $FirstSHA
echo ""
echo "Expected:"
echo $EXPECTED_SHA
echo ""

# Bob uses the public key to generate a session key as well as the chipertext that encapsulates that session key
BobSessionKey=$(./crypto -p pub.txt -o chiperText.txt -s $SEED McEliece)

# Alice receives the chipertext and decapsulates it to generate the same exact session key that Bob has
AliceSessionKey=$(./crypto -P priv.txt -i chiperText.txt -s $SEED McEliece)

echo "Session key from encoding side:"
echo $BobSessionKey
echo ""
echo "Session key from decoding side:"
echo $AliceSessionKey
echo ""

# Bob uses the session key to encrypt the data using AES-256. He uses CBC mode since it's more secure.
./crypto -i in.txt -o out_256_cbc.txt -k $BobSessionKey -v $IV -e AES-256-CBC

xxd -p out_256_cbc.txt > aesGot.txt

echo "AES result:"
cat aesGot.txt
echo ""
echo "Expected:"
echo -e $EXPECTED_AES
echo ""

# Alice receives the encrypted message and uses her own key to decrypt it
./crypto -i out_256_cbc.txt -o decryptedMessage.txt -k $AliceSessionKey -v $IV -d AES-256-CBC

# Alice calculates an hash of the content of the message. Since the hash matches, we know the file was properly encrypted and decrypted
echo "SHA of decrypted result:"
SecondSHA=$(./crypto -i decryptedMessage.txt SHA256)
echo $SecondSHA
echo ""

test $FirstSHA = $EXPECTED_SHA || { echo "Failed SHA" && echo "Example transfer failed!" > test.log && exit 1 ; }
test $SecondSHA = $EXPECTED_SHA || { echo "Failed SHA" && echo "Example transfer failed!" > test.log && exit 1 ; }

cmp -s aesGot.txt aesExpected.txt || { echo "Failed AES" && echo "Example transfer failed!" > test.log && exit 1 ; }

test $BobSessionKey = $AliceSessionKey || { echo "Failed McEliece" && echo "Example transfer failed!" > test.log && exit 1 ; }
echo "Example transfer passed!" | tee test.log
