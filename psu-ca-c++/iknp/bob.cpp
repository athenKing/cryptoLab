// #include <thread>
// #include <vector>
#include <random>

#include <cryptoTools/Network/Channel.h>
#include <cryptoTools/Network/Session.h>
#include <cryptoTools/Network/IOService.h>
#include <cryptoTools/Common/Log.h>
#include <cryptoTools/Common/BitVector.h>
#include <cryptoTools/Common/Matrix.h>

#include <libOTe/Tools/Tools.h>
#include <libOTe/TwoChooseOne/OTExtInterface.h>
#include <libOTe/TwoChooseOne/IknpOtExtReceiver.h>
#include <libOTe/TwoChooseOne/IknpOtExtSender.h>

#include "cJSON.h"
#include "functions.h"
// #include <gmpxx.h>
#include "../common/timing.h"  /* URL: https://github.com/barrust/timing-c */


using namespace osuCrypto;

int main(int argc, char *argv[])
{	
	Timing tm;
    timing_start(&tm);

	IOService ios;
	Session client(ios, "127.0.0.1", 1212, SessionMode::Client);
	Channel sendChannel = client.addChannel();
	PRNG prng1(_mm_set_epi32(253233465, 334565, 0, 235));

	//step1. initiate basic parameters
	FILE *fp;
    fp = fopen("../parameters.in", "r");
	fseek(fp, 0, SEEK_END);
	long fsize = ftell(fp);
	fseek(fp, 0, SEEK_SET);/* same as rewind(f); */
	char *content =(char *)malloc(fsize + 1);
	fread(content, 1, fsize, fp);
	fclose(fp);
	cJSON *config = cJSON_Parse(content);
	cJSON *iknp = cJSON_GetObjectItemCaseSensitive(config, "iknp");
	free(content);


	u32 lambda = cJSON_GetObjectItemCaseSensitive(config, "lambda")->valueint;
	u32 mLen = cJSON_GetObjectItemCaseSensitive(iknp, "mLen")->valueint;

	BloomFilter bf;
	BloomFilter *ptrBF=&bf;
    bloom_filter_init(ptrBF, 
    	cJSON_GetObjectItemCaseSensitive(iknp, "bf_capacity")->valueint,
    	cJSON_GetObjectItemCaseSensitive(iknp, "bf_errorRate")->valuedouble);
   	load_Data_into_BF(ptrBF, "../data/bob.data");
    bloom_filter_stats(ptrBF);
	cJSON_Delete(config);


	//step2.initiate send message pairs
	u32 bytesLen = mLen/8;
	u32 numOTs = ptrBF->number_bits;
	u32 strLength = bytesLen*2+2;//mpz_get_str method requires two more bytes allocation

	mpz_t randomSum;
	mpz_init(randomSum);

	mpz_t modular;
    mpz_init(modular);
    mpz_set_ui(modular,1);
    mpz_mul_2exp(modular,modular,mLen);

    //Then TO convert the hexstr to mpz data.
    std::vector<std::array<block, 2>> sendMsg(numOTs);
    std::string bfBits = binary2BinString((u8*)ptrBF->bloom,numOTs);
    for(u32 i=0;i<numOTs;i++){
		char tempString[100]={0};

    	mpz_t random;
		mpz_init(random);
		prng1.get((u8*)tempString,bytesLen);

		std::string binaryHexString = binary2HexString((u8*)tempString,bytesLen);
		mpz_set_str(random,binaryHexString.c_str(),16);
		mpz_add(randomSum,random,randomSum);

		if(i%10 == 0)
		mpz_mod(randomSum,randomSum,modular);

        mpz_t addOne;
		mpz_init(addOne);
		mpz_add_ui(addOne,random,1);
		mpz_mod(addOne,addOne,modular);

		char *hexString0 =(char *)binaryHexString.c_str();
		unsigned char *binaryRandom = (unsigned char *)malloc(bytesLen);
		hexString2BinaryData(binaryRandom,bytesLen,hexString0,strlen(hexString0));


		char *hexString1 = (char *)malloc(strLength);
		memset(hexString1,0,strLength);
		mpz_get_str(hexString1,16,addOne);
		unsigned char *binaryRandomAdd = (unsigned char *)malloc(bytesLen);
		hexString2BinaryData(binaryRandomAdd,bytesLen,hexString1,strlen(hexString1));


		block blockr = toBlock(binaryRandom);
		block blockr1 = toBlock(binaryRandomAdd);
		sendMsg[i][0] = (bfBits.at(i) == '1') ? blockr1:blockr;
		sendMsg[i][1] =  blockr1;

		mpz_clear(random);
		mpz_clear(addOne);
		free(hexString1);

		free(binaryRandom);
		free(binaryRandomAdd);
    }
    bloom_filter_destroy(ptrBF);
	std::cout<<"finishing send messages gen "<<std::endl;
	
	//step4.execuate iknp process
	IknpOtExtSender sender;
	sender.sendChosen(sendMsg, prng1, sendChannel);

	//step5.calcualte algorithms
	mpz_mod(randomSum,randomSum,modular);
	mpz_sub(randomSum,modular,randomSum);


	char *outputStr = (char *)malloc(strLength);
	memset(outputStr,0,bytesLen*2);
    mpz_get_str(outputStr,16,randomSum);
    mpz_clear(randomSum);
	
	std::string outputString(outputStr);
	sendChannel.send(outputString);

	free(outputStr);


	char sentStatistics[100]={0};
    char receiveStatistics[100]={0};
    sprintf(sentStatistics,"%.2f MB",(float)sendChannel.getTotalDataSent()/(1<<20));
    sprintf(receiveStatistics,"%.2f MB",(float)sendChannel.getTotalDataRecv()/(1<<20));
	std::cout<< "   Session: " << sendChannel.getSession().getName() << std::endl
    << "      Sent: " << sentStatistics << std::endl
    << "  received: " << receiveStatistics << std::endl;
    sendChannel.resetStats();


	sendChannel.close();
    client.stop();
    ios.stop();


    timing_end(&tm);
    printf("\nCompleted iknp tests in %f seconds!\n", timing_get_difference(tm));
	return 1;
}


