#include "bloom.h"
#include "Paillier.h"
#include <gmpxx.h>
#include <iostream>

#include <cryptoTools/Common/Defines.h>


#define ELEMENTS 40000
#define FALSE_POSITIVE_RATE 0.05
#define KEY_LEN 10
#define MPZ_CLEAR(X,Y) for(int i=0;i<Y;i++){mpz_clear(X[i]);}

using namespace osuCrypto;

int load_Data_into_BF(BloomFilter *bf,const char *filepath);

int encrypt_data_in_BF(BloomFilter *bf,mpz_t* paillier_pubKeys,mpz_t* ciphers);

void mpzArray_to_BinaryData(unsigned char** binaryData,mpz_t* data,int dataLen,int &byteCount,const char* toFilePath);

void load_binaryData_fromFile(unsigned char** binaryData,int &length,const char *filePath);

void binaryData_to_mpzArray(unsigned char* binaryData,int outPutLen,mpz_t *outPut);

int load_cipherData(unsigned char** cipherData,int &dataLength,
	unsigned char** pubKeyData,int &pubBytesLen,
	unsigned char** priKeyData,int &priBytesLen,
	int &numbBits,int &numSlices,int &elementNum);

int calculate_Union_on_AliceData(mpz_t *bobCipher,int bobCipherLen,mpz_t pubKey[3],mpz_t priKey[3],mpz_t unionVal);