#include "functions.h"
#include <cryptoTools/Network/IOService.h>
#include <cryptoTools/Network/Channel.h>
#include <cryptoTools/Network/Session.h>
#include <math.h>
#include "../common/timing.h"  /* URL: https://github.com/barrust/timing-c */

int main(int argc, char *argv[])
{
    Timing tm;
    timing_start(&tm);


    unsigned char*cipherData;
    int dataLength;

    unsigned char*pubKeyData;
    int pubBytesLen;

    unsigned char*priKeyData;
    int priBytesLen;


    int number_bits,number_hashes,elementCount;


    load_cipherData(&cipherData,dataLength,&pubKeyData,pubBytesLen,
        &priKeyData,priBytesLen,
        number_bits,number_hashes,elementCount);

    mpz_t pubKey[3];
    mpz_t priKey[3];
    for(int i = 0; i < 3; i++)
    {
        mpz_init(priKey[i]);
        mpz_init(priKey[i]);
    }
    binaryData_to_mpzArray(pubKeyData,3,pubKey);
    binaryData_to_mpzArray(priKeyData,3,priKey);

    //std::cout<<pubBytesLen<<std::endl;

    IOService ios(4);
    ios.showErrorMessages(true);
    auto ipAddress = std::string("localhost:1212");
    auto sessionHint = std::string("alice_homo_bob");
    Session client(ios, ipAddress, SessionMode::Client, sessionHint);
    Channel channel = client.addChannel();


    //step1. send alice's small cipherTexts to bob
    int cipherLen = *((int *)cipherData);
    int pubLen = *((int *)pubKeyData);
    std::vector<int> lenData{cipherLen,pubLen};
    channel.send(lenData);


    std::vector<unsigned char> vecCipher = std::vector<unsigned char>(cipherData, cipherData + dataLength);
    channel.asyncSend(std::move(vecCipher));

    //step2. send alice's public pallier keys to bob
    std::vector<unsigned char> vecPubKey = std::vector<unsigned char>(pubKeyData, pubKeyData + pubBytesLen);
    channel.asyncSend(std::move(vecPubKey));


    std::cout<<"second data sending finished"<<std::endl;
    

    //step3. receive bob's homomorphic ciphertexts
    std::vector<char> receiveCiphers;
    channel.recv(receiveCiphers);//this will cause a block.

    mpz_t clearUnion;
    mpz_init(clearUnion);
    mpz_set_str(clearUnion,&receiveCiphers[0],10);
    paillier_decryption(clearUnion,clearUnion,pubKey,priKey);
    int intUnion = mpz_get_ui(clearUnion);

    std::cout<<"intUnion "<<intUnion<<std::endl;

    float base = 1-1/(float)number_bits;
    float r1 =  intUnion/(float)number_bits;
    float ret = log(r1)/log(base);
    ret = ret/number_hashes;
    std::cout<<"final union estimate is: "<<round(ret)<<std::endl;




    //step4. recevie bob's intersection homomorphic ciphertexts
    std::vector<char> intersectRecv;
    channel.recv(intersectRecv);//this will cause a block.

    mpz_t clearIntersect;
    mpz_init(clearIntersect);
    mpz_set_str(clearIntersect,&intersectRecv[0],10);
    paillier_decryption(clearIntersect,clearIntersect,pubKey,priKey);
    int intIntersect = mpz_get_ui(clearIntersect);


    float bits_per_slice =(float)number_bits/number_hashes;
    float number = intIntersect/10000.0f;
    int finalIntersection = elementCount-round(-bits_per_slice*log(number/number_bits));
    std::cout<<"final intersection estimate is: "<<finalIntersection<<std::endl;


    char sentStatistics[100]={0};
    char receiveStatistics[100]={0};

    sprintf(sentStatistics,"%.2f MB",(float)channel.getTotalDataSent()/(1<<20));
    sprintf(receiveStatistics,"%.2f MB",(float)channel.getTotalDataRecv()/(1<<20));

    std::cout
        << "   Session: " << channel.getSession().getName() << std::endl
        // << "   Channel: " << channel.getName() << std::endl
        << "      Sent: " << sentStatistics << std::endl
        << "  received: " << receiveStatistics << std::endl;
    channel.resetStats();

    channel.close();
    client.stop();
    ios.stop();

    MPZ_CLEAR(pubKey,3);
    MPZ_CLEAR(priKey,3);

    timing_end(&tm);
    printf("\nCompleted homomorphic tests in %f seconds!\n", timing_get_difference(tm));

	return 0;
}









