#include <gmpxx.h>
#include "bloom.h"
#include <iostream>

#include <cryptoTools/Common/Defines.h>

int load_Data_into_BF(BloomFilter *bf,const char *filepath);

// void addOne(unsigned char *des,unsigned char *src,int lenBytes);

// void fastModularAdd(unsigned char *des,unsigned char *src,int lenBytes);


// std::string binary2HexString(std::string &ouputStr,unsigned char *src,int lenBytes);
std::string binary2HexString(unsigned char *src,int lenBytes);
std::string binary2BinString(unsigned char *src,int lenBits);



void hexString2BinaryData(unsigned char *des,size_t lenDes,char *src,int lenSrc);

// int hexchr2bin(const char hex);
// void hexString2BinaryData(unsigned char *des,std::string &src,int lenBytes);

// void print128_num(__m128i var);

