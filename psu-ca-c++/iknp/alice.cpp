// #include <thread>
// #include <vector>
// #include <random>

#include <cryptoTools/Network/Channel.h>
#include <cryptoTools/Network/Session.h>
#include <cryptoTools/Network/IOService.h>
#include <cryptoTools/Common/Log.h>
#include <cryptoTools/Common/BitVector.h>
#include <cryptoTools/Common/Matrix.h>

#include <libOTe/Tools/Tools.h>
#include <libOTe/Base/SimplestOT.h>
#include <libOTe/TwoChooseOne/OTExtInterface.h>
#include <libOTe/TwoChooseOne/IknpOtExtReceiver.h>
#include <libOTe/TwoChooseOne/IknpOtExtSender.h>

#include "cJSON.h"
#include "bloom.h"
#include "functions.h"
#include <math.h>

using namespace osuCrypto;


int main(int argc, char *argv[])
{
	IOService ios;
	Session server(ios, "127.0.0.1", 1212, SessionMode::Server);
	Channel recvChannel = server.addChannel();
	PRNG prng0(_mm_set_epi32(4253465, 3434565, 234435, 23987045));

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

	u32 lambda =cJSON_GetObjectItemCaseSensitive(config, "lambda")->valueint;
	u32 mLen = cJSON_GetObjectItemCaseSensitive(iknp, "mLen")->valueint;
	BloomFilter bf;
	BloomFilter *ptrBF=&bf;

    bloom_filter_init(ptrBF, 
    	cJSON_GetObjectItemCaseSensitive(iknp, "bf_capacity")->valueint,
    	cJSON_GetObjectItemCaseSensitive(iknp, "bf_errorRate")->valuedouble);
   	load_Data_into_BF(ptrBF, "../data/alice.data");
    // bloom_filter_stats(ptrBF);
    cJSON_Delete(config);

	//step2.initiate choice bits
	u32 hashNum = ptrBF->number_hashes;
	u32 numOTs = ptrBF->number_bits;


    std::vector<block> recvMsg(numOTs);
    BitVector choices = BitVector(binary2BinString((u8*)ptrBF->bloom,numOTs));
    bloom_filter_destroy(ptrBF);
	u32 bytesLen = mLen/8;


	mpz_t modular;
    mpz_init(modular);
    mpz_set_ui(modular,1);
    mpz_mul_2exp(modular,modular,mLen);

    mpz_t aliceSum;
	mpz_init(aliceSum);

	//step4.receive selected messages from iknp process
	IknpOtExtReceiver recv;
	recv.receiveChosen(choices, recvMsg, prng0, recvChannel);
	
	for(int i=0;i<numOTs;i++)
	{	
		block cur = recvMsg[i];
		std::string str = binary2HexString((unsigned char*)&cur,bytesLen);

		mpz_t random;
		mpz_init(random);
		mpz_set_str(random,str.c_str(),16);
		mpz_add(aliceSum,aliceSum,random);
		mpz_clear(random);
		
		if(i%10 ==0)
		mpz_mod(aliceSum,aliceSum,modular);
	}
	
	mpz_t result;
	mpz_init(result);

	std::string str1;
    recvChannel.recv(str1);
    mpz_set_str(result,str1.c_str(),16);

    mpz_add(result,result,aliceSum);
	mpz_mod(result,result,modular);
	

	int intUnion = mpz_get_ui(result);
	std::cout<<"final union is: "<<intUnion<<std::endl;


    uint64_t ret = bloom_filter_estimate_elements_by_values(numOTs,intUnion,hashNum);

	// float base = 1-1/(float)numOTs;
 //    float r1 =  (numOTs-intUnion)/(float)numOTs;
 //    float ret = log(r1)/log(base);
 //    ret = ret/hashNum;

    std::cout<<"final union estimate is: "<<ret<<std::endl;
	recvChannel.close();
    server.stop();
    ios.stop();

	return 1;
}


