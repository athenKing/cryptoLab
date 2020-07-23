#include "functions.h"
#include <cryptoTools/Network/IOService.h>
#include <cryptoTools/Network/Channel.h>
#include <cryptoTools/Network/Session.h>

int main(int argc, char *argv[])
{
    BloomFilter bf;
    BloomFilter *ptrBF=&bf;

    bloom_filter_init(ptrBF, ELEMENTS, FALSE_POSITIVE_RATE);

    int arrayLength = load_Data_into_BF(ptrBF, "../data/bob.data");

    bloom_filter_stats(ptrBF);

    IOService ios(4);
    ios.showErrorMessages(true);
    auto ipAddress = std::string("localhost:1212");
    auto sessionHint = std::string("alice_homo_bob");

    Session server(ios, ipAddress, SessionMode::Server, sessionHint);
    Channel channel = server.addChannel();

    //step0. receive parameter length and initiate corresponding mpz arrays.
    std::vector<int> destLen;
    channel.recv(destLen);

    int cipherLen=destLen.at(0);
    int pubKeyLen=destLen.at(1);

    mpz_t otherCiphers[cipherLen];
    for(int i=0;i<cipherLen;i++){
        mpz_init(otherCiphers[i]);
    }

    mpz_t pubKeys[pubKeyLen];
    for(int i=0;i<pubKeyLen;i++){
        mpz_init(pubKeys[i]);
    }

    //step1. receive cipherData
    std::vector<unsigned char> receiveVector;
    channel.recv(receiveVector); //will block.


    unsigned char* receiveBuff = &receiveVector[0];
    binaryData_to_mpzArray(receiveBuff,cipherLen,otherCiphers);


    //step2. receive public Pallier keys.
    std::vector<unsigned char> pubKeysVector;
    channel.recv(pubKeysVector); //will block.
    // std::cout<<"receiv size is: "<<pubKeysVector.size()<<std::endl;


    unsigned char* receiveBuff1 = &pubKeysVector[0];
    binaryData_to_mpzArray(receiveBuff1,pubKeyLen,pubKeys);

    std::cout<<"second data receiving finished"<<std::endl;

    //step3. do union calculation
    mpz_t unionVal;
    mpz_init_set_ui(unionVal,1);
    for(int j=0;j<ptrBF->bloom_length;j++){
        unsigned char *cur = ptrBF->bloom + j;
        int slice;
        if(j < (ptrBF->bloom_length-1) )
            slice=7;
        else
            slice=bf.number_bits-(ptrBF->bloom_length-1)*8-1;

        for(int i=slice;i>=0;i--){
            int bitIndex = j*8+(slice-i);
            if(!((*cur>>i) & 1)){
                mpz_mul(unionVal,unionVal,otherCiphers[bitIndex]);
                mpz_mod(unionVal,unionVal, pubKeys[2]);
            }
        }
    }
    char unionChar[3000];
    mpz_get_str(unionChar,10,unionVal);
    channel.send(std::vector<char>(unionChar, unionChar + strlen(unionChar)));


    //step4. do intersection calculation and send ciphertext to the other
    float multi = exp(arrayLength*bf.number_hashes/(float)bf.number_bits);

    mpz_t exponent;
    mpz_init_set_ui(exponent,round(multi*10000));
    mpz_powm(unionVal,unionVal,exponent,pubKeys[2]);

    char intersectChar[3000];
    mpz_get_str(intersectChar,10,unionVal);
    channel.send(std::vector<char>(intersectChar, intersectChar + strlen(intersectChar)));

    MPZ_CLEAR(otherCiphers,cipherLen);
    MPZ_CLEAR(pubKeys,pubKeyLen);

    bloom_filter_destroy(ptrBF);

    channel.close();
    server.stop();
    ios.stop();

	return 0;
}









